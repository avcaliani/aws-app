#!/bin/bash -xe
# @author       Anthony Vilarim Caliani
# @contact      github.com/avcaliani

# Project Root
cd "$(dirname "$0")/../.."
printf "\033[1;32m%s:\033[00m %s\n" "current directory" "$(pwd)"

APP_ENV='local' spark-submit \
  --master 'local' \
  --packages 'org.apache.hudi:hudi-spark3-bundle_2.12:0.9.0,org.apache.spark:spark-avro_2.12:3.0.1' \
  main.py "$@" || (cd - && exit 1)

cd - && exit 0
