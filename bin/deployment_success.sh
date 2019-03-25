#!/bin/bash

# Varriables
NOTIFY_URL="$1"
GITLAB_USER_NAME="$2"
CI_PIPELINE_URL="$3"
CI_PIPELINE_ID="$4"
PRODUCTION_URL="$5"

# Main
curl -X POST $NOTIFY_URL --data-urlencode \
"payload={ \
  \"channel\": \"#cicd_pipeline\", \
  \"username\": \"GitLab Pipeline\", \
  \"icon_emoji\": \":house:\", \
  \"attachments\": [ \
    { \
      \"fallback\": \"$GITLAB_USER_NAME attempted DEPLOYMENT of pipeline <$CI_PIPELINE_URL|#$CI_PIPELINE_ID>\", \
      \"pretext\": \"$GITLAB_USER_NAME attempted DEPLOYMENT of pipeline <$CI_PIPELINE_URL|#$CI_PIPELINE_ID>\", \
      \"color\": \"good\", \
      \"fields\": [ \
        { \
          \"title\": \"Deployment SUCCEDED\", \
          \"value\": \"Deployment URL: <$PRODUCTION_URL|Reyes HomeAssistant - Production>\" \
        } ] \
    } ] \
}"
