#!/usr/bin/env bash
# 결과 배포: docs/ -> https://ssogi.com/flywheel-demo/
set -e
aws s3 sync ./docs s3://ssogi-site/flywheel-demo/ --profile skyhome --delete
aws cloudfront create-invalidation --distribution-id E37JUDL01DIG5H \
  --paths "/flywheel-demo/*" --profile skyhome --query "Invalidation.Id" --output text
echo "→ https://ssogi.com/flywheel-demo/"
