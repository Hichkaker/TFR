from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# if os.environ.get('HEROKU') is not None:
import logging
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('TFR3 startup')


from app import views, models

# def create_vol():
#
#     if models.Vol.get(phone='+19177948192')
