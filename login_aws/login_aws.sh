#!/bin/bash
#aws_profile "$1"
#AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
#AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
#AWS_SESSION_TOKEN=$(aws configure get aws_session_token)
#export AWS_ACCESS_KEY_ID
#export AWS_SECRET_ACCESS_KEY
#export AWS_SESSION_TOKEN

# Running python script to get the signed URL
AWS_LOGIN_URL=$(python3 /home/mareedu/login_aws/login_aws.py "$1")
export AWS_LOGIN_URL

echo "$AWS_LOGIN_URL"
