from pyspark.sql import SparkSession, Row
from awsglue.utils import getResolvedOptions
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import sum, when, col, count
import sys
import requests

spark = SparkSession.builder\
    .appName("Send API Data")\
    .getOrCreate()

args = getResolvedOptions(sys.argv, ['S3_BUCKET'])
path = f"s3://{args['S3_BUCKET']}/fakedata/"

api_args = getResolvedOptions(sys.argv, ['api_endpoint'])
api_endpoint = api_args['api_endpoint']

df = spark.read.option("header", "true").csv(f"{path}")

row_count = df.count()

print(f"Number of partitions: {df.rdd.getNumPartitions()}")

update_partitions = round(row_count/800)

df_repartitioned = df.repartition(update_partitions)

print(f"Number of partitions after updating: {df_repartitioned.rdd.getNumPartitions()}")

# def send_data_to_api(iterator):
#     results = []
#     for row in iterator:
#         payload = row.asDict()
#         try:
#             response = requests.post(api_endpoint, json=payload, timeout=10)
#             response.raise_for_status()
#             print(f"Successfully posted: {payload}, Response: {response.status_code}")
#             results.append(("success", str(payload), response.status_code))
#         except requests.exceptions.RequestException as e:
#             print(f"Failed to post: {payload}, Error: {e}")
#             results.append(("failure", str(payload), 500))
#     return results



# result_df = df_repartitioned.rdd.mapPartitions(send_data_to_api).toDF(schema=schema)

# count_df = result_df.agg(sum(when(col("status") == "success", 1).otherwise(0)).alias("success_count"),sum(when(col("status") == "failure", 1).otherwise(0)).alias("failure_count"),count("*").alias("TotalCount"))



# count_path = f"s3://{args['S3_BUCKET']}/fakedata/counts/"
# count_df.coalesce(1).write.format("csv").option("header", "true").mode("overwrite").save(f"{count_path}")


def send_data_to_api(row):
        payload = row.asDict()
        try:
            response = requests.post(api_endpoint, json=payload, timeout=10)
            response.raise_for_status()
            print(f"Successfully posted: {payload}, Response: {response.status_code}")
            return Row(status= "success", payload= str(payload), status_code= response.status_code)
        except requests.exceptions.RequestException as e:
            print(f"Failed to post: {payload}, Error: {e}")
            return Row(status= "failed", payload= str(payload), status_code= str(e))

schema = StructType([
    StructField("status", StringType(), True),
    StructField("payload", StringType(), True),
    StructField("status_code", StringType(), True)
])

results_df = df_repartitioned.rdd.map(send_data_to_api).cache().toDF(schema=schema).cache()
print(results_df.count())

# results_df = spark.createDataFrame(results, schema=schema)

count_df = results_df.agg(sum(when(col("status") == "success", 1).otherwise(0)).alias("success_count"),sum(when(col("status") == "failed", 1).otherwise(0)).alias("failure_count"),count("*").alias("TotalCount"))


count_path = f"s3://{args['S3_BUCKET']}/fakedata/counts/"
count_df.coalesce(1).write.format("csv").option("header", "true").mode("overwrite").save(f"{count_path}")
result_path = f"s3://{args['S3_BUCKET']}/fakedata/results/"
results_df.coalesce(1).write.format("csv").option("header", "true").mode("overwrite").save(f"{result_path}")


# def send_data_to_api(row):
#     payload = row.asDict()
#     try:
#         response = requests.post(api_endpoint, json=payload, timeout=10)
#         response.raise_for_status()
#         print(f"Successfully posted: {payload}, Response: {response.status_code}")
#         return {"status": "success", "payload": payload, "status_code": response.status_code}
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to post: {payload}, Error: {e}")
#         return {"status": "failed", "payload": payload, "status_code": response.status_code}
#
#
# schema = StructType([
#     StructField("status", StringType(), True),
#     StructField("payload", StringType(), True),
#     StructField("status_code", IntegerType(), True)
# ])
#
# results = df_repartitioned.rdd.map(send_data_to_api).collect()
#
# results_df = spark.createDataFrame(results, schema=schema)
#
# count_df = results_df.agg(sum(when(col("status") == "success", 1).otherwise(0)).alias("success_count"),
#                           sum(when(col("status") == "failure", 1).otherwise(0)).alias("failure_count"),
#                           count("*").alias("TotalCount"))
#
# count_path = f"s3://{args['S3_BUCKET']}/fakedata/counts/"
# count_df.coalesce(1).write.format("csv").option("header", "true").mode("overwrite").save(f"{count_path}")
# result_path = f"s3://{args['S3_BUCKET']}/fakedata/results/"
# results_df.coalesce(1).write.format("csv").option("header", "true").mode("overwrite").save(f"{result_path}")