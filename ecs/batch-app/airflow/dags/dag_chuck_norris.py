from datetime import datetime, timedelta
from typing import List, Dict, Any

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.providers.amazon.aws.operators.ecs import ECSOperator

ARGS = {
    'owner': 'anthony',
    'description': 'Chuck Norris Pipeline',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email': ['anthony@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@once',
}


def ecs_template(
        command: List[str],
        app_name: str = 'chuck-norris',
        container: str = 'main-container') -> Dict[str, Any]:
    """ECS Task Template.

    This method returns a dict that represents all configurations to be used in a ECS Task.
    For more task options, check boto3 docs at:
      - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html?highlight=run_task#ECS.Client.run_task

    About "chuck_norris_aws_config" variable. You have to configure the variable in Airflow using your own values.
    Here it is a variable value template for you:
      { "env": "dev", "region": "us-east-1", "subnet": "subnet-0x000", "security_group": "sg-0x000" }
    See: https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html

    :param command: Container execution parameter.
    :param app_name: App Name is the Stack Name, without environment prefix.
    :param container: Task Definition Container Name.
    :return:
        Dictionary with ECS Task configuration.
    """
    aws_config = Variable.get("chuck_norris_aws_config", deserialize_json=True)
    stack = f'{aws_config["env"]}-{app_name}'
    return {
        'aws_conn_id': 'aws_default',
        'region_name': aws_config['region'],
        'launch_type': 'FARGATE',
        'cluster': f'{stack}-cluster',
        'task_definition': f'{stack}-task',
        'network_configuration': {
            'awsvpcConfiguration': {
                'assignPublicIp': 'ENABLED',
                'subnets': [aws_config['subnet']],
                'securityGroups': [aws_config['security_group']],
            }
        },
        'awslogs_group': f'/ecs/log-group-{stack}',
        'awslogs_stream_prefix': f'{app_name}/{container}',
        'overrides': {
            'containerOverrides': [
                {
                    'name': container,
                    'memoryReservation': 128,
                    'command': command,
                },
            ],
        },
        'tags': {
            'team': 'GitHub - @avcaliani',
            'project': 'aws-app'
        },
    }


with DAG('chuck-norris', default_args=ARGS, catchup=False) as dag:
    app_initialize = DummyOperator(
        task_id='start'
    )
    app_extract = ECSOperator(
        task_id='app-extract',
        dag=dag,
        **ecs_template(
            command=['python', '/app/main.py', '-p', 'extract'],
        )
    )
    app_show = ECSOperator(
        task_id='app-show',
        dag=dag,
        **ecs_template(
            command=['python', '/app/main.py', '-p', 'show'],
        )
    )
    app_teardown = DummyOperator(
        task_id='teardown'
    )
    app_initialize >> app_extract >> app_show >> app_teardown
