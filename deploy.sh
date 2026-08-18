#!/usr/bin/env bash
# docs/ -> S3 + CloudFront invalidation -> 내용까지 검증
set -e
URL="https://ssogi.com/flywheel-demo/index.html"
MARK="${1:-Clinic Review Pipeline}"   # 페이지에 반드시 있어야 할 문자열

aws s3 sync ./docs s3://ssogi-site/flywheel-demo/ --profile skyhome --delete
ID=$(aws cloudfront create-invalidation --distribution-id E37JUDL01DIG5H \
      --paths "/flywheel-demo/*" --profile skyhome --query "Invalidation.Id" --output text)
echo "invalidation: $ID"

# ⚠️ 이 배포는 403/404 -> /index.html(200) SPA 폴백이 걸려 있어 HTTP 200 은 증거가 안 됨.
#    반드시 본문 문자열로 확인한다.
for i in $(seq 1 40); do
  if curl -s "$URL" | grep -qF "$MARK"; then
    echo "OK  $URL"; exit 0
  fi
  sleep 5
done
echo "FAIL: '$MARK' 를 못 찾음 — 아직 폴백이 잡히는 중이거나 배포 실패"; exit 1
