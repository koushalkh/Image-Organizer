from flask import Flask,flash, request, redirect, url_for
from config import Config
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = '/home/chetan/Desktop/Image-Organizer/app/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes