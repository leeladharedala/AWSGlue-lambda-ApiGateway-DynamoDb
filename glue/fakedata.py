from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import dense_rank, col
from pyspark.sql.window import Window
from faker import Faker
from awsglue.utils import getResolvedOptions
import sys


spark = SparkSession.builder\
    .appName("Generate Fake Data")\
    .getOrCreate()

args = getResolvedOptions(sys.argv, ['S3_BUCKET'])

output_path = f"s3://{args['S3_BUCKET']}/fakedata/"

num_of_users = 50000

user_schema = StructType([
    StructField("firstname", StringType(), False),
    StructField("lastname", StringType(), False),
    StructField("email", StringType(), False),
    StructField("phone", StringType(), False),
    StructField("city", StringType(), False),
    StructField("state", StringType(), False),
    StructField("country", StringType(), False),
    StructField("zipcode", StringType(), False)
])

def generate_fake_data(record):
    fake = Faker()
    return (
        fake.first_name(),
        fake.last_name(),
        fake.email(),
        fake.phone_number(),
        fake.city(),
        fake.state(),
        fake.country(),
        fake.zipcode()
    )

df_data = spark.sparkContext.parallelize(range(num_of_users), 250).map(generate_fake_data).toDF(schema=user_schema)

window_spec = Window.orderBy("country")

df_data = df_data.withColumn("country_id", dense_rank().over(window_spec))

df_data.coalesce(1).write.option("header", "true").format("csv").mode("overwrite").save(output_path)