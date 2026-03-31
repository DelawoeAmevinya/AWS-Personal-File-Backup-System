import boto3
import urllib.parse
import logging
from datetime import datetime
import os

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Environment variables (BEST PRACTICE instead of hardcoding)
BACKUP_BUCKET = os.environ['BACKUP_BUCKET']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']


def lambda_handler(event, context):
    try:
        # Extract bucket and file info from event
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        file_key = urllib.parse.unquote_plus(
            event['Records'][0]['s3']['object']['key']
        )

        # Create timestamped filename
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        backup_key = f"backup_{timestamp}_{file_key}"

        # Copy file to backup bucket
        s3.copy_object(
            CopySource={'Bucket': source_bucket, 'Key': file_key},
            Bucket=BACKUP_BUCKET,
            Key=backup_key
        )

        logger.info(f"✅ Backup successful: {file_key} → {backup_key}")

        # Send notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='✅ File Backup Successful',
            Message=(
                f"Backup completed successfully.\n\n"
                f"Original File: s3://{source_bucket}/{file_key}\n"
                f"Backup File: s3://{BACKUP_BUCKET}/{backup_key}\n"
                f"Time: {timestamp}"
            )
        )

        return {
            'statusCode': 200,
            'body': 'Backup successful'
        }

    except Exception as e:
        logger.error(f"❌ Backup failed: {str(e)}")
        raise
