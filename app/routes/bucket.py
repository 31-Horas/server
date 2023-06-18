from flask import Blueprint, request, jsonify
import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import dotenv_values
from flask_login import current_user, login_required
from csv_to_json import make_json


from app.extensions import db
from app.models.user import User
from app.models.bucket import Bucket

config = dotenv_values(".env")

client = boto3.client('s3', aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'],
                      region_name=config['REGION_NAME'])

bucket_name = config['BUCKET_NAME']

bucket_bp = Blueprint('bucket', __name__)

@bucket_bp.route("/get_data", methods=['GET'])
@login_required
def get_data():
    data = []
    user_id = current_user.get_id()
    buckets = Bucket.query.filter_by(user_id=user_id).all()  # Retrieve the buckets for the current user

    for obj in buckets:
        data.append((obj.bucketfile_name, obj.bucketfile_id))

    return jsonify(data)


@bucket_bp.route('/upload', methods=['POST'])
@login_required
def upload_to_s3():
    # Get the uploaded file from the request
    file = request.files['file']
    # Get the file name from the request
    file_name = request.form['filename']
    # Generate a unique file name
    file_code = os.urandom(24).hex()
    # Get the user_id from the request
    user_id = current_user.get_id()
    print(user_id)

    # Check if the file name already exists for the current user
    existing_file = Bucket.query.filter_by(bucketfile_name=file_name, user_id=user_id).first()
    if existing_file:
        return 'File with the same name already exists!', 409  # Return a conflict status code

    # Check if the file has a CSV or XLSX extension
    if file_name.lower().endswith('.csv'):
        file_extension = '.csv'
    elif file_name.lower().endswith(('.xlsx', '.xls')):
        file_extension = '.xlsx'
    else:
        return 'Only CSV and XLSX files are allowed!', 400  # Return a bad request status code

    # Generate the final file name with the extension
    file_code += file_extension

    # Create an instance of the Bucket model
    new_file = Bucket(file_name, file_code, user_id)

    db.session.add(new_file)
    db.session.commit()

    # Upload the file to S3
    client.put_object(
        Body=file,
        Bucket=bucket_name,
        Key=file_code
    )

    new_bucket = Bucket.query.filter_by(bucketfile_name=file_name, user_id=user_id).first()

    return {'message': 'File uploaded successfully!', 'id': new_bucket.bucketfile_id}, 200

@bucket_bp.route("/delete/<item_id>", methods=['DELETE'])
@login_required
def delete(item_id):
    bucket = Bucket.query.filter_by(bucketfile_id=item_id).first()
    if bucket:
        file_name = bucket.bucketfile_code
        print(file_name)
        # Delete the file from the bucket or storage system
        client.delete_object(
            Bucket=bucket_name,
            Key=file_name,
        )
        # Delete the corresponding MySQL row
        db.session.delete(bucket)
        db.session.commit()
        return f'File deleted: {bucket.bucketfile_name}', 200
    else:
        return 404