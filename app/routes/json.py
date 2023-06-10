from flask import Blueprint, request
import boto3
import os
import csv
import json
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import dotenv_values
from flask_login import current_user

from csv_to_json import make_json

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


@json_bp.route("/<item_id>", methods=["GET"])
def json_data(item_id):
    bucket = Bucket.query.filter_by(bucketfile_id=item_id).first()
    bucket_code = bucket.bucketfile_code
    print(bucket_name) # obtenemos el nombre del bucket con cookies
    # Obtiene la lista de objetos en el bucket
    response = client.get_object(Bucket=bucket_name, Key=bucket_code)
    
    # Lee el contenido del objeto
    object_data = response['Body'].read()

    # Decodifica el contenido si es necesario
    decoded_data = object_data.decode('utf-8')    

    return decoded_data, 200