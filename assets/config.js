/*
 * MinaTech MobileRecruit — 公開設定（Phase 2 で実値に差し替え）
 *
 * このファイルだけ書き換えれば、全LPの応募導線・計測タグが切り替わる。
 * 値を実値にした瞬間に有効化される（プレースホルダ判定で自動的にOFF）。
 *
 * - applyUrl    : 応募フォームURL（Google Forms / formrun 等どれでも可）
 * - lineUrl     : LINE公式アカウントの友だち追加URL。例 https://lin.ee/xxxxx
 * - ga4Id       : Google Analytics 4 測定ID。例 G-XXXXXXXXXX
 * - metaPixelId : Meta（Facebook）Pixel ID。広告運用しない場合は空のままでOK。
 * - siteDomain  : 公開ドメイン。canonical/OGPと整合。
 */
window.RECRUIT_CONFIG = {
  applyUrl: 'https://docs.google.com/forms/d/e/1FAIpQLSfERN_c76RnUtKgVTkGxFleahPekol9ZUmqggHAFCi-cFIKyg/viewform',
  lineUrl: 'https://lin.ee/yHJDg2z',
  ga4Id: 'G-P6NJ1GQ4V5',
  metaPixelId: '',
  siteDomain: 'recruit-mobile.minatech1210.com'
};
