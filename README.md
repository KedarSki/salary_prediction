📋 Overview

This project is designed to help with basic Machine Learning workflows in Python using Poetry for dependency management and pytest for testing. The goal of this project is to predict if a job's salary is above the median using a simple ML model. The project includes tasks such as data processing, model building, and deploying a basic FastAPI service, all packaged in a Docker container.

🏆 Key Deliverables

🧹 Data Processing Pipeline: A well-defined pipeline for cleaning and preparing the data.

🧠 Machine Learning Model: A trained and evaluated ML model.

🔌 FastAPI Application: A RESTful service for salary prediction.

🐳 Dockerized Application: A Docker container that can be deployed locally or on a cloud platform.

🧪 Unit Tests: Tests covering your data processing, prediction logic, and API.


🚀 How to Get Started:

Requirements:

🐍 Python >= 3.8

🧩 Poetry >= 1.2

🐋 Docker (optional for containerized deployment)

Setup:

Clone the Repository:

git clone https://github.com/YourGitHubUsername/salary_prediction.git
cd salary_prediction

Install Dependencies: Use Poetry to manage dependencies:
make poetry-download
make poetry-install-deps

Activate the Environment: Activate the virtual environment (manual method not included here)

poetry shell

Run Tests: Execute all tests to ensure everything works as expected.
make check-all

Run the Application: Start the FastAPI service locally.
poetry run uvicorn src.main:app --reload

Docker Deployment (Optional): Build and run the containerized application.
docker build -t salary-prediction .
docker run -p 8000:8000 salary-prediction

📂 Project Structure

salary_prediction/


├── .venv/                    # Virtual environment (not included in GitHub)

├── src/                      # Source code

│   ├── models/               # ML models and training scripts

│   ├── data/                 # Data processing pipeline

│   ├── api/                  # FastAPI application

│   └── tests/                # Unit tests

├── Dockerfile                # Docker container configuration

├── Makefile                  # Automation scripts (tests, linting, etc.)

├── pyproject.toml            # Poetry configuration

├── README.md                 # Documentation

└── requirements.txt          # Dependencies (for non-Poetry users)

Makefile Guide
The Makefile automates common tasks, such as:

🛠 Dependency Installation: make poetry-install-deps

🔍 Running Tests: make check-all

🧹 Running Linters: make black_check, make pylint, and make mypy

TODO:
- Add missing classes to all files so instance of an objects will be possible to create
- Single Responsibility Principle - data_processing.py and model_building.py both processing data. Place processing data in one file and each function e.g. Data cleaner, Data parser, data_process in according classes.
- Implement interface load_model_and_encoders and predict to enable modifications.
- Split train model method for smaller methods
- Use Pathlib class where necessary to read paths by multiplatform 
- Use context manager for database connection
- All sensitive paths and any consent data place in .env file