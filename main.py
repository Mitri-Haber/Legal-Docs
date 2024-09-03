import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from Connections.AzureDataLake import AzureStorageManager
from Connections.MongoMotor import MongoDBClient
from pymongo import MongoClient
import requests
from io import BytesIO
# Load environment variables
load_dotenv()

# Read environment variables
AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')

# Initialize MongoDB
mongo_client = MongoClient('mongodb://admin:admin123@localhost:27017/KD?authSource=admin')
db = mongo_client['KD']
collection = db['pdf_documents']

# Initialize Azure Storage Manager
azure_manager = AzureStorageManager(
    account_name=AZURE_ACCOUNT_NAME,
    container_name=AZURE_CONTAINER_NAME,
    account_key=AZURE_ACCOUNT_KEY
)

def download_pdf(url):
    response = requests.get(url)
    response.raise_for_status()
    content = response.content
    file_stream = BytesIO(content)
    file_stream.name = url.split("/")[-1]
    return file_stream

def process_file(url, target_category):
    file_stream = download_pdf(url)
    if file_stream.getbuffer().nbytes > 0:
        # Upload to Azure
        azure_manager.upload_pdf(file_stream, target_category)
        # Update MongoDB
  
def main():
    urls = [
        'https://www.oikeusasiamies.fi/r/fi/ratkaisut/-/eoar/8024/2023',
        'https://www.oikeusasiamies.fi/r/fi/ratkaisut/-/eoar/639/2024'
    ]
    target_category = 'Category1'

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_file, url, target_category) for url in urls]
        for future in as_completed(futures):
            future.result()

    # Close Azure Storage Manager
    azure_manager.close()

if __name__ == "__main__":
    main()
