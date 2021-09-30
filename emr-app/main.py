from argparse import ArgumentParser, Namespace
from contextlib import contextmanager

from pyspark.sql import SparkSession

from src.pipelines import trusted, refined
from src.utils import Timer
from src.utils import log


def get_args() -> Namespace:
    parser = ArgumentParser(description='User Score Ingestion')
    parser.add_argument('pipeline', help='Pipeline name')
    parser.add_argument('--date', dest='dt_partition', help='Partition date as "yyyy-mm-dd"')
    parser.add_argument('--bucket', default='nth-dev-datalake', help='S3 Bucket')
    return parser.parse_args()


@contextmanager
def spark_session(pipeline: str):
    spark = SparkSession.builder \
        .appName(f'user-score_{pipeline}') \
        .getOrCreate()
    yield spark
    spark.stop()


def run(spark: SparkSession, args: Namespace) -> None:
    pipeline = args.pipeline.upper()
    if 'TRUSTED' == pipeline:
        trusted.run(spark, dt_partition=args.dt_partition, bucket=args.bucket)
    elif 'REFINED' == pipeline:
        refined.run(spark, bucket=args.bucket)
    else:
        raise RuntimeError(f'Pipeline "{pipeline}" does not exist!')


def main() -> None:
    args, timer = get_args(), Timer()
    with spark_session(args.pipeline) as spark:
        log.info(f'[APP] Args: {args}')
        run(spark, args)
        log.info(f'[APP] Elapsed Time: {timer.stop()}')


if __name__ == '__main__':
    main()
