import boto3
import json
from datetime import datetime

# Define your tag keys outside the function
VISH_AUTOSTART_TAG = 'Vish-AutoStart'
VISH_AUTOSTOP_TAG = 'Vish-AutoStop'

# Initialize EC2 client
ec2 = boto3.client('ec2')

def find_instances_by_tag(tag_key, desired_state):
    """Function to find EC2 instances by tag and state."""
    instances = []
    
    # Fetch all EC2 instances
    response = ec2.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            
            # Get tags for the instance
            tags = instance.get('Tags', [])
            
            # Check if the instance has the specified tag and is in the desired state
            if any(tag['Key'] == tag_key for tag in tags):
                if state == desired_state:
                    instances.append(instance_id)

    return instances


def stop_instances(instances):
    """Function to stop EC2 instances."""
    if instances:
        print(f"Stopping instances: {instances}")
        ec2.stop_instances(InstanceIds=instances)


def start_instances(instances):
    """Function to start EC2 instances."""
    if instances:
        print(f"Starting instances: {instances}")
        ec2.start_instances(InstanceIds=instances)


def lambda_handler(event, context):
    try:
        # Find instances to stop and start based on their tags
        vish_autostop_instances = find_instances_by_tag(VISH_AUTOSTOP_TAG, 'running')
        vish_autostart_instances = find_instances_by_tag(VISH_AUTOSTART_TAG, 'stopped')

        # Stop and start the instances
        stop_instances(vish_autostop_instances)
        start_instances(vish_autostart_instances)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'stopped_instances': vish_autostop_instances,
                'started_instances': vish_autostart_instances
            })
        }
    
    except Exception as e:
        # Handle any errors and return an error message
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"An error occurred: {str(e)}"
        }
