"""Aggregate hr analytics data in dwh"""
import logging

from common.connections import postgres_connection


def aggregate_hr_analytics(ymd: str, **_):
    """Perform data aggregation from hr_analytics to employee of the year in dwh

    Args:
        ymd(str): run date in format YYYYMMDD

    """
    logging.info(f"Start aggregate_hr_analytics on date {ymd}")
    postgres_connection(database="hr_analytics").connect().execute(
        f"""INSERT INTO employee_of_the_year(ymd, empid, department, point, rank_score)
        WITH tbl_emp_point AS (
            SELECT
                empid,
                department,
                (education + joblevel + monthlyrate + percentsalaryhike +
                performancerating + relationshipsatisfaction + standardhours +
                stockoptionlevel + totalworkingyears + trainingtimeslastyear + worklifebalance +
                yearsatcompany + yearsincurrentrole + yearssincelastpromotion) as point
            FROM
                data
            WHERE
                ymd = '{ymd}'
        ),
        tbl_result AS (
            SELECT
                empid,
                department,
                point,
                DENSE_RANK() OVER(
                    PARTITION BY department
                    ORDER BY point DESC
                ) AS rank_score
            FROM
                tbl_emp_point
        )
        SELECT
            '{ymd}' AS ymd,
            empid,
            department,
            point,
            rank_score
        FROM
            tbl_result
        WHERE
            rank_score <= 3
        """
    )
    logging.info(f"Finshed aggregation of hr_analytics data on date {ymd}")
