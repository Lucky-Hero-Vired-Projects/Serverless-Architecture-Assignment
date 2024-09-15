#  Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3

## Steps:
1. Create a Lambda Function with IMA policy __AmazonS3ReadOnlyAccess__ with given python code
2. Create multiple buckets.
3. Manully trigger the lambda function
![screenshot-1](./screenshots/lambda-execution.png)
4. Cloudwatch logs for multiple executions
![screenshot-2](./screenshots/cloudwatch-logs-0.png)
![screenshot-2](./screenshots/cloudwatch-logs-1.png)
![screenshot-2](./screenshots/cloudwatch-logs-2.png)