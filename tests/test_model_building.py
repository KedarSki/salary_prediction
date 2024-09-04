import pytest
from src.model_building import train_model, process_data
from src.data_processing import clean_data


# Ensure data is cleaned before running tests
@pytest.fixture(scope="module", autouse=True)
def setup_test_environment():
    clean_data()


def test_process_data():
    data_set, label_encoders = process_data()
    assert "job_title" in data_set.columns
    assert "salary_above_median" in data_set.columns
    assert isinstance(label_encoders, dict)
    assert len(label_encoders) == 3  # Assuming 3 columns are encoded


def test_train_model():
    model, label_encoders = train_model()
    assert model is not None
    assert len(label_encoders) == 3  # Assuming 3 columns are encoded
