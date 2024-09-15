import boto3
import datetime

# Initialize a boto3 EC2 client
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Get the volume ID from the event
    volume_id = event['volume_id']
    retention_days = event.get('retention_days', 30)

    # Create a snapshot for the specified EBS volume
    snapshot = ec2.create_snapshot(VolumeId=volume_id, Description='Automated EBS Snapshot')
    print(f'Snapshot created: {snapshot["SnapshotId"]}')

    # List snapshots for the specified volume
    snapshots = ec2.describe_snapshots(Filters=[{'Name': 'volume-id', 'Values': [volume_id]}])['Snapshots']
    
    # Get the current time in UTC
    now = datetime.datetime.now(datetime.timezone.utc)
    
    # Delete snapshots older than 30 days
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        snapshot_date = snapshot['StartTime']  # Snapshot StartTime is timezone-aware
        
        # Compare snapshot date with 30 days ago
        if snapshot_date < now - datetime.timedelta(days=retention_days):
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f'Snapshot deleted: {snapshot_id}')
        else:
            print(f'Snapshot {snapshot_id} is within the retention period.')

    return 'EBS snapshot creation and cleanup complete.'
