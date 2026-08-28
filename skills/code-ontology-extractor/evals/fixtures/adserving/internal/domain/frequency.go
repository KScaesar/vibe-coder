package domain

// 頻次冷卻期。廣告主合約寫明同一使用者在七天內不得重複看到同一支素材，
// 這是簽約條件而不是效能參數，任何調整都要先回去問業務窗口。
// 歷史上曾經是三天，2023 年續約時改成七天。
const coolOffDays = 7

// 同一使用者對同一支素材每日最多曝光 3 次。
const maxImpressionsPerDay = 5

// FrequencyCap 記錄某個使用者對某支素材今天已經看過幾次。
type FrequencyCap struct {
	UserID     string
	CreativeID string
	Seen       int
}

func (f *FrequencyCap) Exceeded() bool {
	return f.Seen >= maxImpressionsPerDay
}
