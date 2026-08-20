"""Step 2 — fetch/parse.
함정: blog.naver.com/{id}/{logNo} 직접 URL 은 iframe 껍데기(한글 22자).
     PostView 엔드포인트로 재작성해야 본문이 온다.
     se-main-container 통짜 정규식은 중첩 때문에 제목만 잡히므로 se-text-paragraph 문단 단위로 파싱."""
import re, json, io, time, urllib.request

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36'}
POSTVIEW = ("https://blog.naver.com/PostView.naver?blogId={bid}&logNo={log}"
            "&redirect=Dlog&widgetTypeCall=true&directAccess=false")

def body(bid, log):
    html = urllib.request.urlopen(urllib.request.Request(POSTVIEW.format(bid=bid, log=log), headers=UA), timeout=25).read().decode('utf-8', 'replace')
    paras = re.findall(r'<p class="se-text-paragraph[^"]*"[^>]*>(.*?)</p>', html, re.S)
    lines = []
    for p in paras:
        t = re.sub(r'<[^>]+>', '', p)
        t = t.replace('&nbsp;', ' ').replace('​', '')
        t = re.sub(r'\s+', ' ', t).strip()
        if t and t not in lines:
            lines.append(t)
    return '\n'.join(lines)

if __name__ == '__main__':
    posts = json.load(io.open('data/01_discovered.json', encoding='utf-8'))
    out, fail = [], 0
    for p in posts:
        try:
            txt = body(p['blog_id'], p['log_no'])
        except Exception as e:
            fail += 1; continue
        if len(re.findall(r'[가-힣]', txt)) < 200:   # 껍데기/빈 글 방어
            fail += 1; continue
        p['text_ko'] = txt
        p['ko_chars'] = len(re.findall(r'[가-힣]', txt))
        out.append(p); time.sleep(0.3)
    io.open('data/02_fetched.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"fetched {len(out)} / {len(posts)}  (skipped {fail})  -> data/02_fetched.json")
