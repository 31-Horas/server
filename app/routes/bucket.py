from flask import Blueprint, request
import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import dotenv_values
from flask_login import current_user


from app.extensions import db
from app.models.user import User
from app.models.bucket import Bucket

config = dotenv_values(".env")

client = boto3.client('s3', aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'],
                      region_name=config['REGION_NAME'])

bucket_name = 'truerodobucket'

bucket_bp = Blueprint('bucket', __name__)

@bucket_bp.route('/download_data/<item_id>', methods=['GET'])
def download_data(item_id):
    file_name = item_id
    file_path = f"data/downloaded_{file_name}"

    with open(file_path, 'wb') as f:
        client.download_fileobj(bucket_name, f'{file_name}', f)
    
    return 'File downloaded successfully'


@bucket_bp.route("/get_data", methods=['GET'])
def getdata():
    data = ''
    for obj in client.list_objects(Bucket=bucket_name)['Contents']:
        data += obj['Key'] + '\n'
    return data

@bucket_bp.route('/upload', methods=['POST'])
def upload_to_s3():
    # Get the uploaded file from the request
    file = request.files['file']
    # Generate a unique file name
    file_name = os.urandom(24).hex() + '.csv'
    # Get the user_id from the request
    user_id = current_user.get_id
    # Create an instance of the Bucket model
    new_file = Bucket(file.name, file_name, user_id)

    db.session.add(new_file)
    db.session.commit()

    client.put_object(
            Body=file,
            Bucket=bucket_name,
            Key=file_name
        )
    return 'File uploaded successfully!', 200
    

@bucket_bp.route("/delete/<item_id>", methods=['DELETE'])
def delete(item_id):
    file_name = item_id
    client.delete_object(
        Bucket=bucket_name,
        Key=file_name,
    )
    return f'File deleted: {file_name}'
