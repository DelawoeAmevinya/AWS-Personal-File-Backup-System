# AWS-Personal-File-Backup-System
This project implements an event-driven personal file backup system on AWS that automatically copies files from a source S3 bucket to a backup bucket and sends email notifications upon successful backup.

## Architecture
flowchart TD
    A[User Uploads File] --> B[S3 Source Bucket]
    B -- ObjectCreated Event --> C[AWS Lambda]
    C -- Copy Operation --> D[S3 Backup Bucket]
    C -- Send Notification --> E[AWS SNS]
    E --> F[Email Notification]
    C -- Log Activity --> G[AWS CloudWatch]
    
    H[AWS IAM] -- Provides Permissions --> C

## Features
- Automated file backup on upload
- Timestamped backups to prevent overwrites
- Email notifications via SNS
- Comprehensive CloudWatch logging
- Secure IAM configuration

## Setup Instructions
1. Create s3 buckets( Source and Backup Buckets)
2. Create a SNS Topic
3. Create a IAM role for Lambda - Create role and attach policies
4. Create Lambda function
5. Congifure s3 event trigger
6. Test the system via Lamda console
7. Verify each component works
8. Cleanup to avoid ongoing charges.

## Cost Analysis
Free-tier friendly estimate: $0-2/month for personal use

## Lessons Learned
Security configurations should be part of initial resource creation
Always enable encryption, block public access, use least privilege
IAM permissions are non-negotiable and must be correct from the start
Implement robust filename handling for all special characters
Default 3-second timeout is insufficient for S3 operations
