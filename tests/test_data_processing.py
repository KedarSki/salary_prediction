from pathlib import Path
import os
import pandas as pd
import pytest
from src.data_processing import clean_data, data_parser, compute_median


@pytest.fixture(scope="module")
def setup_test_environment():
    # Setup: Create a sample CSV file for testing
    test_data = {
        "job_title": ["Data Scientist", "Software Engineer", "Data Scientist"],
        "company": ["XYZ Corp", "ABC Inc", "XYZ Corp"],
        "location": ["New York", "San Francisco", "New York"],
        "salary": ["120000", "150000", "110000"],
        "skills": ["Python, Machine Learning", "Java, Spring", "Python, SQL"],
        "posted_date": ["2023-08-15", "2023-08-16", "2023-08-17"],
    }
    test_job_data = Path("data") / "test_job_data.csv"
    cleaned_test_job_data = Path("data") / "cleaned_data.csv"
    df = pd.DataFrame(test_data)
    df.to_csv(test_job_data, index=False)

    # Run the clean_data function to clean and save the data
    clean_data()

    yield

    # Teardown: Remove the test CSV file
    os.remove(test_job_data)
    os.remove(cleaned_test_job_data)


def test_clean_data(setup_test_environment):
    cleaned_test_job_data_path = Path("data") / "cleaned_data.csv"

    # Ensure the cleaned data file was created
    assert os.path.exists(cleaned_test_job_data_path)

    # Load the cleaned data as a pandas DataFrame
    cleaned_test_job_data = pd.read_csv(cleaned_test_job_data_path)

    # Ensure there are no missing values in the cleaned data
    assert cleaned_test_job_data.isnull().sum().sum() == 0

    # Ensure there are no duplicate rows in the cleaned data
    assert len(cleaned_test_job_data.drop_duplicates()) == len(cleaned_test_job_data)


def test_data_parser():
    parsed_data = data_parser()

    assert parsed_data["job_title"].dtype == "string"
    assert parsed_data["company"].dtype == "string"
    assert parsed_data["posted_date"].dtype == "int64"  # Days since 2000-01-01


def test_compute_median():
    # Test the compute_median function
    median_data = compute_median()

    # Ensure the median data has the correct structure
    assert "job_title" in median_data.columns
    assert "salary_median" in median_data.columns  # Ensure salary_median column exists
