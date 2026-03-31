# 📦 AWS Personal File Backup System

![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20SNS%20%7C%20CloudWatch-orange?logo=amazonaws)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Cost](https://img.shields.io/badge/Cost-Free%20Tier%20Friendly-yellow)

An **event-driven personal file backup system** built on AWS that automatically copies files from a source S3 bucket to a backup bucket and sends email notifications upon success.

---

## 🏗️ Architecture

![Architecture](Screenshots/file%20backup%20architecture.png)

**Workflow:**
1. User uploads file to S3 source bucket  
2. S3 triggers AWS Lambda  
3. Lambda copies file to backup bucket  
4. SNS sends email notification  
5. CloudWatch logs all activity  

---

## 🚀 Features

- ✅ Automated file backup on upload  
- 🕒 Timestamped filenames (prevents overwrite)  
- 📧 Email notifications via SNS  
- 📊 CloudWatch logging  
- 🔐 Least-privilege IAM security  
- 🔒 Encryption enabled (SSE-S3)  
- 🚫 Public access blocked  

---

## 📂 Project Structure
AWS-Personal-File-Backup-System/
├── lambda_function.py
├── iam-policy.json
├── README.md
└── Screenshots/
├── file backup architecture.png
├── main s3 bucket.png
├── s3 backup screenshot.png
├── Email Notification.png
└── Log events.png

---
## ⚙️ Lambda Function (Core Logic)

python
import boto3
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
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key']
    )

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_key = f"backup_{timestamp}_{file_key}"

    try:
        s3.copy_object(
            CopySource={'Bucket': source_bucket, 'Key': file_key},
            Bucket=BACKUP_BUCKET,
            Key=backup_key
        )

        logger.info(f"Backed up {file_key}")

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='✅ File Backup Successful',
            Message=(
                f"Original: s3://{source_bucket}/{file_key}\n"
                f"Backup: s3://{BACKUP_BUCKET}/{backup_key}\n"
                f"Time: {timestamp}"
            )
        )

        return {'statusCode': 200}

    except Exception as e:
        logger.error(str(e))
        raise
🛠️ Setup Instructions

1️⃣ Create S3 Buckets
aws s3api create-bucket --bucket your-source-bucket --region us-east-1
aws s3api create-bucket --bucket your-backup-bucket --region us-east-1

2️⃣ Create SNS Topic
aws sns create-topic --name FileBackupNotifications

Subscribe email:

aws sns subscribe \
  --topic-arn YOUR_TOPIC_ARN \
  --protocol email \
  --notification-endpoint your@email.com
3️⃣ Configure IAM Role

Attach:

AWSLambdaBasicExecutionRole
Custom policy (S3 + SNS access)
4️⃣ Create Lambda Function
Runtime: Python 3.12
Timeout: 30 seconds
Add environment variables
5️⃣ Configure S3 Trigger
Event: s3:ObjectCreated:*
Destination: Lambda
6️⃣ Test System
aws s3 cp testfile.txt s3://your-source-bucket/

📸 Results:
1. ![Email20%Notification](Screenshots/Email20%Notification.png)
2. ![Log20%Events](Screenshots/Log20%events.png)
3. ![Main20%s320%Bucket](Screenshots/main20%s320%bucket.png)
4. ![s320%backup20%Screenshot](Screenshots/s320%backup20%screenshot.png)


💰 Cost

Runs within AWS Free Tier:

Service	Usage
S3	Minimal
Lambda	Minimal
SNS	Minimal
CloudWatch	Minimal

💵 Estimated: $0 – $2/month

📚 Lessons Learned
Security first (encryption + block public access)
IAM least privilege is critical
Lambda timeout must be increased
Handle special characters in filenames
Use timestamps to prevent overwrite
👤 Author

Delawoe Amevinya Kwasi

LinkedIn: https://linkedin.com/in/delawoe-amevinya-kwasi
Email: amevinyadelawoe@gmail.com
