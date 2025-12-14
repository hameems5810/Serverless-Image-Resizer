import os
import urllib.parse
import boto3

s3 = boto3.client("s3")
OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET", "")

def lambda_handler(event, context):
    # Get first record from S3 event
    record = event["Records"][0]
    src_bucket = record["s3"]["bucket"]["name"]
    src_key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

    print(f"Source bucket: {src_bucket}, key: {src_key}")
    print(f"Output bucket: {OUTPUT_BUCKET}")

    # Don't process objects that are already in the output bucket
    if src_bucket == OUTPUT_BUCKET:
        print("Object is already in output bucket, skipping.")
        return

    # Build destination key
    dest_key = f"resized-{src_key}"

    # Copy object from input bucket to output bucket
    copy_source = {"Bucket": src_bucket, "Key": src_key}
    s3.copy_object(
        Bucket=OUTPUT_BUCKET,
        Key=dest_key,
        CopySource=copy_source,
    )

    print(f"Copied {src_bucket}/{src_key} -> {OUTPUT_BUCKET}/{dest_key}")
