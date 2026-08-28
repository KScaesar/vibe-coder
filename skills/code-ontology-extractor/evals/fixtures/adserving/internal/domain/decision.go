package domain

import "time"

const maxDailySpend = 50000

// DecisionContext 是做一次決策所需要的全部輸入。
type DecisionContext struct {
	AdRequest *AdRequest
	Now       time.Time
}

type Creative struct {
	ID         string
	SpentToday int
}

// Decide 從候選素材中挑一支回給這次請求。
func Decide(dc *DecisionContext, cands []Creative, all []Creative) *Creative {
	elig := make([]Creative, 0, len(cands))
	for _, c := range cands {
		if c.SpentToday >= maxDailySpend {
			continue
		}
		elig = append(elig, c)
	}
	if len(elig) == 0 {
		return &all[0]
	}
	return &elig[0]
}
