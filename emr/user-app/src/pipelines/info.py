from src import constants
from src.utils import log


def run(spark, bucket):
    path = constants.get('trusted_path').format(bucket)
    log.info('----------------< info >----------------')
    log.info(f'Path {path}')
    df = spark.read.format("hudi").load(path).cache()
    log.info(f'Records: {df.count()}')
    df.printSchema()

    log.info(f'HUDI Fields')
    df.select([col for col in df.columns if col.startswith('_')]).show(truncate=False)

    log.info(f'My Fields')
    df.select([col for col in df.columns if not col.startswith('_')]).show(truncate=False)
