
# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
WHOOSH_BASE = os.path.join(basedir, 'search.db')

TWILIO_ACCOUNT_SID = "ACe4e7ede50e0eaca6c6678c3f639e32cf"
TWILIO_AUTH_TOKEN = "5619512c1bb716e8fada2db30fa30438"
TWILIO_SENDER_NUMBER = "+14152149361"