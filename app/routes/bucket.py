from flask import Blueprint, jsonify, request
import boto3
import os
from dotenv import dotenv_values

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

    client.put_object(
        # ACL='public-read',
        Body=file,
        Bucket=bucket_name,
        Key=file_name
    )

    # Return a response indicating success
    return 'File uploaded successfully!'

@bucket_bp.route("/delete/<item_id>", methods=['DELETE'])
def delete(item_id):
    file_name = item_id
    client.delete_object(
        Bucket=bucket_name,
        Key=file_name,
    )
    return f'File deleted: {file_name}'
