#!/bin/bash

# Varriables
NOTIFY_URL="$1"
GITLAB_USER_NAME="$2"
CI_PIPELINE_URL="$3"
CI_PIPELINE_ID="$4"
CI_PROJECT_URL="$5"
CI_COMMIT_REF_NAME="$6"
CI_BUILD_REF_NAME="$7"
CI_COMMIT_SHA="$8"
CI_COMMIT_TITLE="$9"

# Main
curl -X POST $NOTIFY_URL --data-urlencode \
"payload={ \
  \"channel\": \"#cicd_pipeline\", \
  \"username\": \"GitLab Pipeline\", \
  \"icon_emoji\": \":tada:\", \
  \"attachments\": [ \
    { \
      \"fallback\": \"$GITLAB_USER_NAME attempted BUILDING pipeline <$CI_PIPELINE_URL|#$CI_PIPELINE_ID>\", \
      \"pretext\": \"$GITLAB_USER_NAME attempted BUILDING pipeline <$CI_PIPELINE_URL|#$CI_PIPELINE_ID>\", \
      \"color\": \"good\", \
      \"fields\": [ \
        { \
          \"title\": \"Unit Test SUCCEDED\", \
          \"value\": \"Source branch: <$CI_PROJECT_URL/tree/$CI_COMMIT_REF_NAME|$CI_BUILD_REF_NAME> \nCommit comment: <$CI_PROJECT_URL/commit/$CI_COMMIT_SHA|$CI_COMMIT_TITLE>\" \
        } ] \
    } ] \
}"
