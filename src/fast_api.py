"""
This module provides the FastAPI endpoints for the job salary prediction service.
"""

from typing import Dict, Tuple, Any
import logging
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.preprocessing import LabelEncoder

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class JobPosting(BaseModel):
    """
    Data model for job postings used in the prediction endpoint.
    """

    job_title: str
    company: str
    location: str
    salary: str
    skills: str
    posted_date: str


def load_model_and_encoders(
    model_file: str = "prediction_models/random_forest.pkl",
) -> Tuple[Any, Dict[str, LabelEncoder]]:
    """
    Load the machine learning model and label encoders from the specified file.
    """
    try:
        with open(model_file, "rb") as f:
            data = joblib.load(f)
        model = data["model"]
        label_encoders = data["label_encoders"]
        logger.info("Model and label encoders loaded from %s", model_file)
        return model, label_encoders
    except FileNotFoundError as exc:
        logger.error("Model file not found.")
        raise HTTPException(status_code=500, detail="Model file not found.") from exc
    except Exception as e:
        logger.exception("Failed to load the model and encoders.")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/predict")
def predict(job_posting: JobPosting) -> Dict[str, bool]:
    """
    Predict whether the salary for a job posting is above or below the median.
    """
    try:
        model, label_encoders = load_model_and_encoders()

        data = pd.DataFrame([job_posting.model_dump()])

        for column in ["job_title", "company", "location"]:
            if column in label_encoders:
                le = label_encoders[column]
                if data[column][0] in le.classes_:
                    data[column] = le.transform([data[column][0]])[0]
                else:
                    raise HTTPException(status_code=400, detail=f"Unknown value for '{column}': {data[column][0]}.")

        data["skills"] = data["skills"].apply(lambda x: len(x.split(",")))

        data["posted_date"] = pd.to_datetime(data["posted_date"], errors="coerce")
        if data["posted_date"].isna().any():
            raise HTTPException(status_code=400, detail="Invalid date format.")
        data["posted_date"] = data["posted_date"].apply(lambda x: (x - pd.Timestamp("2000-01-01")).days)

        features = ["job_title", "company", "location", "salary", "skills", "posted_date"]
        for feature in features:
            if feature not in data.columns:
                raise HTTPException(status_code=400, detail=f"Missing required feature: '{feature}'")

        data = data[features]

        data["salary"] = pd.to_numeric(data["salary"], errors="coerce")
        if data["salary"].isna().any():
            raise HTTPException(status_code=400, detail="Invalid salary value.")

        data = data.fillna(0)

        prediction = model.predict(data)
        salary_above_median = bool(prediction[0])

        logger.info("Prediction successful.")
        return {"salary_above_median": salary_above_median}

    except HTTPException as http_exc:
        logger.warning("HTTP Exception: %s", http_exc.detail)
        raise http_exc
    except Exception as e:
        logger.exception("An error occurred during prediction.")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.") from e
