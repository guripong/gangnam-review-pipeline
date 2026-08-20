"""Step 1 — discover. 네이버 블로그 공개 검색 -> 포스트 URL.
Naver Search API 가 신규 앱 등록에서 제거되어 공개 검색 페이지를 사용."""
import re, json, io, time, urllib.parse, urllib.request

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36'}
CLINICS = [
    {"slug": "view-ps",   "ko": "뷰성형외과",    "en": "View Plastic Surgery"},
    {"slug": "da-ps",     "ko": "디에이성형외과", "en": "DA Plastic Surgery"},
    {"slug": "braun-ps",  "ko": "브라운성형외과", "en": "Braun Plastic Surgery"},
    {"slug": "ab-ps",     "ko": "에이비성형외과", "en": "AB Plastic Surgery"},
]
PER_CLINIC = 6

def discover(ko):
    q = urllib.parse.quote(ko + " 후기")
    url = f"https://search.naver.com/search.naver?where=blog&query={q}"
    html = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read().decode('utf-8', 'replace')
    pairs = re.findall(r'https?://blog\.naver\.com/([A-Za-z0-9_-]+)/(\d+)', html)
    return list(dict.fromkeys(pairs))[:PER_CLINIC]

if __name__ == '__main__':
    out = []
    for c in CLINICS:
        for bid, log in discover(c["ko"]):
            out.append({"clinic_slug": c["slug"], "clinic_ko": c["ko"], "clinic_en": c["en"],
                        "blog_id": bid, "log_no": log,
                        "url": f"https://blog.naver.com/{bid}/{log}"})
        time.sleep(0.4)
    io.open('data/01_discovered.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"discovered {len(out)} posts across {len(CLINICS)} clinics -> data/01_discovered.json")
