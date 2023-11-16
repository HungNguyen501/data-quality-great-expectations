"""Module to load data from clean zone to dwh"""
import sys
import logging

from pyspark.sql import SparkSession
from pyspark.sql import functions as SF


def load_to_dwh():
    """Run etl pipelines"""
    ymd = sys.argv[1]
    input_file = sys.argv[2]
    postgres_host = sys.argv[3]
    postgres_port = sys.argv[4]
    postgres_user = sys.argv[5]
    postgres_password = sys.argv[6]
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"input_file={input_file}")
    spark: SparkSession = SparkSession.builder \
        .master("local[*]") \
        .appName(name="job-dwh-loader") \
        .getOrCreate()
    df_hr_analytics = spark.read.parquet(input_file)
    logger.info(f"row_count={df_hr_analytics.count()}")
    df_hr_analytics = df_hr_analytics.withColumn(colName="ymd", col=SF.lit(ymd))
    df_hr_analytics.write \
        .mode(saveMode="append") \
        .format(source="jdbc") \
        .options(
            url=f"jdbc:postgresql://{postgres_host}:{postgres_port}"
                "/hr_analytics",
            driver="org.postgresql.Driver",
            user=postgres_user,
            password=postgres_password,
            dbtable="data",
        ) \
        .save()


if __name__ == "__main__":
    load_to_dwh()
