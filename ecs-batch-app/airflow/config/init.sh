#!/bin/bash

airflow db init

# Connection - AWS Default
airflow connections delete 'aws_default' || true
airflow connections add \
    --conn-type 'aws' \
    --conn-extra "{ \"aws_access_key_id\": \"$AWS_ACCESS_KEY_ID\", \"aws_secret_access_key\": \"$AWS_SECRET_ACCESS_KEY\", \"region_name\": \"$AWS_REGION\" }" \
    aws_default

airflow webserver -p 8080 &
airflow scheduler &
tail -f /dev/null
