from moto.server import ThreadedMotoServer
from pyspark.sql import SparkSession
import pytest
import os


warehouse_path = os.path.join(os.getcwd(), "warehouse")


@pytest.fixture()
def spark():
    server = ThreadedMotoServer()
    server.start()
    spark_builder = SparkSession.builder.master("local[*]").appName(
        "test-spark-session"
    )
    spark_builder.config(
        "spark.sql.extensions",
        "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
    )
    spark_builder.config(
        "spark.sql.catalog.glue_catalog", "org.apache.iceberg.spark.SparkCatalog"
    )
    spark_builder.config("spark.sql.catalog.glue_catalog.type", "hadoop")
    spark_builder.config(
        "spark.sql.catalog.glue_catalog.warehouse",
        warehouse_path,
    )
    spark_builder.config(
        "spark.sql.catalog.glue_catalog.default.write.metadata-flush-after-create",
        "true",
    )
    spark_builder.config("spark.sql.defaultCatalog", "glue_catalog")
    spark_builder.config(
        "spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.3.0"
    )
    spark_builder.config("spark.ui.showConsoleProgress", "false")
    spark_builder.config("spark.ui.enabled", "false")
    spark_builder.config("spark.sql.shuffle.partitions", "1")
    spark_builder.config("spark.executor.heartbeatInterval", "3600s")
    spark_builder.config("spark.network.timeout", "4200s")
    spark_builder.config("spark.storage.blockManagerSlaveTimeoutMs", "4200s")
    spark = spark_builder.getOrCreate()
    hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3.canned.acl", "BucketOwnerFullControl")
    hadoop_conf.set("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    hadoop_conf.set("fs.s3a.access.key", "mock")
    hadoop_conf.set("fs.s3a.secret.key", "mock")
    hadoop_conf.set("fs.s3a.endpoint", "http://127.0.0.1:5000")
    hadoop_conf.set("spark.sql.warehouse.dir", os.getcwd() + "/spark-warehouse")
    yield spark
    server.stop()
    spark.stop()