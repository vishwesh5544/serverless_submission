# serverless_submission
Solution to Graded Assignment On Serverless Architecture

## Prerequisites
- For this assignment, I have used the following IAM rles.
  ![image](https://github.com/user-attachments/assets/05531be4-16df-4e44-872a-f75e1b96106e)
  1. **Arpit-EC2FullAccess**:
     ![image](https://github.com/user-attachments/assets/b7fc3f88-c20a-4a05-aacc-9933ed5b1a05)
  2. **Arpit-S3FullAccess**:
     ![image](https://github.com/user-attachments/assets/6c81262c-5c10-4f88-aaed-997ac445fcd6)

## Assignment 1: Automated Instance Management Using AWS Lambda and Boto3
### Solution 1:
![image](https://github.com/user-attachments/assets/912fd96e-ced3-4637-8883-fa7165c59692)
This script manages EC2 instances based on specific tags (Vish-AutoStart and Vish-AutoStop). 
It performs the following operations:
- **Vish-AutoStop**: Finds running instances with this tag and stops them.
- **Vish-AutoStart**: Finds stopped instances with this tag and starts them.
- **Instance Identification**: It identifies the instances by both their InstanceId and their Name tag (or labels them as "Unnamed Instance" if no name is present).
- **Return Data**: The script returns the InstanceId and InstanceName of all the stopped and started instances.



## Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3
### Solution 2:
![image](https://github.com/user-attachments/assets/9ff4672f-9df8-4a3f-a878-e02b5fc18f43)


## Assignment 9: Archive Old Files from S3 to Glacier Using AWS Lambda and Boto3
### Solution 9:
![image](https://github.com/user-attachments/assets/395aec1e-844b-4c9d-ad93-ce781eb2432c)

## Assignment 15: Implement a Log Cleaner for S3
### Solution 15:
![image](https://github.com/user-attachments/assets/77876786-ae30-40a0-a281-3c177228901b)



