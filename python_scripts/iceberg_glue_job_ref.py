from awsglue.context import GlueContext
import boto3
import logging
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def create_spark_session() -> SparkSession:
    """Initializing the spark session

    Returns:
        SparkSession: spark session
    """
    region = boto3.session.Session().region_name
    print(f"region: {region}")
    conf = (
        SparkConf()
        .set(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
        )
        .set(
            "spark.sql.catalog.glue_catalog",
            "org.apache.iceberg.spark.SparkCatalog",
        )
        .set(
            "spark.sql.catalog.glue_catalog.warehouse",
            "s3://default/default",
        )
        .set(
            "spark.sql.catalog.glue_catalog.catalog-impl",
            "org.apache.iceberg.aws.glue.GlueCatalog",
        )
        .set(
            "spark.sql.catalog.glue_catalog.io-impl",
            "org.apache.iceberg.aws.s3.S3FileIO",
        )
        .set(
            "spark.sql.catalog.glue_catalog.s3.canned.acl",
            "bucket-owner-full-control",
        )
    )
    sc = SparkContext(conf=conf)
    glue_context = GlueContext(sc)
    spark = glue_context.spark_session
    spark.sparkContext._jsc.hadoopConfiguration().set(
        "fs.s3.canned.acl", "BucketOwnerFullControl"
    )
    return spark

