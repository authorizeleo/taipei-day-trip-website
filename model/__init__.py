from flask import *
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask('__main__')

app.secret_key = os.urandom(26)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

db = SQLAlchemy(app)