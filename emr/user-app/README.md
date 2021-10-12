# AWS - EMR App

By Anthony Vilarim Caliani

![#](https://img.shields.io/badge/licence-MIT-lightseagreen.svg) ![#](https://img.shields.io/badge/python-3.9.x-yellow.svg)

Spark Batch application with Apache Hudi.

## Quick Start

```bash
python -m venv .venv \
    && source .venv/bin/activate \
    && pip install -r requirements-dev.txt
```

## AWS

```bash
# Creating Bucket
aws s3api create-bucket \
     --bucket 'nth-dev-datalake' \
     --region 'us-east-1'
     
# Copying dataset to S3
aws s3 cp data/raw/user_score s3://nth-dev-datalake/raw/user_score/ --recursive

# Deploying Spark Job
# Arg 01 - App Version
# Arg 02 - Replace if exists? [ yes | no ] (default: no)
./devops/scripts/deploy.sh 0.0.1-beta yes
```

```bash
devops/scripts/run.sh 'trusted' --date '2021-04-09' --bucket "$(pwd)/data" --overwrite
devops/scripts/run.sh 'info' --bucket "$(pwd)/data"
```

---

- [Medium: EMR in 15 Minutes](https://medium.com/big-data-on-amazon-elastic-mapreduce/run-a-spark-job-within-amazon-emr-in-15-minutes-68b02af1ae16)
- [Apache Hudi: Quick Start](https://hudi.apache.org/docs/quick-start-guide)
- [How To: Airflow + AWS EMR](https://www.startdataengineering.com/post/how-to-submit-spark-jobs-to-emr-cluster-from-airflow/)
