"""
This module handles data processing tasks such as cleaning and encoding.
"""

import re
import pandas as pd
from pathlib import Path


def clean_data():
    """
    Load and clean the dataset by removing null values, duplicates,
    and ensuring the salary is numeric.
    """
    job_data = Path("C:\\Git\\salary_prediction\\data") / "job_data.csv"
    job_data_cleaned = Path("C:\\Git\\salary_prediction\\data") / "cleaned_data.csv"
    df = pd.read_csv(job_data)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df["salary"] = df["salary"].astype(str).apply(lambda x: re.sub(r"[^\d.]", "", x))
    df["salary"] = df["salary"].astype(float)
    df.to_csv(job_data_cleaned, index=False)


def data_parser():
    """
    Load cleaned data from file and parse objects into appropriate variable types.
    """
    job_data_cleaned = Path("C:\\Git\\salary_prediction\\data") / "cleaned_data.csv"
    data_set = pd.read_csv(job_data_cleaned)
    data_set["job_title"] = data_set["job_title"].astype("string")
    data_set["company"] = data_set["company"].astype("string")
    data_set["location"] = data_set["location"].astype("string")
    data_set["skills"] = data_set["skills"].astype("string")
    data_set["posted_date"] = pd.to_datetime(data_set["posted_date"], errors="coerce")
    data_set = data_set.dropna(subset=["posted_date"])
    base_date = pd.Timestamp("2000-01-01")
    data_set["posted_date"] = (data_set["posted_date"] - base_date).dt.days
    data_set = data_set[data_set["posted_date"] >= 0]
    return data_set


def compute_median():
    """
    Compute the median salary across all job postings.
    """
    data = data_parser()
    salary_median = data.groupby("job_title")["salary"].median().reset_index(name="salary_median")
    return salary_median


def main():
    """
    Clean data, parse it, and compute median salary.
    """
    clean_data()
    compute_median()
    data_parser()


if __name__ == "__main__":
    main()
