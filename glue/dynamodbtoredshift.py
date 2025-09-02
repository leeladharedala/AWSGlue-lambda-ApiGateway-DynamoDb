import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

args = getResolvedOptions(sys.argv, ['S3_BUCKET'])
path = f"s3://{args['S3_BUCKET']}/temp"

dynamo_dyf = glueContext.create_dynamic_frame.from_options(
    connection_type="dynamodb",
    connection_options={"dynamodb.input.tableName": "Customers_Table"}
)

glueContext.write_dynamic_frame.from_jdbc_conf(
    frame=dynamo_dyf,
    catalog_connection = "redshift-connection",
    connection_options={
        "dbtable": "customers",
        "database": "dev",
        "aws_iam_role": "arn:aws:iam::730335458634:role/service-role/AmazonRedshift-CommandsAccessRole-20250829T100859"
    },
    redshift_tmp_dir= path,
)

job.commit()