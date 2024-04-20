from google.cloud import pubsub_v1
import json
# TODO(developer)
project_id = "dataeng-gowda-vipulp"
topic_id = "my-topic"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

#for n in range(1, 10):
#    data_str = f"Message number {n}"
    # Data must be a bytestring
#    data = data_str.encode("utf-8")
    # When you publish a message, the client returns a future.
#    future = publisher.publish(topic_path, data)
#    print(future.result())

def publish_message(data):
    future = publisher.publish(topic_path, data.encode("utf-8"))
    print(f"Published message: {data}")

with open("bcsample.json","r") as json_file:
    records = json.load(json_file)
    for record in records:
        publish_message(json.dumps(record))

print(f"Published messages to {topic_path}.")