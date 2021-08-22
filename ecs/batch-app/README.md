# AWS - ECS Batch App

By Anthony Vilarim Caliani

![#](https://img.shields.io/badge/license-MIT-lightseagreen.svg)
![#](https://img.shields.io/badge/python-3.9.x-yellow.svg)

This is my AWS ECS Batch PoC.

## Quick Start

```
# TODO:
 - DevOps: Basic Automation Scripts.
 - Doc: Update + Add Screenshots.
 - AWS: Clean Up
```

### AWS
```bash
# Bucket
aws s3api create-bucket \
  --bucket 'nth-dev-datalake' \
  --region 'us-east-1'
```

### Development Environment

```bash
# Virtual Env.
python3 -m venv .venv \
  && source .venv/bin/activate \
  && pip install -r jobs/chuck-norris/requirements.txt \
  && pip install -r airflow/requirements.txt

python jobs/chuck-norris/main.py -h
```

```bash
# Docker
docker-compose build \
  --build-arg ACCESS_KEY=$(cat ~/.aws/credentials | grep key_id | sed 's/.*key_id.*= //') \
  --build-arg SECRET_KEY=$(cat ~/.aws/credentials | grep secret | sed 's/.*secret.*= //') \
  airflow
  
docker-compose build chuck-norris

# [optional]
docker scan nth/chuck-norris

# ATTENTION!
# Check push commands at AWS Console.

# To change execution params, update "command" at 'docker-compose.yml'
docker-compose up -d


```

> After the execution check **your AWS bucket**.

### Related Links

- [AWS - Batch Service Tutorial](https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/)

---
<span style="color:gray">
🧙‍♂️ "If in doubt Meriadoc, always follow your nose." - Gandalf
</span>
