#!/usr/bin/env bash
# 建立 layer-review eval 用的 fixture repo：一個小型 Go 訂單服務，含三個 commit。
# 用法：setup_fixture.sh <target-dir> [--dirty]
#   --dirty：額外在 working tree 留下未提交的改動（eval 2 用）
set -euo pipefail

target="$1"
mode="${2:-}"

rm -rf "$target"
mkdir -p "$target"
cd "$target"
git init -q -b main
git config user.name fixture
git config user.email fixture@example.com

mkdir -p domain app infra httpapi

cat > go.mod <<'EOF'
module example.com/orders

go 1.22
EOF

cat > domain/order.go <<'EOF'
package domain

import "errors"

type OrderID string

type Order struct {
	ID         OrderID
	CustomerID string
	Items      []Item
}

type Item struct {
	SKU      string
	Quantity int
	Price    int64 // cents
}

var ErrEmptyOrder = errors.New("order has no items")

func NewOrder(id OrderID, customerID string, items []Item) (*Order, error) {
	if len(items) == 0 {
		return nil, ErrEmptyOrder
	}
	return &Order{ID: id, CustomerID: customerID, Items: items}, nil
}

func (o *Order) Total() int64 {
	var sum int64
	for _, it := range o.Items {
		sum += it.Price * int64(it.Quantity)
	}
	return sum
}

type OrderRepository interface {
	Save(o *Order) error
	FindByCustomer(customerID string) ([]*Order, error)
}
EOF

cat > app/place_order.go <<'EOF'
package app

import "example.com/orders/domain"

type PlaceOrder struct {
	Repo domain.OrderRepository
}

func (uc PlaceOrder) Execute(id domain.OrderID, customerID string, items []domain.Item) (*domain.Order, error) {
	o, err := domain.NewOrder(id, customerID, items)
	if err != nil {
		return nil, err
	}
	if err := uc.Repo.Save(o); err != nil {
		return nil, err
	}
	return o, nil
}
EOF

cat > infra/order_repo.go <<'EOF'
package infra

import (
	"database/sql"

	"example.com/orders/domain"
)

type SQLOrderRepo struct {
	DB *sql.DB
}

func (r SQLOrderRepo) Save(o *domain.Order) error {
	_, err := r.DB.Exec(`INSERT INTO orders (id, customer_id) VALUES ($1, $2)`, o.ID, o.CustomerID)
	return err
}

func (r SQLOrderRepo) FindByCustomer(customerID string) ([]*domain.Order, error) {
	rows, err := r.DB.Query(`SELECT id, customer_id FROM orders WHERE customer_id = $1`, customerID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []*domain.Order
	for rows.Next() {
		var o domain.Order
		if err := rows.Scan(&o.ID, &o.CustomerID); err != nil {
			return nil, err
		}
		out = append(out, &o)
	}
	return out, rows.Err()
}
EOF

cat > httpapi/handler.go <<'EOF'
package httpapi

import (
	"encoding/json"
	"net/http"

	"example.com/orders/app"
	"example.com/orders/domain"
)

type Handler struct {
	Place app.PlaceOrder
}

type placeReq struct {
	ID         string        `json:"id"`
	CustomerID string        `json:"customer_id"`
	Items      []domain.Item `json:"items"`
}

func (h Handler) PlaceOrder(w http.ResponseWriter, r *http.Request) {
	var req placeReq
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	o, err := h.Place.Execute(domain.OrderID(req.ID), req.CustomerID, req.Items)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnprocessableEntity)
		return
	}
	json.NewEncoder(w).Encode(o)
}
EOF

git add -A
git commit -q -m "feat: initial order service"

# commit 2：加入 VIP 折扣與訂單列表。刻意埋入分層與安全問題：
# - 折扣規則寫在 handler（業務規則外洩到 UI 層）
# - domain 直接依賴 database/sql 與 log
# - repo 以字串拼接 SQL（SQL injection）且逐筆查 items（N+1）
# - 為單一實作加了多餘的 factory 抽象
cat > domain/order.go <<'EOF'
package domain

import (
	"database/sql"
	"errors"
	"log"
)

type OrderID string

type Order struct {
	ID         OrderID
	CustomerID string
	Items      []Item
	Discount   int64
}

type Item struct {
	SKU      string
	Quantity int
	Price    int64 // cents
}

var ErrEmptyOrder = errors.New("order has no items")

func NewOrder(id OrderID, customerID string, items []Item) (*Order, error) {
	if len(items) == 0 {
		return nil, ErrEmptyOrder
	}
	return &Order{ID: id, CustomerID: customerID, Items: items}, nil
}

func (o *Order) Total() int64 {
	var sum int64
	for _, it := range o.Items {
		sum += it.Price * int64(it.Quantity)
	}
	log.Printf("order %s total=%d", o.ID, sum)
	return sum - o.Discount
}

// LoadVIP 直接查 DB 判斷客戶是否為 VIP。
func LoadVIP(db *sql.DB, customerID string) bool {
	var vip bool
	_ = db.QueryRow(`SELECT vip FROM customers WHERE id = $1`, customerID).Scan(&vip)
	return vip
}

type OrderRepository interface {
	Save(o *Order) error
	FindByCustomer(customerID string) ([]*Order, error)
}

type OrderRepositoryFactory interface {
	Create() OrderRepository
}
EOF

cat > infra/order_repo.go <<'EOF'
package infra

import (
	"database/sql"
	"fmt"

	"example.com/orders/domain"
)

type SQLOrderRepo struct {
	DB *sql.DB
}

type SQLOrderRepoFactory struct {
	DB *sql.DB
}

func (f SQLOrderRepoFactory) Create() domain.OrderRepository {
	return SQLOrderRepo{DB: f.DB}
}

func (r SQLOrderRepo) Save(o *domain.Order) error {
	_, err := r.DB.Exec(`INSERT INTO orders (id, customer_id, discount) VALUES ($1, $2, $3)`, o.ID, o.CustomerID, o.Discount)
	return err
}

func (r SQLOrderRepo) FindByCustomer(customerID string) ([]*domain.Order, error) {
	q := fmt.Sprintf("SELECT id, customer_id, discount FROM orders WHERE customer_id = '%s'", customerID)
	rows, err := r.DB.Query(q)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []*domain.Order
	for rows.Next() {
		var o domain.Order
		if err := rows.Scan(&o.ID, &o.CustomerID, &o.Discount); err != nil {
			return nil, err
		}
		itemRows, err := r.DB.Query(`SELECT sku, quantity, price FROM order_items WHERE order_id = $1`, o.ID)
		if err != nil {
			return nil, err
		}
		for itemRows.Next() {
			var it domain.Item
			if err := itemRows.Scan(&it.SKU, &it.Quantity, &it.Price); err != nil {
				itemRows.Close()
				return nil, err
			}
			o.Items = append(o.Items, it)
		}
		itemRows.Close()
		out = append(out, &o)
	}
	return out, rows.Err()
}
EOF

cat > httpapi/handler.go <<'EOF'
package httpapi

import (
	"database/sql"
	"encoding/json"
	"net/http"

	"example.com/orders/app"
	"example.com/orders/domain"
)

type Handler struct {
	Place app.PlaceOrder
	Repo  domain.OrderRepository
	DB    *sql.DB
}

type placeReq struct {
	ID         string        `json:"id"`
	CustomerID string        `json:"customer_id"`
	Items      []domain.Item `json:"items"`
}

func (h Handler) PlaceOrder(w http.ResponseWriter, r *http.Request) {
	var req placeReq
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	o, err := h.Place.Execute(domain.OrderID(req.ID), req.CustomerID, req.Items)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnprocessableEntity)
		return
	}
	// VIP 打九折，滿 1000 元再折 50 元
	if domain.LoadVIP(h.DB, req.CustomerID) {
		o.Discount = o.Total() / 10
		if o.Total() > 100000 {
			o.Discount += 5000
		}
	}
	json.NewEncoder(w).Encode(o)
}

func (h Handler) ListOrders(w http.ResponseWriter, r *http.Request) {
	orders, err := h.Repo.FindByCustomer(r.URL.Query().Get("customer_id"))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(orders)
}
EOF

git add -A
git commit -q -m "feat: VIP discount and order listing"

# commit 3：小修正
sed -i.bak 's/StatusUnprocessableEntity/StatusBadRequest/' httpapi/handler.go
rm -f httpapi/handler.go.bak
git add -A
git commit -q -m "fix: return 400 on invalid order"

if [ "$mode" = "--dirty" ]; then
	# 未提交改動：app 層開始自己管 transaction，但 Save 失敗時沒有 rollback
	cat > app/place_order.go <<'EOF'
package app

import (
	"database/sql"

	"example.com/orders/domain"
)

type PlaceOrder struct {
	Repo domain.OrderRepository
	DB   *sql.DB
}

func (uc PlaceOrder) Execute(id domain.OrderID, customerID string, items []domain.Item) (*domain.Order, error) {
	tx, err := uc.DB.Begin()
	if err != nil {
		return nil, err
	}
	o, err := domain.NewOrder(id, customerID, items)
	if err != nil {
		return nil, err
	}
	if err := uc.Repo.Save(o); err != nil {
		return nil, err
	}
	return o, tx.Commit()
}
EOF
fi
