sam build --template-file ./api/template.yaml

sam package \
  --template-file ./api/template.yaml \
  --output-template-file ./api/package.yml \
  --s3-bucket feedbacksaver