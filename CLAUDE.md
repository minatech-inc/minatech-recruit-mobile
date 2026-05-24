# MinaTech-MobileRecruit プロジェクト指示書

## 概要
携帯販売スタッフ・パートナーの採用サイト。
docomo / au / SoftBank / 楽天モバイルの販売を行う二次代理店向けのリクルートメディア。
ターゲット別に5つのLP + ハブの構成で、SNS・媒体からの流入を1サイトで受ける。

## 公開
- URL: https://recruit-mobile.minatech1210.com
- ホスティング: Cloudflare Pages + GitHub Pages
- 応募フォーム: Google Forms（Apps Script 自動生成・回答は Google スプレッドシートに集約・recruit@ にメール通知）
- 補助導線: LINE公式アカウント

## ディレクトリ構造

```
MinaTech-MobileRecruit/
├── index.html              # ハブ（新規）
├── employee/index.html     # 契約社員LP（プロトタイプ流用）
├── partner/index.html      # 業務委託LP（プロトタイプ流用）
├── balance/index.html      # 両立LP（プロトタイプ流用）
├── side/index.html         # 副業LP（プロトタイプ流用）
├── urgent/index.html       # 急募LP（プロトタイプ流用）
├── assets/
│   ├── config.js           # 公開設定（URL・ID）
│   ├── recruit-common.js   # 共通機能
│   └── ogp/                # OGP画像
├── _prototype/             # 元プロトタイプ（編集禁止・参照用）
├── 404.html / robots.txt / sitemap.xml / CNAME
└── README.md
```

## 設計の重要前提

**5つのLPは「共通テンプレートの色違い」ではなく、それぞれ完全に別物のデザイン。**
カラー・フォント・クラス名・セクション構成、すべて異なる。
CSSは1ファイルずつ自己完結。共通化されているのは「機能レイヤー（JS）」のみ。

→ コピー修正は各LPファイル内で完結する。LP間でデザイン要素を流用しない。

## 共通機能（assets/recruit-common.js）

各LPの `<body>` には `data-lp="<LP名>"` を付与。
共通JSは以下を提供：

1. UTMパラメータ収集（sessionStorage保存）
2. `[data-action="apply"]` / `[data-action="line"]` のhref一元差し込み
3. FAQアコーディオン開閉
4. GA4 / Meta Pixel ロード（実値時のみ）
5. CTAクリック計測

config.js がプレースホルダ値のときは応募リンクはアラート表示（誤公開防止）。

## コンプライアンス厳守事項

1. **性別限定表現の禁止**（男女雇用機会均等法）
   - NG: 「女性歓迎」「主婦向け」「ママ歓迎」
   - OK: 「家庭と両立したい方」「週3〜働ける方」
2. **根拠のない数字を使わない**
   - 統計データは必ず出典明記（既存LPは出典あり）
   - 「未経験◯％」等の創作値は復活させない
3. **業務委託契約に「残業代」概念を持ち込まない**
   - 「実働8時間を超える場合は事前協議の上、別途支払い」と表現
4. **誇大表現の禁止**
   - 「絶対稼げる」「業界No.1」等は使わない
5. **金額の整合性**
   - 全LP・全媒体で 未経験15,000〜18,000円・経験者20,000円〜 で統一

## 公開前に必須の差し込み項目

- `assets/config.js` の formrunUrl / lineUrl / ga4Id / metaPixelId
- 各LPの `<!-- JobPosting JSON-LD -->` の hiringOrganization.name
- ハブと各LPのフッターの「（公開前に会社名を設定）」
- 会社情報（所在地・法人番号・電話・採用メール・宅建免許等の媒体審査必須項目）
- スタッフインタビュー動画URL（YouTube限定公開・縦9:16・遅延読み込み対応）

## デプロイ

初回: `C:\Users\MinaTech株式会社\.claude\scripts\new-business.ps1 -Name "MobileRecruit" -Subdomain "recruit-mobile"`
（既存の `_prototype/` `assets/` `*/index.html` を保持したまま実行する）

2回目以降: `git push` で Cloudflare Pages が自動再デプロイ。

## 触らないファイル

- `_prototype/` 配下：Claude.aiで作成した原本。改修は本ファイル群（プロジェクトルートの各LP）に対して行い、_prototype は参照用として温存。
