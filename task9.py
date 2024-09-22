import boto3
from datetime import datetime, timezone, timedelta

# Initialize S3 client
s3 = boto3.client('s3')

# Define the age threshold (6 months) for moving files to Glacier
MONTHS_THRESHOLD = 6

# S3 bucket name
BUCKET_NAME = 'your-s3-bucket-name'

def lambda_handler(event, context):
    try:
        # Get the current time in UTC
        current_time = datetime.now(timezone.utc)
        
        # Calculate the time threshold for moving files to Glacier (6 months ago)
        time_threshold = current_time - timedelta(days=MONTHS_THRESHOLD * 30)

        # List objects in the specified bucket
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)

        # Check if the bucket is empty
        if 'Contents' not in response:
            print(f"No objects found in bucket: {BUCKET_NAME}")
            return {
                'statusCode': 200,
                'body': f"Bucket {BUCKET_NAME} is empty. No objects found for archival."
            }
        
        archived_files = []

        # Iterate over each object in the bucket
        for obj in response['Contents']:
            obj_key = obj['Key']
            obj_last_modified = obj['LastModified']

            # If the object is older than the threshold, move it to Glacier
            if obj_last_modified < time_threshold:
                print(f"Archiving {obj_key} (Last Modified: {obj_last_modified})")
                
                # Change the storage class to Glacier
                s3.copy_object(
                    Bucket=BUCKET_NAME,
                    Key=obj_key,
                    CopySource={'Bucket': BUCKET_NAME, 'Key': obj_key},
                    StorageClass='GLACIER'
                )
                
                archived_files.append(obj_key)
        
        # Return appropriate response based on whether files were archived
        if archived_files:
            print(f"Archived files: {archived_files}")
            return {
                'statusCode': 200,
                'body': f"Archived files to Glacier: {archived_files}"
            }
        else:
            print("No files older than 6 months found.")
            return {
                'statusCode': 200,
                'body': "No files older than 6 months found in the bucket."
            }
    
    except Exception as e:
        # Handle any errors and return an error message
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"An error occurred: {str(e)}"
        }
