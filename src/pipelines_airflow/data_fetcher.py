import os

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

def download_csv_from_url(url: str, output_path: str):
    pass
    
if __name__ == "__main__":
    url = Path(os.getenv("CLEAN_DATA_URL"))
    output_path = ""
    download_csv = download_csv_from_url(url, output_path)
