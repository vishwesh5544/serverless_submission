import boto3
from datetime import datetime, timezone, timedelta

# Initialize S3 client
s3 = boto3.client('s3')

# Define constants
DAYS_THRESHOLD = 90
BUCKET_NAME = 'vish-devops7'

def get_time_threshold(days_threshold):
    """Calculate the time threshold for log deletion based on the number of days."""
    current_time = datetime.now(timezone.utc)
    return current_time - timedelta(days=days_threshold)


def list_objects_in_bucket(bucket_name):
    """List objects (logs) in the specified S3 bucket."""
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' not in response:
        print(f"No objects found in bucket: {bucket_name}")
        return None
    return response['Contents']


def delete_old_logs(bucket_name, objects, time_threshold):
    """Delete logs in the S3 bucket older than the time threshold."""
    deleted_logs = []
    
    for obj in objects:
        obj_key = obj['Key']
        obj_last_modified = obj['LastModified']
        
        # Check if the log is older than the threshold
        if obj_last_modified < time_threshold:
            print(f"Deleting log {obj_key} (Last Modified: {obj_last_modified})")
            s3.delete_object(Bucket=bucket_name, Key=obj_key)
            deleted_logs.append(obj_key)
    
    return deleted_logs


def lambda_handler(event, context):
    try:
        # Get the time threshold for files older than 90 days
        time_threshold = get_time_threshold(DAYS_THRESHOLD)

        # List all logs in the bucket
        logs = list_objects_in_bucket(BUCKET_NAME)
        
        # Handle empty bucket
        if logs is None:
            return {
                'statusCode': 200,
                'body': f"Bucket {BUCKET_NAME} is empty. No logs found for deletion."
            }
        
        # Delete old logs and get the list of deleted logs
        deleted_logs = delete_old_logs(BUCKET_NAME, logs, time_threshold)
        
        # Return the deleted logs data
        if deleted_logs:
            print(f"Deleted logs: {deleted_logs}")
            return {
                'statusCode': 200,
                'body': f"Deleted logs: {deleted_logs}"
            }
        else:
            print("No logs older than 90 days found.")
            return {
                'statusCode': 200,
                'body': "No logs older than 90 days found in the bucket."
            }
    
    except Exception as e:
        # Handle any errors and return an error message
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"An error occurred: {str(e)}"
        }
