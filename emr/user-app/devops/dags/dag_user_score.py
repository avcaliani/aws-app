from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.amazon.aws.operators.emr_add_steps import EmrAddStepsOperator
from airflow.providers.amazon.aws.operators.emr_create_job_flow import EmrCreateJobFlowOperator
from airflow.providers.amazon.aws.operators.emr_terminate_job_flow import EmrTerminateJobFlowOperator
from airflow.providers.amazon.aws.sensors.emr_step import EmrStepSensor

# https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/emr.html#create-emr-job-flow-with-manual-steps
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#id65

SCHEDULE = '@once'
TAGS = ['emr', 'spark', 'user-score']
ARGS = {
    'owner': 'anthony',
    'description': 'User Score Pipeline',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email': ['anthony@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/emr.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.run_job_flow
JOB_FLOW_OVERRIDES = {
    "Name": "nth-cluster",
    "ReleaseLabel": "emr-6.4.0",
    "LogUri": "s3://nth-dev-datalake/logs/emr",
    "Applications": [{"Name": "Spark"}],  # We want our EMR cluster to have HDFS and Spark {"Name": "Hadoop"},
    "Configurations": [
        {
            "Classification": "spark-env",
            "Configurations": [
                {
                    "Classification": "export",
                    "Properties": {
                        "PYSPARK_PYTHON": "/usr/bin/python3",  # Just in case :)
                        "APP_ENV": "aws",  # My Env variable
                    },
                }
            ],
        }
    ],
    "Instances": {
        "InstanceGroups": [
            {
                "Name": "Master Node",
                "Market": "SPOT",  # ON_DEMAND | SPOT
                "InstanceRole": "MASTER",
                "InstanceType": "m5.xlarge",
                "InstanceCount": 1,
            },
            # {
            #     "Name": "Core - 2",
            #     "Market": "ON_DEMAND",
            #     "InstanceRole": "CORE",
            #     "InstanceType": "m1.small",
            #     "InstanceCount": 1,
            # },
        ],
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False,  # this lets us programmatically terminate the cluster
    },
    "JobFlowRole": "EMR_EC2_DefaultRole",
    "ServiceRole": "EMR_DefaultRole",
    'StepConcurrencyLevel': 1,
}

SPARK_STEPS = [  # Note the params values are supplied to the operator
    {
        'Name': 'calculate-pi',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': ['/usr/lib/spark/bin/run-example', 'SparkPi', '10'],
        },
    },
    {
        "Name": "user-score_trusted",
        "ActionOnFailure": "CONTINUE",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": [
                "spark-submit",
                "--deploy-mode",
                "client",
                "--packages",
                "org.apache.hudi:hudi-spark3-bundle_2.12:0.9.0,org.apache.spark:spark-avro_2.12:3.0.1",
                "--py-files",
                "s3://{{ params.BUCKET_NAME }}/jobs/user-app/{{ params.APP_VERSION }}/src.zip",
                "s3://{{ params.BUCKET_NAME }}/jobs/user-app/{{ params.APP_VERSION }}/main.py",
                "trusted",
                "--date",
                "2021-04-09",
                "--bucket",
                "{{ params.BUCKET_NAME }}",
            ],
        },
    },
    {
        "Name": "user-score_info",
        "ActionOnFailure": "CONTINUE",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": [
                "spark-submit",
                "--deploy-mode",
                "client",
                "--packages",
                "org.apache.hudi:hudi-spark3-bundle_2.12:0.9.0,org.apache.spark:spark-avro_2.12:3.0.1",
                "--py-files",
                "s3://{{ params.BUCKET_NAME }}/jobs/user-app/{{ params.APP_VERSION }}/src.zip",
                "s3://{{ params.BUCKET_NAME }}/jobs/user-app/{{ params.APP_VERSION }}/main.py",
                "info",
                "--bucket",
                "{{ params.BUCKET_NAME }}",
            ],
        },
    },
]

with DAG('dag-user-score', schedule_interval=SCHEDULE, default_args=ARGS, catchup=False, tags=TAGS) as dag:
    start = DummyOperator(
        task_id='start'
    )
    """
    What is this macro? 
        This macro is the same as "create_cluster.output", but it doesn't create a direct
        connection to the other operators. 
    
    Why did I choose to use it instead of "create_cluster.output"?
        When you use "create_cluster.output" at "job_flow_id" Airflow will create
        a direct connection between the operators, and it will impact directly in my DAG
        workflow. In this example, this "create_cluster.output" approach was not 
        the best option, but it may be a good option for you in another context.
    """
    cluster_id = "{{ task_instance.xcom_pull(task_ids='create-cluster', key='return_value') }}"
    create_cluster = EmrCreateJobFlowOperator(
        task_id="create-cluster",
        job_flow_overrides=JOB_FLOW_OVERRIDES,
        aws_conn_id="aws_default",
        emr_conn_id="emr_default",
    )

    """
    This operator will add Spark Jobs to the cluster queue.
    Obs.: Job Flow ID is the same of Cluster ID.
    """
    add_steps = EmrAddStepsOperator(
        task_id="add-steps",
        job_flow_id=cluster_id,
        aws_conn_id="aws_default",
        steps=SPARK_STEPS,
        params={  # these params are used to fill the paramterized values in SPARK_STEPS json
            "BUCKET_NAME": 'nth-dev-datalake',
            "APP_VERSION": '0.0.1-beta',
        },
    )

    # Wait for the steps to complete
    step_watchers = []
    for i in range(0, len(SPARK_STEPS)):
        step = SPARK_STEPS[i]
        step_watchers.append(
            EmrStepSensor(
                task_id=f"step-{step['Name']}",
                job_flow_id=cluster_id,
                step_id="{{ task_instance.xcom_pull(task_ids='add-steps', key='return_value')[" + str(i) + "] }}",
                aws_conn_id="aws_default",
            )
        )

    # Terminate the EMR cluster
    terminate_cluster = EmrTerminateJobFlowOperator(
        task_id="terminate-cluster",
        job_flow_id=cluster_id,
        aws_conn_id="aws_default",
        trigger_rule='none_skipped',
    )
    the_end = DummyOperator(
        task_id='the-end'
    )
    start >> create_cluster >> add_steps >> step_watchers >> terminate_cluster >> the_end
