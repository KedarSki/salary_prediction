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
    df = pd.DataFrame(test_data)
    df.to_csv("data/test_job_data.csv", index=False)

    # Run the clean_data function to clean and save the data
    clean_data()

    yield

    # Teardown: Remove the test CSV file
    os.remove("data\\test_job_data.csv")
    os.remove("data\\cleaned_job_data.csv")


def test_clean_data():
    # Ensure the cleaned data file was created
    assert os.path.exists("data/cleaned_job_data.csv")

    # Load the cleaned data and check its content
    cleaned_data = pd.read_csv("data/cleaned_job_data.csv")

    # Instead of hardcoding, let's ensure there are no null values and no duplicates
    assert cleaned_data.isnull().sum().sum() == 0  # Ensure no null values
    assert len(cleaned_data.drop_duplicates()) == len(cleaned_data)  # Ensure no duplicates


def test_data_parser():
    # Test the data_parser function
    parsed_data = data_parser()

    # Ensure the parsed data has the correct types
    assert parsed_data["job_title"].dtype == "string"
    assert parsed_data["company"].dtype == "string"
    assert parsed_data["posted_date"].dtype == "int64"  # Days since 2000-01-01


def test_compute_median(setup_test_environment):
    # Test the compute_median function
    median_data = compute_median()

    # Ensure the median data has the correct structure
    assert "job_title" in median_data.columns
    assert "salary_median" in median_data.columns  # Update this line
