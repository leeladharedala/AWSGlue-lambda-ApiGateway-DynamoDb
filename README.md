# Serverless Data Processing Pipeline

A comprehensive serverless data processing pipeline built with AWS services including Lambda, DynamoDB, AWS Glue, and Redshift. This project demonstrates data generation, API processing, and ETL operations in a scalable cloud environment.

## Architecture Overview

This pipeline consists of several components:

- **API Layer:** AWS Lambda function with API Gateway for customer data ingestion  
- **Data Storage:** DynamoDB table for storing customer records  
- **Data Processing:** AWS Glue jobs for ETL operations  
- **Data Warehouse:** Redshift integration for analytics  
- **File Storage:** S3 bucket for temporary data and job artifacts  


## Project Structure

├── glue/
│ ├── dynamodbtoredshift.py # ETL job: DynamoDB → Redshift
│ ├── fakedata.py # Generates fake customer data
│ ├── senddata.py # Sends data to API endpoints (RDD approach)
│ └── senddata2.py # Alternative API sender (foreach approach)
├── lambda_functions/
│ ├── handler.py # Lambda function for customer creation
│ └── test_handler.py # Unit tests for Lambda function
├── dependencies/ # Python dependencies for Glue jobs
└── serverless.yml # Infrastructure as Code configuration



## Features

1. **Customer API (lambda_functions/handler.py)**
   - Creates customer records in DynamoDB  
   - Generates unique UUIDs for each customer  
   - Handles JSON payload validation  
   - Returns success/error responses  

2. **Fake Data Generator (glue/fakedata.py)**
   - Generates 50,000 fake customer records using Faker library  
   - Creates realistic customer data (names, emails, addresses)  
   - Adds country ranking using Spark window functions  
   - Outputs data to S3 in CSV format  

3. **API Data Sender (glue/senddata.py)**
   - Reads generated CSV data from S3  
   - Sends data to API endpoints using HTTP POST requests  
   - Implements partition-based processing for better performance  
   - Tracks success/failure counts and saves results to S3  
   - Handles request timeouts and error logging  

4. **DynamoDB to Redshift ETL (glue/dynamodbtoredshift.py)**
   - Extracts data from DynamoDB table  
   - Loads data into Redshift using JDBC connection  
   - Uses S3 as temporary storage during transfer  
   - Supports IAM role-based authentication  

## Prerequisites

- AWS Account with appropriate permissions  
- Serverless Framework installed  
- Python 3.12  
- Node.js (for Serverless Framework)  



