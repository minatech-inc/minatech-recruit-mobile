# UTM付きURL一覧（流入元計測用）

各SNS投稿・各求人媒体からの流入を、GA4で別々に集計できるようにするための完成URLです。
**そのままコピペで使えます。**

UTMパラメータ設計:
- `utm_source` = 流入元（indeed / kyujin-box / engage / hellowork / twitter / threads / line / instagram）
- `utm_medium` = jobboard / organic / referral
- `utm_campaign` = `<年Q>_<ペルソナ>` 形式（例: 2026q2_balance）
- `utm_content` = 投稿IDや差分（オプション・SNS連続投稿の識別用）

加えて、各LPの recruit-common.js が `mr_lp` と `mr_action` を自動付与します。

---

## 求人媒体（無料）

### Indeed
```
https://recruit-mobile.minatech1210.com/employee/?utm_source=indeed&utm_medium=jobboard&utm_campaign=2026q2_employee
https://recruit-mobile.minatech1210.com/partner/?utm_source=indeed&utm_medium=jobboard&utm_campaign=2026q2_partner
https://recruit-mobile.minatech1210.com/balance/?utm_source=indeed&utm_medium=jobboard&utm_campaign=2026q2_balance
https://recruit-mobile.minatech1210.com/side/?utm_source=indeed&utm_medium=jobboard&utm_campaign=2026q2_side
https://recruit-mobile.minatech1210.com/urgent/?utm_source=indeed&utm_medium=jobboard&utm_campaign=2026q2_urgent
https://recruit-mobile.minatech1210.com/employee/?utm_source=indeed&utm_medium=jobboard&utm_campaign=2026q2_seishain
```

### 求人ボックス
```
https://recruit-mobile.minatech1210.com/employee/?utm_source=kyujin-box&utm_medium=jobboard&utm_campaign=2026q2_employee
https://recruit-mobile.minatech1210.com/partner/?utm_source=kyujin-box&utm_medium=jobboard&utm_campaign=2026q2_partner
https://recruit-mobile.minatech1210.com/balance/?utm_source=kyujin-box&utm_medium=jobboard&utm_campaign=2026q2_balance
https://recruit-mobile.minatech1210.com/side/?utm_source=kyujin-box&utm_medium=jobboard&utm_campaign=2026q2_side
https://recruit-mobile.minatech1210.com/urgent/?utm_source=kyujin-box&utm_medium=jobboard&utm_campaign=2026q2_urgent
```

### engage
```
https://recruit-mobile.minatech1210.com/employee/?utm_source=engage&utm_medium=jobboard&utm_campaign=2026q2_employee
https://recruit-mobile.minatech1210.com/partner/?utm_source=engage&utm_medium=jobboard&utm_campaign=2026q2_partner
https://recruit-mobile.minatech1210.com/side/?utm_source=engage&utm_medium=jobboard&utm_campaign=2026q2_side
```

### ハローワーク（契約社員のみ可・URL記載欄に）
```
https://recruit-mobile.minatech1210.com/employee/?utm_source=hellowork&utm_medium=jobboard&utm_campaign=2026q2_employee
https://recruit-mobile.minatech1210.com/urgent/?utm_source=hellowork&utm_medium=jobboard&utm_campaign=2026q2_urgent
```

---

## SNS（X / Threads）

### X（Twitter）
**契約社員ペルソナ向け投稿用：**
```
https://recruit-mobile.minatech1210.com/employee/?utm_source=twitter&utm_medium=organic&utm_campaign=2026q2_employee
```

**業務委託ペルソナ向け：**
```
https://recruit-mobile.minatech1210.com/partner/?utm_source=twitter&utm_medium=organic&utm_campaign=2026q2_partner
```

**両立ペルソナ向け：**
```
https://recruit-mobile.minatech1210.com/balance/?utm_source=twitter&utm_medium=organic&utm_campaign=2026q2_balance
```

**副業ペルソナ向け：**
```
https://recruit-mobile.minatech1210.com/side/?utm_source=twitter&utm_medium=organic&utm_campaign=2026q2_side
```

**急募エリア向け：**
```
https://recruit-mobile.minatech1210.com/urgent/?utm_source=twitter&utm_medium=organic&utm_campaign=2026q2_urgent
```

**ハブ訴求用（プロフィール固定リンク）：**
```
https://recruit-mobile.minatech1210.com/?utm_source=twitter&utm_medium=organic&utm_campaign=2026q2_profile
```

### Threads
同じパターンで `utm_source=twitter` → `utm_source=threads` に置換するだけ：
```
https://recruit-mobile.minatech1210.com/employee/?utm_source=threads&utm_medium=organic&utm_campaign=2026q2_employee
https://recruit-mobile.minatech1210.com/partner/?utm_source=threads&utm_medium=organic&utm_campaign=2026q2_partner
https://recruit-mobile.minatech1210.com/balance/?utm_source=threads&utm_medium=organic&utm_campaign=2026q2_balance
https://recruit-mobile.minatech1210.com/side/?utm_source=threads&utm_medium=organic&utm_campaign=2026q2_side
https://recruit-mobile.minatech1210.com/urgent/?utm_source=threads&utm_medium=organic&utm_campaign=2026q2_urgent
https://recruit-mobile.minatech1210.com/?utm_source=threads&utm_medium=organic&utm_campaign=2026q2_profile
```

---

## LINE公式から流す既存友だち向け
```
https://recruit-mobile.minatech1210.com/?utm_source=line&utm_medium=referral&utm_campaign=2026q2_line_broadcast
```

---

## GA4で確認する方法

GA4 → 左メニュー「集客」→ 「トラフィック獲得」 →
「セッションのデフォルトチャネル グループ」を「セッションの参照元 / メディア」に変更 →
`indeed / jobboard` や `twitter / organic` ごとに応募数・滞在時間が見える。

応募完了は別途「CTAクリック数」イベント（cta_apply_click / cta_line_click）で計測される。
