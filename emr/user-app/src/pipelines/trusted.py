import json

from pyspark.sql import functions as f

from src import constants
from src.utils import log

HUDI_TABLE = 'user_score'
HUDI_KEY_COL = 'user_id'
HUDI_INCREMENT_COL = 'updated_at'


def _read(spark, bucket, exec_date):
    log.info('=~=~=~=~=~=~=~=~=~= READ =~=~=~=~=~=~=~=~=~=')
    path = constants.get('raw_path').format(bucket, exec_date)
    log.info(f'File: {path}')
    df = spark.read.json(path).cache()
    log.info(f'Records: {df.count()}')
    df.printSchema()
    return df


def _write(df, bucket, overwrite):
    log.info('=~=~=~=~=~=~=~=~=~= WRITE =~=~=~=~=~=~=~=~=~=')
    path = constants.get('trusted_path').format(bucket)
    hudi_opts = constants.hudi_options(
        table=HUDI_TABLE,
        key_col=HUDI_KEY_COL,
        increment_col=HUDI_INCREMENT_COL
    )
    log.info(f'File: {path}')
    log.info(f'Overwrite: {overwrite}')
    log.info(f'Records: {df.count()}')
    log.info(f'HUDI Opts: {json.dumps(hudi_opts, indent=2, ensure_ascii=False)}')
    df.printSchema()
    df.show()
    df.write \
        .format("hudi") \
        .options(**hudi_opts) \
        .mode('overwrite' if overwrite else 'append') \
        .save(path)
    return df


def run(spark, **kwargs):
    bucket, overwrite = kwargs['bucket'], kwargs['overwrite']
    df = _read(spark, bucket, kwargs['exec_date'])
    df = df.withColumn('processed_at', f.current_timestamp()) \
        .withColumn('updated_at', f.to_timestamp('updated_at', 'yyyy-MM-dd HH:mm:ss')) \
        .withColumn('yy_mm', f.date_format('updated_at', 'yyyy-MM'))

    _write(df, bucket, overwrite)
