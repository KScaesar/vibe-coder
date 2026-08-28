package platform

import "strings"

type RedisKeyBuilder struct {
	prefix string
}

func (b *RedisKeyBuilder) Build(parts ...string) string {
	return b.prefix + ":" + strings.Join(parts, ":")
}
