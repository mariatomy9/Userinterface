from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
   #import os
connect_str = "DefaultEndpointsProtocol=https;AccountName=storage123indexer;AccountKey=COIu78pYQgQbkCnb0kQuHq9jL4owewY9MGZ5bQek9elUw64pqFf0/lkxSBnqjKtZpLFeMj1flZ/q1FBoC5Mgjg==;EndpointSuffix=core.windows.net"
# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Create a unique name for the container
container_name = "storage123indexerr" #name should be lowercase
# Create the container
try:
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    print(blob_list)
        
    for blob in blob_list:
        print(blob)
        print("\t" + blob.name)
        
    # Container exists. Now use it.
except Exception as e:
    # Container does not exist. Now create it.
    
    container_client = blob_service_client.create_container(container_name)

local_path = (r'/home/maria/Documents/azure/')
local_file_name = "image (8).JPG"
upload_file_path = os.path.join(local_path, local_file_name)
# Create a blob client using the local file name as the name for the blob
blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
print(blob_client)
print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

# Upload the created file
with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)

print(blob_client.url)
