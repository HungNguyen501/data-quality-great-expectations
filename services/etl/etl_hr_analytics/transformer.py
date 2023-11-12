"""Transform hr analytics data from raw_zone and store in clean zone"""
import sys
import logging

from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import sha2


def filter_data(df: DataFrame) -> DataFrame:
    """Filter employee by age and years with current manager
    and then select main columns

    Args:
        df(DataFrame): input dataframe
    Returns dataframe satisfised conditions

    """
    df_fillter_null = df.filter(condition="YearsWithCurrManager is not null and Age < 55")
    return df_fillter_null.select([
        "EmpID",
        "Age",
        "Department",
        "Education",
        "EducationField",
        "Gender",
        "JobLevel",
        "JobRole",
        "MonthlyRate",
        "OverTime",
        "PercentSalaryHike",
        "PerformanceRating",
        "RelationshipSatisfaction",
        "StandardHours",
        "StockOptionLevel",
        "TotalWorkingYears",
        "TrainingTimesLastYear",
        "WorkLifeBalance",
        "YearsAtCompany",
        "YearsInCurrentRole",
        "YearsSinceLastPromotion",
    ])


def encrypt_data(df: DataFrame) -> DataFrame:
    """Encrypt EmpID field

    Args:
        df(DataFrame): intput dataframe
    Returns encrypted data

    """
    return df.withColumn("EmpID", sha2(df["EmpID"], 256))


def main():
    """Run etl pipelines"""
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    logging.info(f"input_file={input_file}")
    logging.info(f"output_file={output_file}")
    spark: SparkSession = SparkSession.builder \
        .master("local[*]") \
        .appName(name="job-transformer") \
        .getOrCreate()
    df_hr_analytics = spark.read.parquet(input_file)
    df_filter = filter_data(df=df_hr_analytics)
    encrypt_data(df=df_filter) \
        .coalesce(numPartitions=1).write.parquet(path=output_file, mode="overwrite")


if __name__ == '__main__':
    main()
