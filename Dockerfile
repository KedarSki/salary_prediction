# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Install dependencies without dev dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the current directory contents into the container at /app
COPY . .

# Make sure the prediction_models directory is included in the container
COPY prediction_models /app/prediction_models

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.fast_api:app", "--host", "0.0.0.0", "--port", "8000"]