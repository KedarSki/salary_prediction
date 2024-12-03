"""
This module handles the machine learning model training for job salary predictions.
"""

from pathlib import Path
import os
import sys
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.preprocessing import LabelEncoder
from src.data_processing import data_parser, compute_median

sys.path.append(str(Path(__file__).resolve().parents[1]))


def process_data():
    """
    Process the data: compute the median salary and encode categorical variables.
    """
    salary_median = compute_median()
    data_set = data_parser()

    data_set = data_set.merge(salary_median, on="job_title", how="left")
    data_set["salary_above_median"] = data_set["salary"] > data_set["salary_median"]

    label_encoders = {}
    for column in ["job_title", "company", "location"]:
        le = LabelEncoder()
        data_set[column] = le.fit_transform(data_set[column])
        label_encoders[column] = le

    data_set["skills"] = data_set["skills"].apply(lambda x: len(x.split(",")))
    data_set = data_set.drop(columns=["salary_median"])
    return data_set, label_encoders


def train_model():
    """
    Train the RandomForestClassifier model using the processed data.
    """
    salary_data, label_encoders = process_data()
    random_forest_ml = Path("prediction_models") / "random_forest.pkl"

    features, target = (
        salary_data.drop(columns=["salary_above_median"]),
        salary_data["salary_above_median"],
    )

    features_train, features_test, target_train, target_test = train_test_split(
        features, target, test_size=0.20, random_state=123, stratify=target
    )

    model = RandomForestClassifier(random_state=42, n_estimators=200, max_depth=10, class_weight="balanced")
    model.fit(features_train, target_train)

    predictions = model.predict(features_test)
    print(classification_report(target_test, predictions))
    print(f"Accuracy: {accuracy_score(target_test, predictions):.2f}")
    print(f"Precision: {precision_score(target_test, predictions):.2f}")
    print(f"Recall: {recall_score(target_test, predictions):.2f}")
    print(f"F1 Score: {f1_score(target_test, predictions):.2f}")

    model_and_encoders = {"model": model, "label_encoders": label_encoders}

    if not os.path.exists("prediction_models"):
        os.makedirs("prediction_models")

    joblib.dump(model_and_encoders, random_forest_ml)
    print("Model and label encoders saved as 'random_forest.pkl'.")
    return model, label_encoders


def main():
    """
    Execute the main steps: clean data, process it, and train the model.
    """
    train_model()


if __name__ == "__main__":
    main()
