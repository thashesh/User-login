

from flask import Blueprint, Flask
from flask_restful import Api
from user_app.views import (
    Hello,
    UserDetails,
    UserList,
    UploadImage,
    LoginUser
)

api_bp = Blueprint('user_api', __name__)
api = Api(api_bp)
# app = Flask(__name__)
# api = Api(app)

# Route
api.add_resource(Hello, '/hello')
api.add_resource(UserList, '/')
api.add_resource(LoginUser, '/login')
api.add_resource(UserDetails, '/<int:user_id>')
api.add_resource(UploadImage, '/<int:user_id>/upload_image')
