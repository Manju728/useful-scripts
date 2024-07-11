from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
import boto3
import json
import logging
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import DataFrame
import sys


class SomeClass:
    def __init__(self):
        self.aws_region = ""
        self.db_url = ""
        self.certificate_path = ""  # DB certificate path in s3(if required)
        self.db_driver_path = ""  # DB driver in s3
        self.db_username = None
        self.db_password = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig()
        self.logger.setLevel(logging.INFO)
        self.spark = None
        self.df = None

    def get_arguments(self) -> None:
        """Fetching job arguments

        Returns:
            None
        """
        args = getResolvedOptions(
            sys.argv,
            [
                "AWS_REGION",
                "DB_URL",
                "CERTIFICATE_PATH",
                "DB_DRIVER_PATH",
            ],
        )
        self.aws_region = args["AWS_REGION"]
        self.db_url = args["DB_URL"]
        self.certificate_path = args["CERTIFICATE_PATH"]
        self.db_driver_path = args["DB_DRIVER_PATH"]

    def create_spark_session(self) -> None:
        """Initializing the spark session

        Returns:
            None
        """
        spark_conf = SparkConf()
        spark_context = SparkContext(conf=spark_conf)
        glue_context = GlueContext(spark_context)
        self.spark = glue_context.spark_session
        self.spark.sparkContext._jsc.hadoopConfiguration().set(
            "fs.s3.canned.acl", "BucketOwnerFullControl"
        )

    def load_table(self, table_name: str) -> DataFrame:
        self.logger.info(f"Loading the data of {table_name}")
        jdbc_properties = {
            "driver": "com.ibm.db2.jcc.DB2Driver",
            "user": self.db_username,
            "password": self.db_password,
            "loginTimeout": "60",
            "customJdbcDriverS3Path": self.db_driver_path,
            "sslcert": self.certificate_path,
        }
        df = (
            self.spark.read.format("jdbc")
            .option("url", self.db_url)
            .option("dbtable", table_name)
            .options(**jdbc_properties)
            .load()
        )
        return df

    def run(self) -> None:
        self.df = self.load_table("SELECT * FROM db.table")  # load data from d66


if __name__ == "__main__":
    some_job = SomeClass()
    some_job.get_arguments()
    client = boto3.client("secretsmanager", region_name=some_job.aws_region)
    # Fetching db credentials from secrets.
    get_secret_value_response = client.get_secret_value(SecretId="db_credentials")
    secret = get_secret_value_response["SecretString"]
    secret = json.loads(secret)
    some_job.db2_username = secret.get("db2_username")
    some_job.db2_password = secret.get("db2_password")
    some_job.create_spark_session()
    some_job.run()
