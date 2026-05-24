# MinaTech-MobileRecruit

携帯販売スタッフ・パートナーの採用サイト。
公開: <https://recruit-mobile.minatech1210.com>

## サイト構成

| パス | 役割 | 訴求 |
|---|---|---|
| `/` | ハブ | 5つの働き方への振り分け |
| `/employee/` | 契約社員LP | 安定・正社員登用あり |
| `/partner/` | 業務委託LP | 自由・もっと稼ぐ |
| `/balance/` | 両立LP | 家庭と両立・週3〜 |
| `/side/` | 副業LP | 本業と並行・複業OK |
| `/urgent/` | 急募LP | 北海道・静岡エリア |

## 技術スタック

- 静的HTML（ビルドツールなし・素のHTML/CSS/JS）
- ホスティング: Cloudflare Pages（GitHub Pages 経由）
- ドメイン管理: Cloudflare DNS
- 応募フォーム: Google Forms（Apps Script で自動生成、回答は Google スプレッドシートに集約）
- 計測: Google Analytics 4（必要に応じて Meta Pixel）

## ディレクトリ

```
MinaTech-MobileRecruit/
├── index.html              ← ハブ（5LPへの導線）
├── employee/index.html     ← 契約社員LP
├── partner/index.html      ← 業務委託LP
├── balance/index.html      ← 両立LP
├── side/index.html         ← 副業LP
├── urgent/index.html       ← 急募LP
├── assets/
│   ├── config.js           ← URL・ID集中管理（Phase 2 で差し替え）
│   ├── recruit-common.js   ← 共通機能（UTM/CTA/FAQ/GA4/Pixel）
│   └── ogp/                ← OGP画像
├── 404.html / robots.txt / sitemap.xml / CNAME
├── _prototype/             ← Claude.ai で作った元プロトタイプ（参照用）
└── README.md / CLAUDE.md
```

## 共通機能（assets/recruit-common.js）

全LP共通で動く：

1. **UTM収集**：流入URLの `utm_*` を `sessionStorage` に保存
2. **応募/LINEリンク差し込み**：`data-action="apply"` / `data-action="line"` を持つ要素のhrefをconfig.jsの値に書き換え、UTM・LP名・アクション名を付与
3. **FAQアコーディオン**：`.faq-item .faq-q` クリックで `.open` トグル
4. **GA4 / Meta Pixel**：config.jsが実値のときのみロード
5. **CTAクリック計測**：`cta_apply_click` / `cta_line_click`

## 公開前に差し込む値（Phase 2）

`assets/config.js` を書き換える：

```js
window.RECRUIT_CONFIG = {
  applyUrl: 'https://docs.google.com/forms/d/e/.../viewform',  // Google Forms / formrun どちらでも
  lineUrl: 'https://lin.ee/xxxxx',
  ga4Id: 'G-XXXXXXXXXX',
  metaPixelId: '',  // 広告運用しないなら空
  siteDomain: 'recruit-mobile.minatech1210.com'
};
```

加えて各LPの `<!-- JobPosting JSON-LD -->` コメント内に会社名・電話・所在地を入れてコメント解除。
フッターの「（公開前に会社名を設定）」も実値に。

## デプロイ

`C:\Users\MinaTech株式会社\.claude\scripts\new-business.ps1` を使い、初回のみGitHub/Cloudflare/Pages/SSLを一発構築する。
2回目以降は `git push` で Cloudflare Pages が自動再デプロイ。

## コンプライアンス（コピー編集時に必ず守る）

- 性別限定表現NG（「女性歓迎」「主婦向け」等）→ 「両立したい方」等で代替
- 根拠のない数字を使わない（出典明記の統計データのみ）
- 業務委託に「残業代」概念を持ち込まない
- 給与は全LP統一：未経験 15,000〜18,000円 / 経験者 20,000円〜

詳細は `_prototype/data-verification-report.md`（未配置）と [CLAUDE.md](CLAUDE.md) を参照。
