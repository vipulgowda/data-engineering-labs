from google.cloud import storage


def create_bucket_class_location():
    """
    Create a new bucket in the US region with the nearline storage
    class
    """
    bucket_name = "trimet-storage"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "NEARLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket

create_bucket_class_location()