from io import BytesIO, BufferedReader
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

account_url = "https://team50filestorage.blob.core.windows.net"
default_credential = DefaultAzureCredential()

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=default_credential)

def upload_blob_to_container(content: bytes, filename: str, year: str):
    bio = BytesIO()
    bio.write(content)
    bio.seek(0)
    container_name = "fileupload"
    local_file_name = f"{year}/{filename}"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    blob_client.upload_blob(BufferedReader(bio))