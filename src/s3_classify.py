"""Step 3 — classify. 수집물은 '후기'가 아니다. 4종으로 가른다.
news_regulatory 는 버리면 안 된다 — 신뢰 신호의 원천이다."""
import re, json, io
DISCLOSE = ['소정의','원고료','체험단','협찬','제공받','대가를','수수료','서포터즈','앰버서더']
REG = ['공정거래위원회','공정위','시정명령','제재','과징금','뒷광고','기만광고','표시광고법','적발']
CLINIC_VOICE = ['드립니다','안내해','전하여','내원하시','본원','저희 병원','원장입니다']
PATIENT = ['내돈내산','다녀왔','받았어요','했어요','아팠','부었','회복','상담 후기','찐후기']

def classify(t):
    reg = [k for k in REG if k in t]
    dis = [k for k in DISCLOSE if k in t]
    cv  = [k for k in CLINIC_VOICE if k in t]
    pv  = [k for k in PATIENT if k in t]
    fp  = len(re.findall(r'제가|저는|내가', t))
    if len(reg) >= 3:
        return 'news_regulatory', reg
    if dis:
        return 'disclosed_ad', dis
    if cv and fp < 3:
        return 'clinic_marketing', cv
    if pv or fp >= 3:
        return 'patient_report', pv
    return 'unknown', []

if __name__ == '__main__':
    posts = json.load(io.open('data/02_fetched.json', encoding='utf-8'))
    from collections import Counter
    c = Counter()
    for p in posts:
        p['label'], p['label_evidence'] = classify(p['text_ko'])
        c[p['label']] += 1
    io.open('data/03_classified.json','w',encoding='utf-8').write(json.dumps(posts,ensure_ascii=False,indent=1))
    print(f"{len(posts)} posts classified -> data/03_classified.json")
    for k,v in c.most_common(): print(f"  {k:<18} {v}")
