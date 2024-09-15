import boto3

# Initialize S3 client using boto3
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # List all the S3 buckets in the account
    buckets = s3.list_buckets()

    # List to store unencrypted bucket names
    unencrypted_buckets = []

    # Loop through each bucket and check encryption status
    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        try:
            # Attempt to retrieve bucket's encryption settings
            encryption = s3.get_bucket_encryption(Bucket=bucket_name)
            rules = encryption['ServerSideEncryptionConfiguration']['Rules']
            print(f'Bucket "{bucket_name}" is encrypted: {rules}')
        except s3.exceptions.ClientError as e:
            # If encryption is not found, mark the bucket as unencrypted
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                unencrypted_buckets.append(bucket_name)
                print(f'Bucket "{bucket_name}" does not have encryption.')

    # Log and return the list of unencrypted buckets
    if unencrypted_buckets:
        print(f'Unencrypted buckets: {unencrypted_buckets}')
    else:
        print('All buckets are encrypted.')

    # Return the result
    return {
        'statusCode': 200,
        'body': f'Unencrypted buckets: {unencrypted_buckets if unencrypted_buckets else "None"}'
    }
