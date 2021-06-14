#!/bin/bash
source "$PWD/scripts/deploy/common.sh"

# Usage: createLamdaFunction LambdaName FolderName HandlerName
createLamdaFunction feedbacksaver feedback save_handler
aws apigateway create-deployment --rest-api-id feedbacksaverapi --region $REGION
