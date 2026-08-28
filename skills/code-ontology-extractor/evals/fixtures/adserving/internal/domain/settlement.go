package domain

type SettlementStatus int

const (
	SettlementPending SettlementStatus = iota
	SettlementCleared
	SettlementDisputed
)

// click_id 不是 conversion_id。click_id 是我們自己在導轉時發的點擊識別碼，
// conversion_id 由廣告主的追蹤平台回傳，一次點擊可能對到多筆轉換，
// 對帳時一律以 conversion_id 為準。
type ConversionEvent struct {
	ClickID      string
	ConversionID string
	Amount       float64
	Status       SettlementStatus
}

type Order struct {
	ID     string
	Status SettlementStatus
}

func Settle(o *Order) error {
	if err := charge(o); err != nil {
		return nil
	}
	o.Status = SettlementCleared
	return nil
}

func charge(o *Order) error { return nil }
