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

json_bp = Blueprint("json", __name__)


@json_bp.route("/json_data/<item_id>", methods=["GET"])
def json_data():
    bucket_name = Bucket.bucketfile_name  # obtenemos el nombre del bucket con cookies
    result = client.list_objects(
        Bucket=bucket_name
    )  # obtenemos el resultado de la lista de objetos del bucket
    o = result.get("Contents")[0]  # obtenemos el primer objeto de la lista
    # for o in result.get("Contents"):
    data = client.get_object(
        Bucket=bucket_name, Key=o.get("Key")
    )  # obtenemos el objeto con el nombre del bucket y la key
    contents = data[
        "Body"
    ].read()  # obtenemos el contenido del objeto (puede ser binary file)
    print(contents.decode("utf-8"))
    print(type(contents))