from pyspark.sql import SparkSession

from src.utils import log

RAW_PATH = 'raw/users'
TRUSTED_PATH = 'trusted/users'


def run(spark: SparkSession, **kwargs):
    bucket, dt_partition = kwargs['bucket'], kwargs['dt_partition']
    raw_file = f'{bucket}/{RAW_PATH}/{dt_partition}'
    log.info(f'Reading file "{raw_file}"')
    df = spark.read \
        .option('header', True) \
        .option('inferSchema', True) \
        .option('sep', ',') \
        .csv(raw_file) \
        .cache()

    log.info(f'Records found: {df.count()}')
    df.printSchema()
    df.show()

    log.info(f'Writing to "{bucket}/{TRUSTED_PATH}"')
    df.write \
        .mode('append') \
        .partitionBy('user_id') \
        .parquet(f'{bucket}/{TRUSTED_PATH}')
