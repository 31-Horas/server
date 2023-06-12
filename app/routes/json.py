from flask import Blueprint, request
import boto3
import json
from io import BytesIO
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


def decode_data(item_id):
    bucket = Bucket.query.filter_by(bucketfile_id=item_id).first()
    bucket_code = bucket.bucketfile_code
    # Obtiene la lista de objetos en el bucket
    response = client.get_object(Bucket=bucket_name, Key=bucket_code)

    # Lee el contenido del objeto
    object_data = response["Body"].read()

    # Convertir XLSX a CSV si es necesario
    if bucket_code.lower().endswith('.xlsx'):
        try:
            print('Data is not a csv.')
            # Leer el archivo XLSX usando pandas
            df = pd.read_excel(BytesIO(object_data))
            print('Xlsx readed.')

            # Convertir el DataFrame a CSV
            csv_data = df.to_csv(index=False)
            print('Xlsx converted to csv')

            # Encode the CSV data to bytes
            decoded_data = csv_data.encode("utf-8")

            print('Decoded data complete.')
            return decoded_data, 200
        except Exception as e:
            print('Error converting XLSX to CSV:', e)

    # Return the object_data as bytes
    print('Decoded data complete.')
    return object_data


@json_bp.route("json_data/<item_id>", methods=["GET"])
def json_data(item_id):
    try:
        decoded, status_code = decode_data(item_id)  # Renamed variable to avoid naming conflict
        if status_code != 200:
            return "Error decoding data", status_code
        
        tablelabels = []  # stores certification names
        tabledata = []  # stores number of times a certification appears
        df = None

        df = pd.read_csv(BytesIO(decoded), encoding='utf-8-sig')

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
    except Exception as e:
        print('Error generating JSON data:', e)
        return "Error generating JSON data", 500
