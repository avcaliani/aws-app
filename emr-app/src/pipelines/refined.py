from pyspark.sql import SparkSession
from pyspark.sql import functions as f

from src.utils import log

TRUSTED_PATH = 'trusted/users'
REFINED_PATH = 'refined/users'


def run(spark: SparkSession, **kwargs):
    bucket = kwargs['bucket']
    trusted_file = f'{bucket}/{TRUSTED_PATH}'
    log.info(f'Reading file "{trusted_file}"')
    df = spark.read \
        .parquet(trusted_file) \
        .groupBy('user_id') \
        .agg(f.mean('score').alias('mean_score'),
             f.max('date').alias('last_update')) \
        .cache()

    df.printSchema()
    df.show()

    refined_file = f'{bucket}/{REFINED_PATH}'
    log.info(f'Writing to "{refined_file}"')
    df.write \
        .mode('overwrite') \
        .parquet(refined_file)
