FROM python:3.7

# Docker Args
ARG ACCESS_KEY='default'
ARG SECRET_KEY='default'
ARG REGION='us-east-1'

# AWS Credentials
ENV AWS_ACCESS_KEY_ID="$ACCESS_KEY"
ENV AWS_SECRET_ACCESS_KEY="$SECRET_KEY"
ENV AWS_REGION="$REGION"

# Airflow Config
ENV AIRFLOW_HOME='/airflow'
ENV AIRFLOW__CORE__LOAD_EXAMPLES='False'

WORKDIR $AIRFLOW_HOME

RUN pip install -q apache-airflow[aws]==2.1.2 \
    --constraint 'https://raw.githubusercontent.com/apache/airflow/constraints-2.1.2/constraints-3.7.txt'

# Remove Web App Login
RUN printf "\nAUTH_ROLE_PUBLIC = 'Admin'\n" >> webserver_config.py
RUN printf "\n[webserver]\n" >> airflow.cfg
RUN printf "rbac = False\n" >> airflow.cfg
RUN printf "authenticate = False\n" >> airflow.cfg

# Init Services
ADD config ./config

CMD /bin/bash $AIRFLOW_HOME/config/init.sh
