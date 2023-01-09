

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db_engine = create_engine('sqlite:///db.sqlite?check_same_thread=False')
Base = automap_base()
Base.prepare(autoload_with=db_engine)
sqlalchemy.orm.configure_mappers()
session= Session(db_engine)

from application import routes
