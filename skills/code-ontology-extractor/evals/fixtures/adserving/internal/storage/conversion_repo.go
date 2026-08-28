package storage

import "database/sql"

type ConversionRepo struct {
	db *sql.DB
}

// AdRequestLog 保留每次請求的決策結果，供事後對帳。
type AdRequestLog struct {
	AdRequest string
	Decided   string
}

func (r *ConversionRepo) Insert(clickID string, conversionID string) error {
	_, err := r.db.Exec("INSERT INTO conversion_event (click_id, conversion_id) VALUES ($1, $2)", clickID, conversionID)
	return err
}
