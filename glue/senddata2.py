from pyspark.sql import SparkSession
from awsglue.utils import getResolvedOptions
import sys
import requests

spark = SparkSession.builder\
         .appName("Send data using foreach")\
         .getOrCreate()

args = getResolvedOptions(sys.argv, ['S3_BUCKET'])
path = f"s3://{args['S3_BUCKET']}/fakedata/"

api_args = getResolvedOptions(sys.argv, ['api_endpoint'])
api_endpoint = api_args['api_endpoint']

df = spark.read.option("header", "true").csv(path)

print(f"Number of partitions: {df.rdd.getNumPartitions()}")

def send_partition_to_api(partition_rows):
    for row in partition_rows:
        payload = row.asDict()
        try:
            response = requests.post(api_endpoint, json=payload)
            response.raise_for_status()
            print(f"Successfully posted: {payload}, Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to post: {payload}, Error: {e}")

df.foreachPartition(send_partition_to_api)