"""사이트맵 -> 로케일별 엔티티 커버리지 매트릭스 + 갭 진단."""
import re, io, sys, json, collections
LOCS = ['en','ja','zh-TW','de','fr','es','pt','th','vi','ar']

def load(path='data/sitemap.xml'):
    urls = re.findall(r'<loc>([^<]+)</loc>', io.open(path, encoding='utf-8').read())
    slugs = collections.defaultdict(lambda: collections.defaultdict(set))
    for u in urls:
        p = u.replace('https://gangnambeautyguide.com','').strip('/').split('/')
        if len(p) >= 3:
            slugs[p[1]][p[0]].add('/'.join(p[2:]))
    return slugs

def report(slugs):
    out = {}
    for typ in ['clinics','doctors','procedures']:
        union = set().union(*slugs[typ].values())
        out[typ] = {
            'union': len(union),
            'per_locale': {l: len(slugs[typ].get(l,set())) for l in LOCS},
            'missing_vs_union': {l: sorted(union - slugs[typ].get(l,set())) for l in LOCS},
        }
    return out

if __name__ == '__main__':
    r = report(load())
    for typ, d in r.items():
        print(f"\n== {typ}  (합집합 {d['union']}) ==")
        for l in LOCS:
            print(f"  {l:<6} 보유 {d['per_locale'][l]:>3}  누락 {len(d['missing_vs_union'][l]):>3}")
    json.dump(r, io.open('data/coverage.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n-> data/coverage.json')
