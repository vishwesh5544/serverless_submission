import boto3
from datetime import datetime, timezone, timedelta

# Initialize S3 client
s3 = boto3.client('s3')

# Define constants
DAYS_THRESHOLD = 30
BUCKET_NAME = 'vish-devops7'


def get_time_threshold(days_threshold):
    """Calculate the time threshold based on the number of days."""
    current_time = datetime.now(timezone.utc)
    return current_time - timedelta(days=days_threshold)


def list_objects_in_bucket(bucket_name):
    """List objects in the specified S3 bucket."""
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' not in response:
        print(f"No objects found in bucket: {bucket_name}")
        return None
    return response['Contents']


def delete_old_files(bucket_name, objects, time_threshold):
    """Delete files in the S3 bucket older than the time threshold."""
    deleted_files = []
    
    for obj in objects:
        obj_key = obj['Key']
        obj_last_modified = obj['LastModified']
        
        # Check if the object is older than the threshold
        if obj_last_modified < time_threshold:
            print(f"Deleting {obj_key} (Last Modified: {obj_last_modified})")
            s3.delete_object(Bucket=bucket_name, Key=obj_key)
            deleted_files.append(obj_key)
    
    return deleted_files


def lambda_handler(event, context):
    try:
        # Get the time threshold for 30 days ago
        time_threshold = get_time_threshold(DAYS_THRESHOLD)

        # List all objects in the bucket
        objects = list_objects_in_bucket(BUCKET_NAME)
        
        # Handle empty bucket
        if objects is None:
            return {
                'statusCode': 200,
                'body': f"Bucket {BUCKET_NAME} is empty. No objects found for deletion."
            }
        
        # Delete old files and get the list of deleted files
        deleted_files = delete_old_files(BUCKET_NAME, objects, time_threshold)
        
        # Return the deleted files data
        if deleted_files:
            print(f"Deleted files: {deleted_files}")
            return {
                'statusCode': 200,
                'body': f"Deleted files: {deleted_files}"
            }
        else:
            print("No files older than 30 days found.")
            return {
                'statusCode': 200,
                'body': "No files older than 30 days found in the bucket."
            }
    
    except Exception as e:
        # Handle any errors and return an error message
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"An error occurred: {str(e)}"
        }
