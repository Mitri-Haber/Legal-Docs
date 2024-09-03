import os
from azure.storage.blob import BlobServiceClient

class AzureStorageManager:
    def __init__(self, account_name=None, container_name=None, account_key=None, token=None):
        if not account_name:
            account_name = os.getenv("AZURE_ACCOUNT_NAME")
        if not container_name:
            container_name = os.getenv("AZURE_CONTAINER_NAME")
        if not account_key:
            account_key = os.getenv("AZURE_ACCOUNT_KEY")
        
        if account_key:
            self.blob_service_client = BlobServiceClient(
                account_url=f"https://{account_name}.blob.core.windows.net",
                credential=account_key
            )
        elif token:
            self.blob_service_client = BlobServiceClient(
                account_url=f"https://{account_name}.blob.core.windows.net",
                credential=token
            )
        else:
            raise ValueError("Either account_key or token must be provided.")
        
        self.container_name = container_name
        self.container_client = self.blob_service_client.get_container_client(container_name)
        self.source = os.getenv("SOURCE_HOST")
        # Ensure the container exists
        self._create_container_if_not_exists()

    def _create_container_if_not_exists(self):
        if not self.container_client.exists():
            self.container_client.create_container()

    def upload_data(self, data: bytes, blob_name: str):
        """
        Upload binary data to Azure Blob Storage.

        :param data: Binary data to upload
        :param blob_name: Name of the blob in Azure Storage
        """
         
        
        # Construct the blob path using the source host
        blob_path = f"{self.source}/{blob_name}"
        
        blob_client = self.container_client.get_blob_client(blob_path)
        
        # Upload the data
        blob_client.upload_blob(data, overwrite=True)
        
        # print(f"Data uploaded to blob '{blob_path}'.")

