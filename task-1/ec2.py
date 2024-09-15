import boto3
from botocore.config import Config

session = boto3.Session(profile_name='siri')

# Create an EC2 client using the session
ec2_client = session.client('ec2', region_name='us-west-2')  

# Function to create an EC2 instance with a specified tag
def create_ec2_instance(tag_key, tag_value):
    # Create EC2 instance
    instance = ec2_client.run_instances(
        ImageId='ami-0bfddf4206f1fa7b9',  
        InstanceType='t2.micro', 
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': tag_key,
                        'Value': tag_value
                    }
                ]
            }
        ]
    )
    instance_id = instance['Instances'][0]['InstanceId']
    print(f'Created EC2 instance {instance_id} with tag {tag_key}={tag_value}')
    return instance_id

# Create two instances with different tags
auto_stop_instance_id = create_ec2_instance('Auto-Stop', 'TRUE')
auto_start_instance_id = create_ec2_instance('Auto-Start', 'TRUE')

