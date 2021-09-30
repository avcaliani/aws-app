# AWS - EMR App
By Anthony Vilarim Caliani

![#](https://img.shields.io/badge/licence-MIT-lightseagreen.svg) ![#](https://img.shields.io/badge/python-3.9.x-yellow.svg)

## Quick Start

```bash
python -m venv .venv \
    && source .venv/bin/activate \
    && pip install -r requirements.txt
```

## AWS
```bash
# Creating Bucket
aws s3api create-bucket \
     --bucket 'nth-dev-datalake' \
     --region 'us-east-1'
     
# Copying our dataset to S3
aws s3 cp data/raw/users s3://nth-dev-datalake/raw/users/ --recursive

# Copying our script to S3
aws s3 cp main.py s3://nth-dev-datalake/jobs/aws-emr-app/

# Checking...
aws s3 ls s3://nth-dev-datalake/

# TODO: Create Cluster

```

```bash
spark-submit --master local main.py trusted --date 2021-04-09 --bucket data
spark-submit --master local main.py refined --bucket data

```

---

 - [Medium: EMR in 15 Minutes](https://medium.com/big-data-on-amazon-elastic-mapreduce/run-a-spark-job-within-amazon-emr-in-15-minutes-68b02af1ae16)