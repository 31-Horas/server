from flask import Blueprint, request, jsonify
import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import dotenv_values
from flask_login import current_user, login_required


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
@login_required
def get_data():
    data = []
    user_id = current_user.get_id()
    buckets = Bucket.query.filter_by(user_id=user_id).all()  # Retrieve the buckets for the current user

    for obj in buckets:
        data.append(obj.bucketfile_name)  # Append the 'bucketfile_name' attribute to the list

    return jsonify(data)


@bucket_bp.route('/upload', methods=['POST'])
@login_required
def upload_to_s3():
    # Get the uploaded file from the request
    file = request.files['file']
    # Get the file name from the request
    file_name = request.form['filename']
    # Generate a unique file name
    file_code = os.urandom(24).hex() + '.csv'
    # Get the user_id from the request
    user_id = current_user.get_id()
    print(user_id)

    # Check if the file name already exists for the current user
    existing_file = Bucket.query.filter_by(bucketfile_name=file_name, user_id=user_id).first()
    if existing_file:
        return 'File with the same name already exists!', 409  # Return a conflict status code

    # Create an instance of the Bucket model
    new_file = Bucket(file_name, file_code, user_id)

    db.session.add(new_file)
    db.session.commit()

    client.put_object(
        Body=file,
        Bucket=bucket_name,
        Key=file_name
    )
    
    return 'File uploaded successfully!', 200
    

@bucket_bp.route("/delete/<item_id>", methods=['DELETE'])
@login_required
def delete(item_id):
    file_name = item_id
    client.delete_object(
        Bucket=bucket_name,
        Key=file_name,
    )
    return f'File deleted: {file_name}'
