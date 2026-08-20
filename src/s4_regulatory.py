"""Step 4 — regulatory signal. 제재 뉴스에서 '어느 병원이' 제재됐는지 뽑아
사이트 클리닉 레코드에 sanction 플래그를 붙인다. 이게 verified-surgeon 보다 상위 신호다."""
import re, json, io
from collections import defaultdict

SITE = {  # gangnambeautyguide.com 레코드
    "뷰성형외과":     {"slug":"view-ps",  "en":"View Plastic Surgery",  "tier":"GOLD","rating":4.8},
    "디에이성형외과": {"slug":"da-ps",    "en":"DA Plastic Surgery",    "tier":"GOLD","rating":4.7},
    "에이비성형외과": {"slug":"ab-ps",    "en":"AB Plastic Surgery",    "tier":"GOLD","rating":4.8},
    "브라운성형외과": {"slug":"braun-ps", "en":"Braun Plastic Surgery", "tier":"GOLD","rating":4.8},
}
# 표기 변형 -> 정규 클리닉명 (clinic normalisation)
ALIAS = {
    "뷰성형외과":"뷰성형외과", "뷰 성형외과":"뷰성형외과",
    "디에이성형외과":"디에이성형외과", "디에이 성형외과":"디에이성형외과", "DA성형외과":"디에이성형외과",
    "에이비성형외과":"에이비성형외과", "에이비성형외과의원":"에이비성형외과", "에이비 성형외과":"에이비성형외과",
    "브라운성형외과":"브라운성형외과", "브라운아이성형외과":"브라운성형외과", "브라운아이의원":"브라운성형외과",
}
SANCTION = ['공정거래위원회','공정위','시정명령','제재','뒷광고','기만광고','후기 조작','적발']

if __name__ == '__main__':
    posts = json.load(io.open('data/03_classified.json', encoding='utf-8'))
    hits = defaultdict(list)
    for p in posts:
        if p['label'] != 'news_regulatory':
            continue
        t = p['text_ko']
        named = {ALIAS[a] for a in ALIAS if a in t}
        for canon in named:
            hits[canon].append({"url": p['url'], "clinic_searched": p['clinic_slug'],
                                "evidence": [k for k in SANCTION if k in t][:5],
                                "excerpt": re.sub(r'\s+',' ', t[:160])})
    out = []
    for canon, rec in SITE.items():
        ev = hits.get(canon, [])
        out.append({**rec, "clinic_ko": canon,
                    "sanctioned": bool(ev), "evidence_count": len(ev),
                    "sources": [e["url"] for e in ev][:4],
                    "markers": sorted({m for e in ev for m in e["evidence"]}),
                    "excerpt": ev[0]["excerpt"] if ev else ""})
    io.open('data/04_regulatory.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
    for r in out:
        flag = "SANCTIONED" if r["sanctioned"] else "clean"
        print(f"  {r['slug']:<10} {r['clinic_ko']:<8} tier={r['tier']} rating={r['rating']}  -> {flag} (evidence {r['evidence_count']})")
