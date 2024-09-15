import boto3
from datetime import datetime, timezone, timedelta

# Initialize the S3 client
s3 = boto3.client('s3')

# Set the number of days for the cleanup
DAYS_TO_KEEP = 30

def lambda_handler(event, context):
    # Define the bucket name
    bucket_name = 'task2-assignment'

    # Get the current time
    current_time = datetime.now(timezone.utc)
    
    # Calculate the cutoff time
    cutoff_time = current_time - timedelta(days=DAYS_TO_KEEP)

    # List all the objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Check if the bucket contains objects
    if 'Contents' not in response:
        return {
            'statusCode': 200,
            'body': f'No objects found in bucket {bucket_name}'
        }

    # List to store the files that will be deleted
    files_to_delete = []

    # Loop through all the objects in the bucket
    for obj in response['Contents']:
        # Get the last modified date of the object
        last_modified = obj['LastModified']

        # Check if the object is older than 30 days
        if last_modified < cutoff_time:
            # Add the object's key to the list of files to delete
            files_to_delete.append({'Key': obj['Key']})

    # If there are files to delete, proceed
    if files_to_delete:
        # Print the names of the files to delete for logging
        print(f'Files to be deleted: {[file["Key"] for file in files_to_delete]}')

        # Delete the files
        delete_response = s3.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': files_to_delete
            }
        )
        
        # Return a success message with deleted files
        return {
            'statusCode': 200,
            'body': f'Successfully deleted {len(files_to_delete)} files from {bucket_name}.'
        }
    else:
        return {
            'statusCode': 200,
            'body': f'No files older than {DAYS_TO_KEEP} days found in bucket {bucket_name}.'
        }
