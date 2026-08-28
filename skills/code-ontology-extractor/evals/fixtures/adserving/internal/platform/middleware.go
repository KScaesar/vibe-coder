package platform

import (
	"net/http"
	"time"
)

const upstreamTimeout = 30 * time.Second
const maxIdleConns = 100

type HTTPMiddleware struct {
	next http.Handler
}

func (m *HTTPMiddleware) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	m.next.ServeHTTP(w, r)
}
