"""
Main module to execute the data processing, model training, and FastAPI setup.
"""

from .data_processing import clean_data, data_parser, compute_median
from .model_building import process_data, train_model


def main():
    """
    Execute the main steps: clean data, process it, and train the model.
    """
    clean_data()
    data_parser()
    compute_median()
    process_data()
    train_model()


if __name__ == "__main__":
    main()
