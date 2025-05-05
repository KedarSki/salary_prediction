import os
from pathlib import Path

import oracledb
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def load_jobs_from_csv(job_data_cleaned: str) -> None:
    try:
        df = pd.read_csv(job_data_cleaned, encoding="latin1")
        df.columns = df.columns.str.upper()

        expected_cols = {"JOB_TITLE", "COMPANY", "LOCATION", "SALARY"}
        if not expected_cols.issubset(df.columns):
            raise ValueError(f"Expected columns missing in CSV file. Expected columns {expected_cols}")

        conn = oracledb.connect(
            user=os.getenv("ORACLE_USER"), password=os.getenv("ORACLE_PASSWORD"), dsn=os.getenv("ORACLE_DSN")
        )

        cursor = conn.cursor()

        insert_sql = """
        INSERT INTO JOBS (TITLE, COMPANY, LOCATION, SALARY)
        VALUES (:1, :2, :3, :4)
        """

        data = df[["JOB_TITLE", "COMPANY", "LOCATION", "SALARY"]].values.tolist()
        cursor.execute("TRUNCATE TABLE JOBS")
        conn.commit()

        cursor.executemany(insert_sql, data)
        conn.commit()
        print("Data has been loaded to 'jobs' table")

    except Exception as e:
        print(f"Load data error [{type(e).__name__}]: {e}")

    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    job_data_cleaned = Path(os.getenv("CLEANED_DATA_PATH"))
    load_jobs_from_csv(job_data_cleaned)
