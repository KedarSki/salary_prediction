from fastapi.testclient import TestClient
from src.fast_api import app

client = TestClient(app)


def test_predict_endpoint():
    response = client.post(
        "/predict",
        json={
            "job_title": "Maintenance engineer",
            "company": "Bright Ltd",
            "location": "Scottville",
            "salary": "1200544",
            "skills": "several, small",
            "posted_date": "2024-07-20",
        },
    )
    assert response.status_code == 200
    assert "salary_above_median" in response.json()


def test_predict_unknown_value():
    response = client.post(
        "/predict",
        json={
            "job_title": "Unknown Job",
            "company": "XYZ Corp",
            "location": "New York",
            "salary": "120000",
            "skills": "Python, Machine Learning, Data Science",
            "posted_date": "2023-08-15",
        },
    )
    assert response.status_code == 400
    assert "detail" in response.json()
