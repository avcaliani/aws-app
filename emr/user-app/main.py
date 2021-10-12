import platform
from argparse import ArgumentParser, Namespace
from contextlib import contextmanager

from pyspark.sql import SparkSession

from src.pipelines import trusted, info
from src.utils import Timer
from src.utils import log


def get_args() -> Namespace:
    parser = ArgumentParser(description='User Score Ingestion')
    parser.add_argument('pipeline', help='Pipeline name')
    parser.add_argument('--date', dest='exec_date', help='Partition date as "yyyy-mm-dd"')
    parser.add_argument('--bucket', default='nth-dev-datalake', help='S3 Bucket name or absolute local path.')
    parser.add_argument('--overwrite', dest='overwrite', action='store_true', default=False)
    return parser.parse_args()


@contextmanager
def spark_session(pipeline: str):
    spark = SparkSession.builder \
        .appName(f'user-score_{pipeline}') \
        .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') \
        .getOrCreate()
    yield spark
    spark.stop()


def run(spark: SparkSession, args: Namespace) -> None:
    pipeline = args.pipeline.lower()
    if 'trusted' == pipeline:
        trusted.run(spark, exec_date=args.exec_date, bucket=args.bucket, overwrite=args.overwrite)
    elif 'info' == pipeline:
        info.run(spark, bucket=args.bucket)
    else:
        raise RuntimeError(f'Pipeline "{pipeline}" does not exist!')


def main() -> None:
    args, timer = get_args(), Timer()
    with spark_session(args.pipeline) as spark:
        log.info(f'[APP] Args: {args}')
        log.info(f'[APP] Spark Version: {spark.version}')
        log.info(f'[APP] Python Version.: {platform.python_version()}')
        run(spark, args)
        log.info(f'[APP] Elapsed Time: {timer.stop()}')


if __name__ == '__main__':
    main()
