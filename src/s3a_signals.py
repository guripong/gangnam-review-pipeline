"""Step 3a — 결정적 신호 추출. 에이전트가 판단할 근거만 압축해서 넘긴다.
키워드로 잡히는 건 '정직하게 밝힌 광고'뿐. 미표시 광고는 문체로만 잡히므로 3b(에이전트)로 넘김."""
import re, json, io
DISCLOSE = ['소정의','원고료','체험단','협찬','제공받','광고','제휴','수수료','대가를','서포터즈','앰버서더','무상']
CLINIC_VOICE = ['드립니다','안내해','전하여','내원하시','예약 문의','상담 문의','전화 문의','저희','본원','오시는 길','진료시간']
PATIENT_VOICE = ['저는','제가','받았어요','했어요','했는데','다녀왔','고민하다','후기입니다','아팠','부었','회복']

def sig(t):
    return {
        "disclose": sorted({k for k in DISCLOSE if k in t}),
        "clinic_voice": sorted({k for k in CLINIC_VOICE if k in t}),
        "patient_voice": sorted({k for k in PATIENT_VOICE if k in t}),
        "first_person": len(re.findall(r'제가|저는|저희', t)),
        "phone": bool(re.search(r'0\d{1,2}[-.]?\d{3,4}[-.]?\d{4}', t)),
    }

if __name__ == '__main__':
    posts = json.load(io.open('data/02_fetched.json', encoding='utf-8'))
    for p in posts:
        p['signals'] = sig(p['text_ko'])
        p['head'] = p['text_ko'][:220]
    io.open('data/03a_signals.json','w',encoding='utf-8').write(json.dumps(posts,ensure_ascii=False,indent=1))
    n=sum(1 for p in posts if p['signals']['disclose'])
    print(f"{len(posts)} posts | 대가성 표지 보유 {n} ({100*n//len(posts)}%) -> data/03a_signals.json")
