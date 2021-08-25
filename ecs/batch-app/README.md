# AWS - ECS Batch App

By Anthony Vilarim Caliani

![#](https://img.shields.io/badge/license-MIT-lightseagreen.svg)
![#](https://img.shields.io/badge/python-3.9.x-yellow.svg)

This is my AWS ECS Batch PoC.

## Quick Start

### AWS
```bash
# Bucket
aws s3api create-bucket \
  --bucket 'nth-dev-datalake' \
  --region 'us-east-1'

# Then create you project Stack based on devops/cloud-formation template.
```

### Development Environment

```bash
# Virtual Env.
python3 -m venv .venv \
  && source .venv/bin/activate \
  && pip install -r jobs/chuck-norris/requirements.txt

python jobs/chuck-norris/main.py -h
```

```bash
# Building Docker Image  
docker build -t nth/dev-chuck-norris .

# [optional] Scanning our image to check vulnerabilities.
docker scan nth/dev-chuck-norris

# ATTENTION!
# Check push commands at AWS Console (ECR Service).
```

> After the execution check **your AWS bucket**.

### Related Links

 - [Tutorial: Airflow Parallel Tasks](https://headspring.com/2020/06/17/airflow-parallel-tasks/)
 - [Airflow: ECS Example](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_modules/airflow/providers/amazon/aws/example_dags/example_ecs_fargate.html)
 - [Medium - How to create cloud formation stack](https://medium.com/workfall/how-can-we-deploy-aws-resources-with-ease-using-aws-cloudformation-templates-d10a811c5819)

---
<span style="color:gray">
🧙‍♂️ "If in doubt Meriadoc, always follow your nose." - Gandalf
</span>
