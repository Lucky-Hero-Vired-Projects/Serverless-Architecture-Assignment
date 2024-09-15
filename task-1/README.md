# Automated Instance Management Using AWS Lambda and Boto3

## Steps:
1. Create ec2 instances using ec2.py file which can create 2 instance with tags Auto-Start and Auto-Stop and Key name. Value will be any. (IAM ROLE: __AmazonEC2FullAccess__)
![ec2.py file o/p](./screenshots/ec2.png)
2. Creating Lambda function where python is using boto3 module and fetch all instanceID's with tags Auto-start and Auto-stop based on condition.
3. When invoking manually, has to provide 
```
   { "Auto-Start" : "TRUE" }

   or

   { "Auto-Stop" : "TRUE" }
```
   when key is Auto-start, lambda function is checking all instance with tag and start those instance simmalary for Auto-Stop also.

 ![ec2-start](./screenshots/lambda-start.png)
 ![ec2-starting](./screenshots/ec2-starting.png)
 ![ec2-stop](./screenshots/lambda-stop.png)
 ![ec2-stoping](./screenshots/ec2-stoping.png)
 ![cloudwatch-logs](./screenshots/cloudwatch-logs.png)
