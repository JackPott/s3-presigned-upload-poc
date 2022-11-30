# S3 Upload with pre-signed URLS

This is a simple proof of concept to demonstrate uploading files to S3 with a presigned URL, avoiding the need for the client to do any AWS authentication directly, and avoiding the need to stream large files via a backend API before storing it in S3.  

## Where to look

[main.py](main.py) shows the backend code with two simple methods for generating an upload URL, and returning a list of objects in the bucket with download URLS

[index.html](static/index.html) has the Javascript in it which lets the client get the URL asyncronously and PUT the file to it. Has some minor embelishment to show off the bucket contents in a pretty way. 

## Run it locally

```sh
# Install deps and venv, requires poetry
poetry install --no-root

# Auth shell to AWS
aws-vault exec sandbox-ca

# Load venv
source .venv/bin/activate

# Start webserver
python3 main.py 

# Go to localhost:8000 in browser
```

Note bucket name is hardcoded in [main.py](main.py)

## TODO: 

- [ ] Upload a demo video 