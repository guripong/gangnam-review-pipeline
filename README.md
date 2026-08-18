# Clinic Review Pipeline

Multi-step agentic pipeline: **collect → translate/normalise → validate → publish**

- **Live output: https://ssogi.com/flywheel-demo/**
- Run log / failure notes: [NOTES.md](NOTES.md)

## Deploy
```bash
./deploy.sh          # docs/ -> S3 + CloudFront invalidation
```

## ⚠️ 배포 함정 (사전 검증 2026-08-19)
이 CloudFront 배포는 **403/404 를 `/index.html` 로 200 반환**(SPA 폴백)한다.

- ❌ `https://ssogi.com/flywheel-demo/`  → 슬래시 경로는 폴백에 먹혀 **포트폴리오 홈**이 뜬다
- ✅ `https://ssogi.com/flywheel-demo/index.html` → 실제 결과물
- **HTTP 200 은 배포 성공의 증거가 아니다.** 반드시 본문 문자열로 검증할 것 (`deploy.sh` 가 자동으로 함)

제출 링크는 **반드시 `index.html` 까지 포함**할 것.
