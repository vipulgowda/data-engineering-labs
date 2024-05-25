from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from google.cloud import storage
import json

project_id = "dataeng-gowda-vipulp"
subscription_id = "archivetest-sub"

subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(project_id, subscription_id)
json_list = []


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    json_message = json.loads(message.data.decode('utf-8'))
    json_list.append(json_message)
    message.ack()

streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback)

print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        streaming_pull_future.result(timeout=20.0)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

# Convert to JSON string
data_string = json.dumps(json_list)

# Encode to bytes
data_bytes = data_string.encode('utf-8')


def upload_blob_from_memory(bucket_name, data_bytes, destination_blob_name):
    """Uploads data from memory to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data_bytes, content_type='application/json')

    print(f"Data uploaded to {destination_blob_name}.")

# Usage
bucket_name = 'trimet-storage'
destination_blob_name = 'trimet.json'

upload_blob_from_memory(bucket_name, data_bytes, destination_blob_name)