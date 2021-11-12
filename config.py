import os
from dotenv import load_dotenv
import cloudinary

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

cloudinary.config(cloud_name = os.environ.get('CLOUD_NAME'), api_key = os.environ.get('API_KEY'), api_secret = os.environ.get('API_SECRET'))

class Config():
    """
        Set Config variables for the flask app.
        Using Evironment variables where available otherwise
        create the config variables if not done already.
    """
    api_key = os.environ.get('API_KEY')
    api_secret = os.environ.get('API_SECRET')
    cloud_name = os.environ.get('CLOUD_NAME')

    SECRET_KEY = os.environ.get('SECRET_KEY')  or "You will never guess" 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Turn off Update Messages from the sqlalchemy
    CLOUDINARY_URL = "cloudinary://" + api_key + ":" + api_secret + "@" + cloud_name
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')

