# -*- encoding:utf-8 -*-
import os
import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy(basedir)

class DataRecord(db.Model):
    pass