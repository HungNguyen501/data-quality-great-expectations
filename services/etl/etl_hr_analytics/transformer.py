"""Transform hr analytics data from raw_zone and store in clean zone"""
import sys
import logging

from pyspark.sql import DataFrame
from pyspark.storagelevel import StorageLevel
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import sha2
from great_expectations import data_context
from great_expectations.data_context.data_context.file_data_context import FileDataContext


def validate_df(gx: FileDataContext, df: DataFrame) -> dict:
    """Validate dataframe by GX

    Args:
        gx(FileDataContext): gx context
        df(DataFrame): dataframe is validated

    Returns result of validation as dict
    """
    checkpoint = gx.get_checkpoint(name="dpd_checkpoint")
    ck_kwargs = {
        "run_name_template": "%Y%m%d-%H%M%S-validate_transform_hr_analytics",
        "validations": [
            {
                "batch_request": {
                    "datasource_name": "sandbox_hdfs",
                    "data_connector_name": "sandbox_hdfs_runtime_connector",
                    "data_asset_name": "transform_hr_analytics",
                    "runtime_parameters": {
                        "batch_data": df
                    },
                    "batch_identifiers": {
                        "airflow_run_id": "{{ task_instance_key_str }}"
                    }
                },
                "expectation_suite_name": "transform_hr_analytics_suite"
            }
        ]
    }
    return checkpoint.run(**ck_kwargs).to_json_dict()


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
    """Run pipelines for tranformation"""
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    spark: SparkSession = SparkSession.builder \
        .master("local[*]") \
        .appName(name="job-transformer") \
        .getOrCreate()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    gx_context = data_context.get_context(context_root_dir="services/great_expectations")
    logger.info(f"input_file={input_file}")
    logger.info(f"output_file={output_file}")
    df_hr_analytics = spark.read.parquet(input_file)
    logger.info(f"input row_count={df_hr_analytics.count()}")
    df_filter = filter_data(df=df_hr_analytics)
    df_encrypt = encrypt_data(df=df_filter)
    df_encrypt.persist(StorageLevel.MEMORY_AND_DISK)
    logger.info(f"output row_count={df_encrypt.count()}")
    ck_result = validate_df(gx=gx_context, df=df_encrypt)
    if not ck_result["success"]:
        raise RuntimeError(f"Validation with Great Expectations failed.\nResults:\n {ck_result}")
    df_encrypt.coalesce(numPartitions=1).write.parquet(path=output_file, mode="overwrite")


if __name__ == '__main__':
    main()
