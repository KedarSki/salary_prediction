import os
import requests
import logging

import pandas as pd

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)-+

def download_csv_from_url(url: str, output_path: str):
    try:
        get_csv = requests.get(url, stream=True)
        df = pd.read_csv(get_csv.raw)
        df.to_csv(output_path, index=False)
    except Exception as e:
        logger.exception("Error server connection to fetch csv file")
        raise Exception(f"Download failed: {e}") from e

if __name__ == "__main__":
    url = os.getenv("DATA_SOURCE")
    output_path = os.getenv("OUTPUT_PATH")
    download_csv_from_url(url, output_path)