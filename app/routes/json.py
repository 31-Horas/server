from flask import Blueprint, request
import boto3
import json
import csv
import pandas as pd
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
def decoded_data(item_id):
    bucket = Bucket.query.filter_by(bucketfile_id=item_id).first()
    bucket_code = bucket.bucketfile_code
    print(bucket_name)  # obtenemos el nombre del bucket con cookies
    # Obtiene la lista de objetos en el bucket
    response = client.get_object(Bucket=bucket_name, Key=bucket_code)

    # Lee el contenido del objeto
    object_data = response["Body"].read()

    # Decodifica el contenido si es necesario
    decoded_data = object_data.decode("utf-8")

    return decoded_data, 200


@json_bp.route("json_data/<item_id>", methods=["GET"])
def json_data(item_id):
    decoded_data = decoded_data(item_id)

    tablelabels = []  # stores certification names
    tabledata = []  # stores number of times a certification appears
    df = pd.read_csv(decoded_data)

    for certification in df["certification"]:
        if certification in tablelabels:
            tabledata[
                tablelabels.index(certification)
            ] += 1  # if a certification was already saved, add 1 to the counter
        else:
            tablelabels.append(certification)  # else add the certification to the array
            tabledata.append(1)  # and initialize its counter at 1

    dataset = [
        {
            "label": "Certifications in IBM",  # stores data to be displayed in the graph
            "data": tabledata,
            "backgroundColor": "rgba(75, 192, 192, 0.6)",
            "borderColor": "rgba(75, 192, 192, 1)",
            "borderWidth": 1,
        }
    ]

    graphdata = {  # stores dataset array and certification names as labels
        "labels": tablelabels,
        "datasets": dataset,
    }

    tableoptions = {  # stores scaling options of graph
        "scales": {"x": {"type": "category"}, "y": {"beginAtZero": True}}
    }

    datajson = {  # stores previous dictionaries
        "type": "bar",
        "data": graphdata,
        "options": tableoptions,
    }

    return json.dumps(datajson, indent=4), 200
