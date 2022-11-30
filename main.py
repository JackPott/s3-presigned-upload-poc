import logging

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from flask import Flask

"""
To run use `python3 main.py` and expect it to host on localhost:8000
It expects AWS credentials on the shell you run it from, ie;
  aws-vault exec sandbox-ca
The account you auth to should have a bucket configured with the correct CORS policy
"""
bucket = "999999999999-upload-test"

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

app.logger.info('-'*88)
app.logger.info("Welcome to the Amazon S3 presigned URL demo.")
app.logger.info('-'*88)


# Region is important to get a region specific upload URL and avoid CORS errors
s3_client = boto3.client('s3', region_name='eu-west-2')


@app.route("/")
def hello_world():
    return "<a href=\"/static/index.html\">Start here</a>"

@app.route("/get_upload_url/<key>")
def get_upload_url(key):
    client_action = 'put_object'
    url = generate_presigned_url(
        s3_client, client_action, {'Bucket': bucket, 'Key': key}, 1000)
    return url

@app.route("/list_objects")
def list_objects():
    return list_s3_objects(s3_client, bucket)


def generate_presigned_url(s3_client, client_method, method_parameters, expires_in):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.

    :param s3_client: A Boto3 Amazon S3 client.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params=method_parameters,
            ExpiresIn=expires_in
        )
        app.logger.info("Got presigned URL: %s", url)
    except ClientError:
        app.logger.exception(
            "Couldn't get a presigned URL for client method '%s'.", client_method)
        raise
    return url


def list_s3_objects(s3_client, bucket_name):
    """
    Lists all the objects in specified bucket, creating a pre-signed URL for each
    """
    try:
        app.logger.info("Getting files...")
        files = s3_client.list_objects(
            Bucket=bucket_name
        )
        app.logger.info("Done")
        file_list = []
        for f in files["Contents"]:
            app.logger.info(f"Getting presigned URL for {f}")
            url = generate_presigned_url(s3_client, 'get_object', {'Bucket': bucket_name, 'Key': f['Key']}, 1000)
            file_list.append({"key": f['Key'], "url": url})
        
    except ClientError:
        app.logger.exception("Couldn't list objects in bucket '%s", bucket_name)
        raise
    return {"file_list": file_list}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
