from argparse import ArgumentParser

from pyspark.sql import SparkSession


def init_spark():
    spark = SparkSession.builder \
        .appName('aws-emr-app') \
        .getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')
    return spark


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input-file', required=True, help='Input File')
    parser.add_argument('-o', '--output-file', required=True, help='Output Path')
    return parser.parse_args()


def main():
    args, spark = get_args(), init_spark()
    print(f'Args: {args}')
    print(f'Spark Version: {spark.version}')
    df = spark.read \
        .option('header', True) \
        .option('inferSchema', True) \
        .option('sep', ',') \
        .csv(args.input_file) \
        .cache()

    print(f'Records found: {df.count()}')
    df.printSchema()
    df.show()
    df.write \
        .mode('append') \
        .partitionBy('user_id') \
        .parquet(args.output_file)

    spark.stop()


if __name__ == '__main__':
    main()
