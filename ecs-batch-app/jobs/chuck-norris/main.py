import json
import logging as log
from argparse import ArgumentParser
from datetime import datetime
from os import environ
from random import choice
from time import sleep
from uuid import uuid4

import requests
from boto3 import Session


def init_log():
    log.basicConfig(
        format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=log.INFO
    )


def init_session():
    return Session(
        aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=environ.get('AWS_REGION'),
    )


def get_args():
    parser = ArgumentParser(description='Job - Chuck Norris')
    parser.add_argument('-p', dest='pipeline', required=True, choices=['extract', 'show'], help='Job Pipeline')
    parser.add_argument('-b', dest='bucket', default='nth-dev-datalake', help='S3 Bucket')
    parser.add_argument('-o', dest='output_path', default='sandbox/jokes', help='Output path inside bucket.')
    parser.add_argument('--api-url', default='https://api.chucknorris.io/jokes/random', help='API URL')
    parser.add_argument('--api-sleep', default=1, type=int, help='API Request Interval (Seconds)')
    parser.add_argument('--api-requests', default=10, type=int, help='How many requests?')
    return parser.parse_args()


def save(session, bucket, path, data):
    if data:
        time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        file_path = f'{path}/{time}-{uuid4()}.json'
        log.info(f'Writing file "s3://{bucket}/{file_path}"')
        client = session.client('s3')
        client.put_object(
            Body=bytes(json.dumps(data, ensure_ascii=False), 'utf8'),
            Bucket=bucket,
            Key=file_path
        )


def request(url):
    data = requests.get(url).json()
    if data:
        data['created_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    log.info(f'Response Data: {data}')
    return data


def exec_extraction(args):
    session = init_session()
    how_many = args.api_requests
    log.info(f'Starting {how_many} executions...')
    for i in range(how_many):
        count = f'({i + 1}/{how_many})'
        log.info(f'{count} Requesting data...')
        data = request(args.api_url)

        log.info(f'{count} Saving data...')
        save(session, args.bucket, args.output_path, data)

        log.info(f'{count} Done!')
        sleep(args.api_sleep)


def exec_show(args):
    session = init_session()
    client = session.client('s3')

    log.info(f'Listing bucket "s3://{args.bucket}/{args.output_path}"')
    files = client.list_objects(Bucket=args.bucket, Prefix=args.output_path).get('Contents')
    log.info(f'{len(files)} files found!')

    random_joke = choice(files)
    data = client.get_object(Bucket=args.bucket, Key=random_joke.get('Key'))
    data = json.loads(data['Body'].read().decode('utf8'))
    log.info(f'Joke: "{data.get("value")}"')
    log.info(f'Created At: "{data.get("created_at")}"')


def main(args):
    log.info(f'Env: {environ.get("APP_ENV", "unknown")}')
    log.info(f'Args: {args}')
    if args.pipeline.strip().lower() == 'extract':
        exec_extraction(args)
    else:
        exec_show(args)


if __name__ == '__main__':
    init_log()
    main(get_args())
