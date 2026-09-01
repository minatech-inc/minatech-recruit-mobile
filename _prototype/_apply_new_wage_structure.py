"""半年ごと昇給制への切替スクリプト（Phase 3.5）

【新給与体系】
・入社〜6ヶ月:  日給 17,600円（月20日換算 35.2万円）
・7〜12ヶ月:   日給 20,900円（月20日換算 40.18万円）
・13〜18ヶ月:  日給 23,100円（月20日換算 46.2万円）
・19ヶ月〜:    日給 26,400円（月20日換算 52.8万円）
※経験者はスタート段階を面談で相談

【従前】
未経験 日給/日額 15,000〜18,000円 / 経験者 日給/日額 20,000円〜
月収例: 未経験300,000円〜 / 経験者400,000円〜
"""
import sys
from pathlib import Path

base = Path(__file__).resolve().parents[1]

# 全ファイル共通の置換（安全なもの）
COMMON_REPLACEMENTS = [
    # JSON-LD baseSalary
    ('"minValue":15000,"maxValue":20000',
     '"minValue":17600,"maxValue":26400'),
    # JSON-LD description mentions
    ('日給15,000円〜18,000円（未経験）／20,000円〜（経験者）',
     '日給17,600円スタート・半年ごとに昇給・2年で26,400円'),
    ('日額15,000円〜18,000円（未経験）／20,000円〜（経験者）',
     '日額17,600円スタート・半年ごとに昇給・2年で26,400円'),
]

# ファイル別置換
FILE_REPLACEMENTS = {
    'index.html': [
        # hub conditions
        ('<div class="cond-val">15,000円〜</div>',
         '<div class="cond-val">17,600円〜</div>'),
        # hub note
        ('<strong>給与（全LP共通）：</strong>未経験 日給/日額 15,000円〜18,000円 ／ 経験者 日給/日額 20,000円〜<br>',
         '<strong>給与（全LP共通）：</strong>日給/日額 17,600円スタート・半年ごとに昇給・2年で26,400円（月20日換算：35.2万→52.8万）<br>'),
    ],
    'employee/index.html': [
        # hero stat
        ('<div class="stat-num">15,000<span class="unit">円〜</span></div>',
         '<div class="stat-num">17,600<span class="unit">円〜</span></div>'),
        # DATA section - 未経験月収
        ('          <div class="data-big">300,000<span class="unit">円〜</span></div>\n          <div class="data-label">未経験スタート時の月収例</div>',
         '          <div class="data-big">352,000<span class="unit">円</span></div>\n          <div class="data-label">スタート時の月収例（半年ごとに昇給）</div>'),
        # DATA section - 未経験説明
        ('日給15,000円×月20日稼働の場合。未経験でも15,000〜18,000円スタートで、しっかり稼げます。',
         '日給17,600円×月20日稼働の場合。半年ごとに昇給し、2年後には日給26,400円（月52.8万円）まで到達します。'),
        # DATA section - 経験者月収
        ('          <div class="data-big">400,000<span class="unit">円〜</span></div>\n          <div class="data-label">経験者の月収例</div>',
         '          <div class="data-big">528,000<span class="unit">円</span></div>\n          <div class="data-label">2年経過後の月収例（半年ごとの昇給後）</div>'),
        # DATA section - 経験者説明
        ('日給20,000円×月20日稼働の場合。経験者は初日から日給20,000円スタートです。',
         '日給26,400円×月20日稼働の場合。全員が半年ごとの昇給で到達する水準。経験者はスタート段階を面談で相談・優遇。'),
        # FLEXIBILITY 契約社員
        ('<li>日給15,000円〜</li>',
         '<li>日給17,600円スタート</li>'),
    ],
    'partner/index.html': [
        # hero-price
        ('¥15,000<span class="unit">/day〜</span>',
         '¥17,600<span class="unit">/day〜</span>'),
        # hero-price-label (英語)
        ('DAILY FEE (UNEXPERIENCED 15,000〜18,000 / EXPERIENCED 20,000)',
         'STARTING ¥17,600/DAY · RAISED EVERY 6 MONTHS · UP TO ¥26,400 IN 2 YEARS'),
        # FLEXIBILITY 業務委託
        ('<li>手取り最大化</li>',
         '<li>日額17,600円スタート・半年で昇給</li>'),
        # money-content
        ('額面の日給だけじゃない。<br>\n          「手取りでどれだけ残るか」が、<br>\n          本当の稼ぎ方です。',
         '額面の日給だけじゃない。<br>\n          「手取りでどれだけ残るか」が、<br>\n          本当の稼ぎ方です。<br><br>\n          <strong>スタート日額17,600円 → 半年で20,900円 → 12ヶ月で23,100円 → 18ヶ月で26,400円</strong>まで、半年ごとに単価改定する仕組み。'),
        # money-table 月額（同稼働）
        ('        <div class="money-row">\n          <span>月額(同稼働)</span>\n          <span class="val-a">¥300,000</span>\n          <span class="val-b">¥300,000</span>\n        </div>',
         '        <div class="money-row">\n          <span>月額(スタート・月20日)</span>\n          <span class="val-a">¥352,000</span>\n          <span class="val-b">¥352,000</span>\n        </div>\n        <div class="money-row">\n          <span>月額(2年後・月20日)</span>\n          <span class="val-a">¥528,000</span>\n          <span class="val-b">¥528,000</span>\n        </div>'),
    ],
    'balance/index.html': [
        # hero-stats 15,000 doesn't exist in balance (uses 週3日〜/10:00始業/直行直帰)
        # 募集要項 給与
        ('未経験:日給/日額 15,000円〜18,000円<br>経験者:日給/日額 20,000円〜<br><span style="font-size: 12px;">※月収例:未経験 月300,000円〜(月20日稼働)</span>',
         '【半年ごとの昇給制】<br>・入社〜6ヶ月：日給/日額 17,600円（月20日 35.2万円）<br>・7〜12ヶ月：日給/日額 20,900円（月20日 40.18万円）<br>・13〜18ヶ月：日給/日額 23,100円（月20日 46.2万円）<br>・19ヶ月〜：日給/日額 26,400円（月20日 52.8万円）<br><span style="font-size: 12px;">※経験者はスタート段階を面談で相談</span>'),
    ],
    'side/index.html': [
        # hero-price
        ('<div class="hero-price">¥15,000</div>',
         '<div class="hero-price">¥17,600</div>'),
        # hero-price-sub
        ('/day〜 (未経験15,000〜18,000 / 経験者¥20,000〜)',
         '/day〜 スタート・半年ごと昇給・2年で¥26,400/日'),
        # compare-table 月額
        ('        <div class="compare-row">\n          <span>月額(同稼働)</span>\n          <span class="col-a">¥300,000</span>\n          <span class="col-b">¥300,000</span>\n        </div>',
         '        <div class="compare-row">\n          <span>月額(スタート)</span>\n          <span class="col-a">¥352,000</span>\n          <span class="col-b">¥352,000</span>\n        </div>\n        <div class="compare-row">\n          <span>月額(2年後)</span>\n          <span class="col-a">¥528,000</span>\n          <span class="col-b">¥528,000</span>\n        </div>'),
    ],
    'urgent/index.html': [
        # pay-marquee (2ペア×2セット=4置換)
        ('未経験 ¥15,000〜18,000/日', 'スタート ¥17,600/日'),
        ('経験者 ¥20,000/日', '2年後 ¥26,400/日'),
        # pay-cards
        ('未経験 / NO EXP.', 'スタート / START'),
        ('経験者 / EXPERIENCED', '2年後 / AFTER 2Y'),
        ('<div class="pay-card-amount">15,000<span class="small">〜18,000円</span></div>',
         '<div class="pay-card-amount">17,600<span class="small">円/日</span></div>'),
        ('<div class="pay-card-amount">20,000<span class="small">円〜</span></div>',
         '<div class="pay-card-amount">26,400<span class="small">円/日</span></div>'),
        ('日給/日額・1日実働8時間<br>月収例:300,000円〜(月20日稼働)',
         '日給・実働8時間<br>月20日稼働で月35.2万円'),
        ('日給/日額・1日実働8時間<br>月収例:400,000円〜(月20日稼働)',
         '日給・実働8時間<br>月20日稼働で月52.8万円（半年ごと昇給後）'),
        # cond-table 給与
        ('未経験:<span class="hl">日給15,000〜18,000円</span> / 経験者:<span class="hl">日給20,000円〜</span>',
         '<span class="hl">日給17,600円スタート → 半年ごとに昇給 → 2年で26,400円</span>（月20日稼働で月35.2万〜52.8万円）'),
    ],
}

def apply_replacements(path, replacements):
    p = base / path
    if not p.exists():
        return f'MISSING: {path}'
    content = p.read_text(encoding='utf-8')
    original = content
    hits = 0
    misses = []
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            hits += 1
        else:
            misses.append(old[:60])
    if content != original:
        p.write_text(content, encoding='utf-8')
    result = f'{path}: {hits} hits'
    if misses:
        result += f' | {len(misses)} misses'
    return result, misses

def main():
    print('=== 半年ごと昇給制への切替 ===\n')
    all_misses = {}

    # 全ファイル共通
    for lp in ['employee', 'partner', 'balance', 'side', 'urgent']:
        path = f'{lp}/index.html'
        result, misses = apply_replacements(path, COMMON_REPLACEMENTS)
        print(f'  [共通] {result}')
        if misses:
            all_misses[f'共通-{lp}'] = misses

    # ファイル別
    print()
    for path, reps in FILE_REPLACEMENTS.items():
        result, misses = apply_replacements(path, reps)
        print(f'  [個別] {result}')
        if misses:
            all_misses[f'個別-{path}'] = misses

    if all_misses:
        print('\n=== マッチしなかったパターン（要調査） ===')
        for k, v in all_misses.items():
            print(f'\n[{k}]')
            for m in v:
                print(f'  - {m}...')
    print('\n完了。')

if __name__ == '__main__':
    main()
