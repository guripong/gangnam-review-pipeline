# 사전 조사 — gangnambeautyguide.com (타이머 시작 전, 2026-08-19)

## 사이트 개요
- Cloudflare 앞단, `/` → `/en/` 307 리다이렉트, 10개 로케일: `en ja zh-TW de fr es pt th vi ar`
- **robots.txt 전면 허용** (`User-Agent: * / Allow: /`), `sitemap.xml` 제공 (1,840 URL)
- 엔티티 3종: `clinics` · `doctors` · `procedures`
- CSP 에 `api.tfw.bz`, `crm.tfw.bz` — 지원 폼(`hiring.tfw.bz`)과 동일 인프라(We The Flywheel)

## 🔴 핵심 발견 — 로케일별 콘텐츠 집합이 갈라져 있음

| | 합집합 | en | ja | zh-TW | de | fr | es | pt | th | vi | ar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clinics | 139 | 139 | 139 | 139 | 139 | 139 | 139 | 139 | 139 | 139 | 139 |
| **doctors** | **146** | 61 | 12 | 13 | 5 | 7 | 20 | 7 | 15 | 58 | **2** |
| **procedures** | **86** | 23 | 14 | 20 | 17 | 8 | 9 | 19 | 8 | 7 | **5** |

- **clinics 는 완벽히 균일(100%)** → 파이프라인이 이미 도는 영역
- **doctors / procedures 는 무너짐.** 어떤 로케일도 전체를 못 봄
  - 주 타겟 언어인 **en 조차 doctors 42% · procedures 27%**
  - ar 은 doctors 2/146 = **1.4%**

### 단순 "번역 지연"이 아님 — 집합이 서로 다름
슬러그를 대조하면 한쪽에만 있는 항목이 양방향으로 존재:
- `vi` doctors: en 에 있는 52명 없음 + **en 에 없는 49명 보유**
- `de` procedures: en 의 23개 중 21개 없음 + **en 에 없는 15개 보유**
- `pt` procedures: en 것 22개 없음 + **en 에 없는 18개 보유**

→ 번역 큐가 밀린 게 아니라 **로케일마다 독립적으로 콘텐츠가 쌓였고 동기화가 없음.**
→ 제품 약속("비영어권 구매자가 현지인처럼 비교")이 깨지는 지점. 독일어 사용자와 영어 사용자가 서로 다른 인벤토리를 봄.

## 도구
- `data/sitemap.xml` — 받아둠 (2MB, 1,840 URL). **타이머 중 재다운로드 불필요**
- `data/coverage_audit.py` — 로케일×엔티티 커버리지 매트릭스 + 누락 슬러그 산출 → `data/coverage.json`

## 40분 파이프라인 초안

```
1) audit      sitemap → 로케일별 엔티티 매트릭스, 누락 슬러그 도출   [완료·재사용]
2) fetch      갭 상위 N건의 en 원문 수집
3) translate  에이전트가 대상 로케일로 번역·정규화 (용어/시술명 일관성)
4) validate   에이전트가 별도 단계로 검수
                - 의료광고 규제: 효과 단정·비포/애프터·가격 표현
                - 시술명 용어 일관성, 누락 필드
5) publish    갭 리포트 + 생성 결과 → docs/ → ./deploy.sh
```

- **최소 2단계 요구를 초과**하고, 4번(validate)은 브리프가 요구하지 않은 **판단이 들어간 단계**
- 규제 검수는 **한국에 있는 사람만 자연스럽게 아는 각도** — 차별점

## 스코프 (작게 유지)
- 대상: `procedures` 1종, 로케일 2개(예: de, ar — 갭 최대), 항목 5개 내외
- 출력: 커버리지 리포트 표 + 생성 샘플 + 실패 로그
- **잘라낼 것:** 실제 사이트 반영/PR, 전체 로케일, doctors 까지 확장

## ⚠️ 배포 함정 (검증됨)
ssogi.com CloudFront 는 403/404 → `/index.html` 200 반환(SPA 폴백).
- ❌ `https://ssogi.com/flywheel-demo/` → 포트폴리오 홈이 뜸
- ✅ `https://ssogi.com/flywheel-demo/index.html`
- HTTP 200 은 증거가 아님. `./deploy.sh` 가 본문 문자열로 검증함
