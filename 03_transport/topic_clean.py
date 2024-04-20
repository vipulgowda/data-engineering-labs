import os
from google.cloud import pubsub_v1

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    sub='my-sub',  # Set this to something appropriate.
)

def callback(message):
    print(message.data)
    message.ack()

with pubsub_v1.SubscriberClient() as subscriber:
    streaming_pull_future = subscriber.subscribe(subscription_name, callback=callback)
    try:
      streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.