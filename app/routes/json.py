from flask import Blueprint, request
import boto3
import os
import csv
import json
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import dotenv_values
from flask_login import current_user

from app.extensions import db
from app.models.user import User
from app.models.bucket import Bucket

config = dotenv_values(".env")

client = boto3.client(
    "s3",
    aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
    region_name=config["REGION_NAME"],
)

bucket_name = "truerodobucket"

bucket_bp = Blueprint("bucket", __name__)


@bucket_bp.route("/json_data/<item_id>", methods=["GET"])
def json_data():
    bucket_name = Bucket.bucketfile_name
    # item_id =Bucket.bucketfile_id

    result = client.list_objects(Bucket=bucket_name)
    for o in result.get("Contents"):
        data = client.get_object(Bucket=bucket_name, Key=o.get("Key"))
        contents = data["Body"].read()
        print(contents.decode("utf-8"))
