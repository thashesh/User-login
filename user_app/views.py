
import os
import uuid
from flask import request, redirect
from flask_restful import Resource, reqparse

from user_app.schema import get_user_schema, list_users_schema
from user_app.models import User, db

# from cStringIO import StringIO
from io import StringIO

# from boto.s3.connection import S3Connection
# from boto.s3.key import Key as S3Key
import boto3
from botocore.exceptions import ClientError
# from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
FILE_CONTENT_TYPES = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png'
}
BUCKET_NAME = "lambda-fleet"


class Hello(Resource):
    def get(self):
        return {"message": "Hello, World!"}

    def post(self):
        return {"message": "Hello, World!"}


class UserList(Resource):

    def get(self):
        user_obj = User.query.all()
        user_list = list_users_schema().dump(user_obj)
        return {'status': 'success', 'data': user_list}, 200
    
    def post(self):
        json_data = request.get_json()
        # import pdb; pdb.set_trace()
        if not json_data:
            return {"message": "No input data provided"}, 400
        try:
            user_data = get_user_schema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        user = User(
            first_name=json_data.get("first_name"),
            last_name=json_data.get("last_name"),
            password=json_data.get("password"),
            age=json_data.get("age"),
            email=json_data.get("email"),
        )
        db.session.add(user)
        db.session.commit()
        return {
            "status": 'success', 'data': get_user_schema().dump(user)
        }, 201

class UserDetails(Resource):
    def get(self, user_id):
        user_obj = User.query.get(user_id)
        user_list = get_user_schema().dump(user_obj)
        return {'status': 'success', 'data': user_list}, 200

class LoginUser(Resource):
    def post(self):
        json_data = request.get_json()
        # import pdb; pdb.set_trace()
        if not json_data:
            return {"message": "No input data provided"}, 400
        user = User.query.filter_by(
            first_name=json_data.get("first_name"),
            password=json_data.get("password")
        ).first()
        if not user:
            return {
                "status": "Unauthorized User",
                "message": "Incorrect unsername and password. Please retry!"
            }, 401
        return redirect("user_api/{0}".format(user.id), code=200)


## Helper Methods
def upload_s3(file, key_name, content_type):
    # create connection
    # conn = S3Connection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
    s3 = boto3.client('s3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY']
    )

    # upload the file after getting the right bucket
    try:
        s3.upload_file(
            Bucket = BUCKET_NAME,
            Filename = file,
            Key = key_name,
        )
    except ClientError as e:
        return False

    return True


class UploadImage(Resource):

    def put(self, user_id):

        img = request.files['image']

        # check logo extension
        extension = img.filename.rsplit('.', 1)[1].lower()
        if '.' in img.filename and not extension in ALLOWED_EXTENSIONS:
            abort(400, message="File extension is not one of our supported types.")

        # create a file object of the image
        filename = secure_filename(img.filename)
        img.save(filename)

        file_name = str(uuid.uuid1())
        # upload to s3
        key_name = '{0}/{1}.{2}'.format('profile_pics', file_name, extension)
        content_type = FILE_CONTENT_TYPES[extension]
        logo_url = upload_s3(filename, key_name, content_type)

        # update user profile with s3 url
        user_profile = "s3://{0}/{1}".format(BUCKET_NAME, key_name)
        user_obj = User.query.get(user_id)
        user_obj.profile = user_profile

        db.session.commit()
        
        return redirect("user_api/{0}".format(user_obj.id), code=204)
        # {
        #     "status": "Success",
        #     'data': get_user_schema().dump(user_obj)
        # }, 204
