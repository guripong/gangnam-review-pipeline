"""Step 5 — publish. 데이터 덤프가 아니라 '파이프라인이 잡아낸 것' 리포트."""
import json, io, html, datetime
from collections import Counter

reg = json.load(io.open('data/04_regulatory.json', encoding='utf-8'))
posts = json.load(io.open('data/03_classified.json', encoding='utf-8'))
c = Counter(p['label'] for p in posts)
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M KST')
LBL = {'news_regulatory':'Regulatory news','clinic_marketing':'Clinic marketing copy',
       'disclosed_ad':'Disclosed paid post','patient_report':'Genuine patient report','unknown':'Unclassified'}

rows = ""
for r in reg:
    if r['sanctioned']:
        badge = '<span class="bad">KFTC SANCTIONED</span>'
        src = " ".join(f'<a href="{html.escape(u)}">src{i+1}</a>' for i,u in enumerate(r['sources']))
        note = f"<div class=note>markers: {', '.join(r['markers'])} &middot; {r['evidence_count']} sources &middot; {src}</div>"
    else:
        badge = '<span class="ok">no sanction found</span>'; note = "<div class=note>control case &mdash; detector did not fire</div>"
    rows += f"""<tr><td><code>{r['slug']}</code><br><span class=ko>{html.escape(r['clinic_ko'])}</span></td>
    <td>{html.escape(r['en'])}</td><td class=c>{r['tier']} TIER<br>&#9733; {r['rating']}</td>
    <td>{badge}{note}</td></tr>"""

corpus = "".join(f"<li><b>{v}</b> &mdash; {LBL.get(k,k)}</li>" for k,v in c.most_common())

io.open('docs/index.html','w',encoding='utf-8').write(f"""<!doctype html><meta charset=utf-8>
<title>Clinic Review Pipeline — what it caught</title>
<style>
:root{{--bg:#fff;--fg:#111;--mut:#666;--line:#e3e3e6;--bad:#b3261e;--ok:#1b6b3a;--card:#faf9f8}}
@media(prefers-color-scheme:dark){{:root{{--bg:#111315;--fg:#e9e9ea;--mut:#9a9a9e;--line:#2a2d31;--bad:#ff7a70;--ok:#6ee7a0;--card:#17191c}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,-apple-system,sans-serif;max-width:860px;margin:0 auto;padding:40px 18px}}
h1{{font-size:22px;margin:0 0 6px}} .sub{{color:var(--mut);font-size:13px;margin-bottom:26px}}
.lead{{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--bad);padding:14px 16px;border-radius:6px;margin:20px 0}}
table{{border-collapse:collapse;width:100%;margin:18px 0;font-size:14px}}
th,td{{border-bottom:1px solid var(--line);padding:10px 8px;text-align:left;vertical-align:top}}
th{{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}}
td.c{{white-space:nowrap}} code{{font-size:13px}} .ko{{color:var(--mut);font-size:12px}}
.bad{{color:var(--bad);font-weight:700;font-size:12px}} .ok{{color:var(--ok);font-weight:600;font-size:12px}}
.note{{color:var(--mut);font-size:11.5px;margin-top:4px}} a{{color:inherit}}
ul{{padding-left:20px}} .pipe{{background:var(--card);border:1px solid var(--line);padding:12px 14px;border-radius:6px;font:12.5px/1.7 ui-monospace,monospace;overflow-x:auto}}
</style>
<h1>Clinic Review Pipeline — what it caught</h1>
<div class=sub>Second review source for Gangnam Beauty Guide &middot; generated {now}</div>

<div class=lead><b>Three of the four clinics sampled were sanctioned by the Korea Fair Trade Commission
for eight years of fabricated reviews.</b> Gangnam Beauty Guide currently lists all three as
GOLD TIER with 4.7&ndash;4.8 ratings. The evidence exists only in Korean-language sources.</div>

<table><tr><th>Clinic</th><th>Site record</th><th>Tier / rating</th><th>Pipeline verdict</th></tr>{rows}</table>

<h3>What the corpus actually contained</h3>
<p class=sub>24 Korean posts retrieved for &ldquo;&lt;clinic&gt; 후기&rdquo;. Only two were genuine patient reports.</p>
<ul>{corpus}</ul>
<p>A naive scrape&rarr;translate&rarr;publish pipeline would have syndicated clinic marketing copy and
paid posts to English-speaking medical-tourism buyers as patient testimony.</p>

<h3>Pipeline</h3>
<div class=pipe>s1 discover &nbsp;&rarr;&nbsp; Naver blog search (public; Naver Search API is no longer offered to new apps)<br>
s2 fetch &nbsp;&nbsp;&nbsp;&nbsp;&rarr;&nbsp; PostView endpoint + se-text-paragraph parse (direct URL returns an iframe shell)<br>
s3 classify &nbsp;&rarr;&nbsp; agent step: regulatory news / disclosed ad / clinic marketing / patient report<br>
s4 regulatory &rarr;&nbsp; agent step: name extraction + clinic-alias normalisation &rarr; sanction flag<br>
s5 publish &nbsp;&nbsp;&rarr;&nbsp; S3 + CloudFront, verified by body text (403/404 fall back to a 200 SPA shell)</div>
<p class=sub>Code: <a href="https://github.com/guripong/gangnam-review-pipeline">github.com/guripong/gangnam-review-pipeline</a></p>
""")
print('docs/index.html written')
