AWS Personal File Backup System
[https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20SNS%20%7C%20CloudWatch-orange?logo=amazonaws]
[https://img.shields.io/badge/Python-3.12-blue?logo=python]
[https://img.shields.io/badge/Status-Complete-brightgreen]
[https://img.shields.io/badge/Cost-Free%20Tier%20Friendly-yellow]

An event-driven personal file backup system built on AWS that automatically copies files from a source S3 bucket to a backup bucket and sends email notifications upon successful backup.

Architecture
flowchart TD
    A[User Uploads File] --> B[S3 Source Bucket]
    B -- ObjectCreated Event --> C[AWS Lambda]
    C -- Copy Operation --> D[S3 Backup Bucket]
    C -- Send Notification --> E[AWS SNS]
    E --> F[Email Notification]
    C -- Log Activity --> G[AWS CloudWatch]
    H[AWS IAM] -- Provides Permissions --> C

[https://raw.githubusercontent.com/DelawoeAmevinya/AWS-Personal-File-Backup-System/main/Screenshots/file%20backup%20architecture.png]


Features
Automated file backup triggered on every upload
Timestamped filenames to prevent overwrites
Email notifications via SNS on successful backup
Comprehensive CloudWatch logging for all operations
Secure IAM configuration with least-privilege access
Encryption enabled on both S3 buckets
Public access blocked by default


Project Structure
AWS-Personal-File-Backup-System/
├── lambda_function.py              # Core Lambda handler
├── iam-policy.json                 # IAM role policy document
├── README.md
└── Screenshots/
    ├── file backup architecture.png
    ├── main s3 bucket.png
    ├── s3 backup screenshot.png
    ├── Email Notification.png
    └── Log events.png

Lambda Function (Core Logic)
pythonimport boto3
import urllib.parse
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
sns = boto3.client('sns')

BACKUP_BUCKET = 'your-backup-bucket-name'
SNS_TOPIC_ARN = 'arn:aws:sns:your-region:your-account-id:your-topic-name'

def lambda_handler(event, context):
    # Extract source bucket and file key from the S3 event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key']
    )

 Generate a timestamped backup filename to prevent overwrites
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_key = f"backup_{timestamp}_{file_key}"

    try:
 Copy file from source to backup bucket
        s3.copy_object(
            CopySource={'Bucket': source_bucket, 'Key': file_key},
            Bucket=BACKUP_BUCKET,
            Key=backup_key
        )
        logger.info(f"Successfully backed up {file_key} to {BACKUP_BUCKET}/{backup_key}")

 Send SNS email notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='✅ File Backup Successful',
            Message=(
                f"File backup completed successfully.\n\n"
                f"Original File: s3://{source_bucket}/{file_key}\n"
                f"Backup Location: s3://{BACKUP_BUCKET}/{backup_key}\n"
                f"Timestamp: {timestamp}"
            )
        )

 return {'statusCode': 200, 'body': 'Backup successful'}

except Exception as e:
        logger.error(f"Backup failed for {file_key}: {str(e)}")
        raise

Setup Instructions
Prerequisites

AWS account (free tier is sufficient)
AWS CLI installed and configured
Basic familiarity with the AWS Console


Step 1 — Create S3 Buckets
Create two buckets: one as the source and one as the backup.
bash# Source bucket
aws s3api create-bucket --bucket your-source-bucket \
  --region us-east-1
  [Screenshots/main s3 bucket.png]

 Backup bucket
aws s3api create-bucket --bucket your-backup-bucket \
  --region us-east-1
For both buckets, enable the following in the AWS Console under bucket settings:

Block all public access — ON
Server-side encryption (SSE-S3) — Enabled
[Screenshots/s3 backup screenshot.png]

Step 2 — Create an SNS Topic
bashaws sns create-topic --name FileBackupNotifications
Then subscribe your email address:
bashaws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:FileBackupNotifications \
  --protocol email \
  --notification-endpoint your@email.com
Check your inbox and confirm the subscription.

Step 3 — Create IAM Role for Lambda
In the AWS Console, create a new IAM role with the following trust policy (Lambda as the trusted entity) and attach these permissions:

AWSLambdaBasicExecutionRole (AWS managed)
A custom inline policy for S3 and SNS:

json{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::your-source-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::your-backup-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": ["sns:Publish"],
      "Resource": "arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:FileBackupNotifications"
    }
  ]
}

Step 4 — Create Lambda Function
In the AWS Console:

Go to Lambda → Create function
Runtime: Python 3.12
Attach the IAM role created in Step 3
Set timeout to 30 seconds (default 3s is insufficient for S3 operations)
Paste the Lambda code from above
Update BACKUP_BUCKET and SNS_TOPIC_ARN with your actual values

Step 5 — Configure S3 Event Trigger
In the AWS Console:

Go to your source S3 bucket → Properties → Event notifications
Create a new notification:

Event type: s3:ObjectCreated:*
Destination: Lambda function → select your function


Step 6 — Test the System
Upload a test file to your source bucket:
bashaws s3 cp testfile.txt s3://your-source-bucket/
Then verify:
[Screenshots/Email Notification.png]
log events
[Screenshots/Log events.png]

The file appears in your backup bucket with a timestamp prefix
You receive an email notification
CloudWatch logs show a successful execution

Step 7 — Cleanup (Avoid Ongoing Charges)
When done testing, remove all resources to avoid charges:
bash# Empty and delete buckets
aws s3 rm s3://your-source-bucket --recursive
aws s3 rm s3://your-backup-bucket --recursive
aws s3api delete-bucket --bucket your-source-bucket
aws s3api delete-bucket --bucket your-backup-bucket

# Delete Lambda function
aws lambda delete-function --function-name your-function-name

# Delete SNS topic
aws sns delete-topic --topic-arn arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:FileBackupNotifications

# Delete IAM role (detach policies first via Console)

Cost Analysis
This project runs comfortably within the AWS Free Tier for personal use.
ServiceFree Tier AllowanceExpected UsageS35 GB storage, 20K GET, 2K PUTMinimalLambda1M requests/month, 400K GB-secMinimalSNS1M publishes/monthMinimalCloudWatch5 GB logs/monthMinimal
Estimated cost for personal use: $0 – $2/month

Lessons Learned

Security must be built in from the start — enabling encryption and blocking public access should happen at bucket creation, not as an afterthought
IAM permissions are non-negotiable — overly broad permissions caused early issues; least-privilege must be correct before testing
Default Lambda timeout (3 seconds) is insufficient for S3 operations — always set a higher timeout (30s recommended)
Filename handling matters — special characters in filenames require urllib.parse.unquote_plus() to decode correctly
Timestamped backup keys prevent silent overwrites — without them, re-uploading the same file replaces the previous backup


Author
Delawoe Amevinya Kwasi

LinkedIn: linkedin.com/in/delawoe-amevinya-kwasi
Email: amevinyadelawoe@gmail.com
