package api

import (
	"net/http"
	"time"
)

const decisionTimeout = 2700 * time.Millisecond

// AdRequest 是播放器在廣告破口打過來的一次請求。
type AdRequest struct {
	PlacementID string
	UserID      string
	DeviceType  string
	BreakIndex  int
}

func Serve(addr string) error {
	return http.ListenAndServe(addr, nil)
}

func decide(w http.ResponseWriter, r *http.Request) {
	ctx, cancel := context.WithTimeout(r.Context(), decisionTimeout)
	defer cancel()
	_ = ctx
}
