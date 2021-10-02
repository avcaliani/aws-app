from os import environ

__LOCAL = {
    'raw_path': '{}/raw/user_score/{}',
    'trusted_path': 'file://{}/trusted/user_score'
}

__AWS = {
    'raw_path': 's3a://{}/raw/user_score',
    'trusted_path': 's3a://{}/trusted/user_score'
}


def get(key):
    env = environ.get('APP_ENV', 'unknown').lower().strip()
    key = key.lower().strip()
    if env == 'local':
        return __LOCAL[key]
    elif env == 'aws':
        return __AWS[key]
    else:
        raise RuntimeError(f'Environment "{env}" not found! Valid envs: local, aws')


def hudi_options(table, key_col, increment_col, partition_col):
    return {
        'hoodie.table.name': table,
        'hoodie.datasource.write.recordkey.field': key_col,
        # The partition path is not required, BUT! BE CAREFUL!
        # I found some interesting Hudi behaviors because of this field.
        #  1 - When you don't specify a partition field a "default"
        #      directory will be created inside the path you pass.
        #  2 - In my case, I want a single record for each user.
        #      When I defined as partition field a field with year and month
        #      I found the SAME USER in DIFFERENT PARTITIONS. To solve this
        #      I had to define the user_id as partition, then I finally
        #      had a single record for user.
        'hoodie.datasource.write.partitionpath.field': partition_col,
        'hoodie.datasource.write.table.name': table,
        'hoodie.datasource.write.operation': 'upsert',
        'hoodie.datasource.write.precombine.field': increment_col,
        'hoodie.upsert.shuffle.parallelism': 2,
        'hoodie.insert.shuffle.parallelism': 2
    }
