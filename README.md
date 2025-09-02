Serverless Data Processing Pipeline
A comprehensive serverless data processing pipeline built with AWS services including Lambda, DynamoDB, AWS Glue, and Redshift. This project demonstrates data generation, API processing, and ETL operations in a scalable cloud environment.
Architecture Overview
This pipeline consists of several components:

API Layer: AWS Lambda function with API Gateway for customer data ingestion
Data Storage: DynamoDB table for storing customer records
Data Processing: AWS Glue jobs for ETL operations
Data Warehouse: Redshift integration for analytics
File Storage: S3 bucket for temporary data and job artifacts

Project Structure
├── glue/
│   ├── dynamodbtoredshift.py    # ETL job: DynamoDB → Redshift
│   ├── fakedata.py              # Generates fake customer data
│   ├── senddata.py              # Sends data to API endpoints (RDD approach)
│   └── senddata2.py             # Alternative API sender (foreach approach)
├── lambda_functions/
│   ├── handler.py               # Lambda function for customer creation
│   └── test_handler.py          # Unit tests for Lambda function
├── dependencies/                 # Python dependencies for Glue jobs
└── serverless.yml               # Infrastructure as Code configuration
Features
1. Customer API (lambda_functions/handler.py)

Creates customer records in DynamoDB
Generates unique UUIDs for each customer
Handles JSON payload validation
Returns success/error responses

2. Fake Data Generator (glue/fakedata.py)

Generates 50,000 fake customer records using Faker library
Creates realistic customer data (names, emails, addresses)
Adds country ranking using Spark window functions
Outputs data to S3 in CSV format

3. API Data Sender (glue/senddata.py)

Reads generated CSV data from S3
Sends data to API endpoints using HTTP POST requests
Implements partition-based processing for better performance
Tracks success/failure counts and saves results to S3
Handles request timeouts and error logging

4. DynamoDB to Redshift ETL (glue/dynamodbtoredshift.py)

Extracts data from DynamoDB table
Loads data into Redshift using JDBC connection
Uses S3 as temporary storage during transfer
Supports IAM role-based authentication

Prerequisites

AWS Account with appropriate permissions
Serverless Framework installed
Python 3.12
Node.js (for Serverless Framework)

Setup and Deployment
1. Install Dependencies
bashnpm install -g serverless
pip install boto3 faker requests
2. Configure AWS Credentials
bashaws configure
3. Update Configuration
Edit serverless.yml and update:

org: Your Serverless Framework organization
s3BucketName: Unique S3 bucket name
AWS region if different from us-east-1

4. Deploy Infrastructure
bashserverless deploy
This will create:

DynamoDB table (Customers_Table)
S3 bucket for Glue jobs
IAM roles and policies
AWS Glue ETL jobs
Lambda function with API Gateway endpoint

5. Upload Dependencies
The deployment automatically syncs:

Glue Python scripts to S3
Required Python wheels (Faker, requests) to S3

Usage
1. Generate Fake Data
Run the Glue job to generate sample data:
bashaws glue start-job-run --job-name GlueFakeProfilesJob
2. Send Data to API
Execute the API sender job:
bashaws glue start-job-run --job-name GlueSendAPIJob_RDD
3. Transfer to Redshift
Before running the Redshift job, ensure:

Redshift cluster is available
Connection redshift-connection is configured in Glue Data Catalog
Target table exists in Redshift

bashaws glue start-job-run --job-name GlueSendDatatoRedshift
4. Direct API Usage
Send POST requests to the customer endpoint:
bashcurl -X POST https://your-api-gateway-url/dev/customer \
  -H "Content-Type: application/json" \
  -d '{
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "city": "New York",
    "state": "NY",
    "country": "USA",
    "zipcode": "10001"
  }'
Configuration
Environment Variables

DYNAMODB_TABLE: DynamoDB table name (set automatically)
S3_BUCKET: S3 bucket for temporary storage
api_endpoint: API Gateway endpoint URL

Glue Job Parameters

Worker Type: G.1X (standard workers)
Number of Workers: Varies by job (5-10 workers)
Glue Version: 5.0
Python Version: 3

Monitoring and Logging
CloudWatch Logs

Lambda function logs: /aws/lambda/{function-name}
Glue job logs: /aws-glue/jobs/logs-v2/

Job Monitoring

Track job execution in AWS Glue Console
Monitor API Gateway metrics
Check DynamoDB item counts
Review S3 output files for processing results

Performance Considerations
Partitioning Strategy

Fake data job: 250 partitions for 50K records
API sender: Dynamic partitioning based on ~800 records per partition
Configurable worker counts based on data volume

Error Handling

Request timeouts set to 10 seconds
Retry logic for failed API calls
Comprehensive error logging and result tracking
Graceful handling of malformed data

Testing
Unit Tests
Run Lambda function tests:
bashcd lambda_functions
python -m pytest test_handler.py
Integration Testing

Deploy the stack
Run the fake data generation job
Verify CSV output in S3
Test API endpoint manually
Run the API sender job
Check success/failure counts

Security
IAM Permissions

Least privilege principle applied
Separate roles for different services
VPC permissions for Glue jobs
Redshift and DynamoDB access controls

Data Protection

Data encrypted in transit and at rest
Secure API endpoints with CORS enabled
Environment variable protection
S3 bucket policies for access control

Troubleshooting
Common Issues
Glue Job Failures:

Check CloudWatch logs for detailed error messages
Verify S3 permissions and bucket existence
Ensure dependencies are properly uploaded

API Timeout Errors:

Increase timeout values in senddata.py
Reduce partition size for better distribution
Check API Gateway throttling limits

DynamoDB Errors:

Verify table exists and is active
Check IAM permissions for DynamoDB operations
Monitor write capacity if using provisioned mode

Redshift Connection Issues:

Ensure Redshift cluster is running
Verify connection configuration in Glue Data Catalog
Check VPC security group rules

Cost Optimization

Use spot instances for large Glue jobs when possible
Monitor DynamoDB read/write capacity usage
Implement S3 lifecycle policies for temporary data
Consider reserved capacity for predictable workloads

Future Enhancements

Add data quality checks and validation
Implement incremental data processing
Add monitoring dashboards with CloudWatch
Integrate with AWS Step Functions for workflow orchestration
Add data lineage tracking
Implement automated testing pipelines

Contributing

Fork the repository
Create a feature branch
Make changes and add tests
Submit a pull request

License
This project is licensed under the MIT License - see the LICENSE file for details.
