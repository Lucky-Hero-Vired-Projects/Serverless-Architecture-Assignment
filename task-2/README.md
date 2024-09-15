# Automated S3 Bucket Cleanup Using AWS Lambda and Boto3


### Steps:
1. Manual Trigger the Lambda function with empty bucket (IAM Policy : __AmazonS3ReadOnlyAccess__)
![screenshot0](./screenshots/bucket-with-files.png)
![screenshot1](./screenshots/empty-bucket-lambda.png)
2. Upload any file in s3 bucket
![screenshot2](./screenshots/bucket-with-files.png)
3. Again trigger the lambda function 
![screenshot3](./screenshots/lambda-execution.png)