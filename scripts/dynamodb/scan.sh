#!/bin/bash
source "$PWD/scripts/dynamodb/common.sh"

cmd="aws dynamodb $endPoint --region $region scan --table-name story --query \"Items[*].[user_code.S,story_link.S]\" --output text"
echo $cmd
eval $cmd

cmd="aws dynamodb $endPoint --region $region scan --table-name termsboard --query \"Items[*].[user_code.S,story_term.S]\" --output text"
echo $cmd
eval $cmd