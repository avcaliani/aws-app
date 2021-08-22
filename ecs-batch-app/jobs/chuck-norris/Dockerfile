FROM python:3.9-alpine

# Project Workdir
WORKDIR /app

# Adding Project Files
ADD *.py .
ADD *.txt .

# Installing Project Dependencies
RUN pip install -q -r requirements.txt

# Execution command should be defined on the fly ;)
