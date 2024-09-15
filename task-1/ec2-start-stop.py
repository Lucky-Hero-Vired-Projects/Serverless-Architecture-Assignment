import boto3

class EC2InstanceManager:
    # Initilize the boto client for ec2
    def __init__(self):
        self.ec2 = boto3.client('ec2')
    
    def get_instances_by_tag(self, tag_name, tag_value='TRUE'):
        response = self.ec2.describe_instances(
            Filters=[
                {
                    'Name': [tag_name],
                    'Values': [tag_value]
                }
            ]
        )
        instance_ids = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])
        return instance_ids

    def stop_instances(self, instance_ids):
        if instance_ids:
            print(f'Stopping instances: {instance_ids}')
            self.ec2.stop_instances(InstanceIds=instance_ids)

    def start_instances(self, instance_ids):
        if instance_ids:
            print(f'Starting instances: {instance_ids}')
            self.ec2.start_instances(InstanceIds=instance_ids)

    def manage_instances(self, action):
        if action == 'start':
            instances = self.get_instances_by_tag('Auto-Start')
            for instance in instances:
                response = self.ec2.describe_instances(InstanceIds=[instance])
                instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
                if instance_state == 'running':
                    print(f'Instance {instance} is already running.')
                else:
                    self.start_instances([instance])
                    print(f'Lambda is starting instance {instance}.')
            return f'Successfully started instances: {instances}'
        elif action == 'stop':
            instances = self.get_instances_by_tag('Auto-Stop')
            for instance in instances:
                response = self.ec2.describe_instances(InstanceIds=[instance])
                instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
                if instance_state == 'stopped':
                    print(f'Instance {instance} is already stopped.')
                else:
                    self.stop_instances([instance])
                    print(f'Lambda is stopping instance {instance}.')
            return f'Successfully stopped instances: {instances}'
        else:
            return f'Invalid action provided: {action}'

def lambda_handler(event, context):
    # Extract action from the test event (this will be passed when invoking the Lambda function)
    action = list(event.keys())[0]

    if action not in ['Auto-Start', 'Auto-Stop']:
        return {
            'statusCode': 400,
            'body': f'Error: Invalid action "{action}". Must be "Auto-Start" or "Auto-Stop".'
        }

    # Create an instance of the EC2InstanceManager class
    ec2_manager = EC2InstanceManager()

    # Trigger the action (start or stop)
    if action == 'Auto-Start':
        result_message = ec2_manager.manage_instances('start')
    elif action == 'Auto-Stop':
        result_message = ec2_manager.manage_instances('stop')
    
    return {
        'statusCode': 200,
        'body': result_message
    }