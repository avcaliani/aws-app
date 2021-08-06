FROM python:3.9-alpine

# Docker Args
ARG ACCESS_KEY=default
ARG SECRET_KEY=default

# AWS Credentials
ENV AWS_ACCESS_KEY_ID=$ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=$SECRET_KEY

# Project Workdir
WORKDIR /app

# Adding Project Files
ADD *.py .
ADD *.txt .

# Installing Project Dependencies
RUN pip install -q -r requirements.txt

# Execution command should be defined on the fly ;)
