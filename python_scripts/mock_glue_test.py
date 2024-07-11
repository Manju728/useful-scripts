from moto import mock_s3
from moto import mock_glue
from moto.server import ThreadedMotoServer
import boto3
import os
from awsglue.context import GlueContext
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql.functions import current_date


def create_mock_services_and_test():
    print(os.getcwd()+'/test.csv')
    csv_path = os.getcwd()+'/test.csv'
    server = ThreadedMotoServer()
    server.start()
    mock_s3().start()
    mock_glue().start()
    local_moto_server_endpoint = "http://127.0.0.1:5000"
    s3_client = boto3.client("s3", region_name='eu-west-1', endpoint_url=local_moto_server_endpoint)
    s3_client.create_bucket(
        Bucket='test-bucket',
        CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-1'
        }
    )
    s3_client.upload_file(csv_path, 'test-bucket', 'test.csv')
    glue_client = boto3.client("glue", region_name='eu-west-1', endpoint_url=local_moto_server_endpoint)
    glue_client.create_database(
        DatabaseInput={
            'Name': 'test_data_base'
        }
    )
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    glue_context = GlueContext(sc)
    spark_session = glue_context.spark_session
    hadoop_conf = spark_session.sparkContext._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3.canned.acl", "BucketOwnerFullControl")
    hadoop_conf.set("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    hadoop_conf.set("fs.s3a.access.key", "mock")
    hadoop_conf.set("fs.s3a.secret.key", "mock")
    hadoop_conf.set("fs.s3a.endpoint", local_moto_server_endpoint)
    hadoop_conf.set("spark.sql.warehouse.dir", os.getcwd()+'/spark-warehouse')
    spark_session.sql("create database test_data_base")
    spark_session.sql("use test_data_base")

    s3_path = "s3://test-bucket/test.csv"
    df = spark_session.read.csv(
        s3_path,
        sep=",",
        header=True,
    )
    df.printSchema()
    df.show()
    df.withColumn(
        "ingest_date", current_date()
    ).write.options(
        path="s3://test-bucket/test_data_mapping"
    ).format(
        "parquet"
    ).mode(
        "overwrite"
    ).partitionBy(
        ['p_ingest_date']
    )
    df.coalesce(1).write.mode("overwrite").csv("s3://test-bucket/test_data_mapping", header=True)
    mock_s3().stop()
    mock_glue().start()


create_mock_services_and_test()
