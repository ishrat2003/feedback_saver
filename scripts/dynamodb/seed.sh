#!/bin/bash
source "$PWD/scripts/dynamodb/common.sh"

cmd="aws dynamodb $endPoint --region $region create-table --cli-input-json file://$PWD/database/dynamodb/seed/story.json"
eval $cmd

cmd="aws dynamodb $endPoint --region $region create-table --cli-input-json file://$PWD/database/dynamodb/seed/termsboard.json"
eval $cmd