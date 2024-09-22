import boto3
from datetime import datetime, timezone, timedelta

# Initialize S3 client
s3 = boto3.client('s3')

DAYS_THRESHOLD = 30

# S3 bucket name
BUCKET_NAME = 'vish-devops7'

def lambda_handler(event, context):
    try:
        # current time
        current_time = datetime.now(timezone.utc)
        
        # get time differecne from 30
        time_threshold = current_time - timedelta(days=DAYS_THRESHOLD)

        # get all objects from s3
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)

        # handle if bucket is empty
        if 'Contents' not in response:
            print(f"No objects found in bucket: {BUCKET_NAME}")
            return {
                'statusCode': 200,
                'body': f"Bucket {BUCKET_NAME} is empty. No objects found for deletion."
            }
        
        deleted_files = []

        # for each project in the bucket
        for obj in response['Contents']:
            obj_key = obj['Key']
            obj_last_modified = obj['LastModified']

            # If the object is older than the threshold, delete it
            if obj_last_modified < time_threshold:
                print(f"Deleting {obj_key} (Last Modified: {obj_last_modified})")
                s3.delete_object(Bucket=BUCKET_NAME, Key=obj_key)
                deleted_files.append(obj_key)
        
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
