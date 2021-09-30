#!/bin/bash -xe
# @author       Anthony Vilarim Caliani
# @contact      github.com/avcaliani

APP_VERSION=${1:?'App version not informed!'}
APP_REPLACE=${2:-'no'}

DEPLOY_PATH="s3://nth-dev-datalake/jobs/batch-app/$APP_VERSION"
DIST='./dist'

rm -rf "$DIST" || true
mkdir -p "$DIST"
zip -r "$DIST/src.zip" "./src" -x "*__pycache__*"
cp "main.py" "$DIST"

version_exists="$(aws s3 ls "$DEPLOY_PATH" || echo '')"
if [ -n "$version_exists" ] && [ "$APP_REPLACE" = 'no' ]; then
  echo "Version $APP_VERSION already exists!"
  exit 1
fi

aws s3 cp "$DIST" "$DEPLOY_PATH" --recursive
aws s3 ls "$DEPLOY_PATH"
exit 0
