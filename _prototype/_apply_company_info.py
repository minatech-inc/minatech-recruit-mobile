"""Phase 2 step 1: MinaTech 会社情報を全ファイルに反映。
このスクリプトは _prototype/ 配下に置いてあるだけで、サイト配信には含まれない。
1回実行したら役目終わり。"""
import sys
from pathlib import Path

base = Path(__file__).resolve().parents[1]

# -----------------------------------------------------------------------------
# 1) 全LPの JobPosting JSON-LD：コメント解除 + hiringOrganization 差し込み +
#    validThrough 追加
# -----------------------------------------------------------------------------
hiring_old = '"name":"(公開前に会社名を設定)","sameAs":"https://recruit-mobile.minatech1210.com/"'
hiring_new = (
    '"name":"MinaTech株式会社","telephone":"+81-467-28-7603",'
    '"address":{"@type":"PostalAddress","postalCode":"251-0055",'
    '"addressCountry":"JP","addressRegion":"神奈川県",'
    '"addressLocality":"藤沢市","streetAddress":"南藤沢3-12 クリオ藤沢駅前 7階"}'
)

vt_old = '"datePosted":"2026-05-23","hiringOrganization":'
vt_new = (
    '"datePosted":"2026-05-23",'
    '"validThrough":"2026-11-30T23:59:59+09:00","hiringOrganization":'
)

comment_open_old = (
    '<!-- JobPosting JSON-LD: Phase 2 で会社情報差し込み後にコメント解除 -->\n'
    '<!--\n'
    '<script type="application/ld+json">'
)
comment_open_new = (
    '<!-- JobPosting JSON-LD（Phase 2 で有効化済） -->\n'
    '<script type="application/ld+json">'
)

comment_close_old = '</script>\n-->\n<link rel="preconnect" href="https://fonts.googleapis.com">'
comment_close_new = '</script>\n<link rel="preconnect" href="https://fonts.googleapis.com">'

# -----------------------------------------------------------------------------
# 2) 5LPの footer：会社情報ブロックを追加
# -----------------------------------------------------------------------------
lp_copyrights = {
    'employee': '© 2026 CAREER. All Rights Reserved.',
    'partner':  '© 2026 PARTNERS. ALL RIGHTS RESERVED.',
    'balance':  '© 2026 balance. All Rights Reserved.',
    'side':     '© 2026 SIDE/PARTNER. ALL RIGHTS RESERVED.',
    'urgent':   '© 2026 URGENT.RECRUIT — HOKKAIDO / SHIZUOKA',
}

dark_footer_block = (
    '<div style="margin-bottom: 16px; font-size: 12px; line-height: 1.85; '
    'color: rgba(255,255,255,0.72); '
    "font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, 'Hiragino Sans', sans-serif; "
    'letter-spacing: normal;">\n'
    '    <strong style="font-weight: 700; color: rgba(255,255,255,0.92);">MinaTech株式会社</strong> ｜ '
    '〒251-0055 神奈川県藤沢市南藤沢3-12 クリオ藤沢駅前 7階<br>\n'
    '    TEL <a href="tel:0467287603" style="color: inherit; text-decoration: none;">0467-28-7603</a> ｜ '
    '採用窓口 <a href="mailto:recruit@minatech1210.com" style="color: inherit; text-decoration: none;">recruit@minatech1210.com</a>\n'
    '  </div>\n'
    '  '
)

# -----------------------------------------------------------------------------
# 3) hub index.html の footer：会社情報を copyright の上に挿入
# -----------------------------------------------------------------------------
hub_footer_old = (
    '<footer>\n'
    '  <div>© 2026 MinaTech MobileRecruit</div>\n'
    '  <div class="legal">運営：（公開前に会社名を設定）</div>\n'
    '</footer>'
)
hub_footer_new = (
    '<footer>\n'
    '  <div style="margin-bottom: 14px; font-size: 12.5px; line-height: 1.85; color: var(--ink-soft);">\n'
    '    <strong style="color: var(--ink); font-weight: 700;">MinaTech株式会社</strong> ｜ '
    '〒251-0055 神奈川県藤沢市南藤沢3-12 クリオ藤沢駅前 7階<br>\n'
    '    TEL <a href="tel:0467287603" style="color: var(--ink-soft);">0467-28-7603</a> ｜ '
    '採用窓口 <a href="mailto:recruit@minatech1210.com" style="color: var(--ink-soft);">recruit@minatech1210.com</a>\n'
    '  </div>\n'
    '  <div>© 2026 MinaTech MobileRecruit</div>\n'
    '</footer>'
)

# -----------------------------------------------------------------------------
def main():
    failures = []

    # 1) LPs JSON-LD
    for lp in lp_copyrights:
        p = base / lp / 'index.html'
        c = p.read_text(encoding='utf-8')
        original = c
        c = c.replace(hiring_old, hiring_new)
        c = c.replace(vt_old, vt_new)
        c = c.replace(comment_open_old, comment_open_new)
        c = c.replace(comment_close_old, comment_close_new)
        # footer
        cp = lp_copyrights[lp]
        if cp in c:
            c = c.replace(cp, dark_footer_block + cp, 1)
        else:
            failures.append(f'  - footer copyright not found in {lp}/index.html')
        if c != original:
            p.write_text(c, encoding='utf-8')
            print(f'  OK   {lp}/index.html updated ({len(original)} → {len(c)} chars)')
        else:
            failures.append(f'  - no changes applied to {lp}/index.html')

    # 2) Hub
    p = base / 'index.html'
    c = p.read_text(encoding='utf-8')
    if hub_footer_old in c:
        c = c.replace(hub_footer_old, hub_footer_new)
        p.write_text(c, encoding='utf-8')
        print('  OK   index.html (hub) footer updated')
    else:
        failures.append('  - hub footer pattern not found')

    if failures:
        print('\nFAILURES:')
        for f in failures:
            print(f)
        sys.exit(1)
    print('\nAll updates applied successfully.')

if __name__ == '__main__':
    main()
