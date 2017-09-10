# -*- encoding:utf-8 -*-
import json
import sqlalchemy
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Float, Text

import database
from database import db
from log import logger


class SerialComTable(db.BaseModel):
    __tablename__ = "serialdata"
    id = Column(Integer, primary_key=True)
    barcode = Column(String(64))
    flag_bit = Column(Text)
    tight_torque = Column(Text)
    tight_angle = Column(Text)
    record_date = Column(DateTime)


def insert_productItem(barcode=None, flag_bit=None, tight_torque=None, tight_angle=None):
    product_data = SerialComTable(barcode=barcode,
                                  flag_bit=json.dumps(flag_bit),
                                  tight_torque=json.dumps(tight_torque),
                                  tight_angle=json.dumps(tight_angle),
                                  record_date=datetime.now())
    db.add(product_data)


def update_productItem(barcode=None, flag_bit=None, tight_torque=None, tight_angle=None):
    with db.getQuery(SerialComTable) as query:
        res = query.order_by(SerialComTable.id.desc()).first()
        if res:
            res.barcode = barcode
            res.flag_bit = json.dumps(flag_bit)
            res.tight_torque = json.dumps(tight_torque)
            res.tight_angle = json.dumps(tight_angle)
            res.record_date = datetime.now()


def query_productItem(session):
    res = session.query(SerialComTable).order_by(
        SerialComTable.id.desc()).first()
    return res


def query_productInfo():
    product_info = {}
    try:
        with db.getQuery(SerialComTable) as query:
            res = query.order_by(SerialComTable.id.desc()).first()
            if res is not None:
                product_info["id"] = res.id
                product_info["barcode"] = res.barcode
                product_info["tight_torque"] = json.loads(res.flag_bit)
                product_info["tight_torque"] = json.loads(res.tight_torque)
                product_info["tight_angle"] = json.loads(res.tight_angle)
                product_info["record_date"] = res.record_date.strftime(
                    "%Y-%m-%d %H:%M:%S")
                return product_info
    except Exception as e:
        logger.warning(e)
        return


def query_productInfoByID(id):
    product_info = {}
    try:
        with db.getQuery(SerialComTable) as query:
            res = query.get(id)
            if res:
                product_info["id"] = res.id
                product_info["barcode"] = res.barcode
                product_info["tight_torque"] = json.loads(res.flag_bit)
                product_info["tight_torque"] = json.loads(res.tight_torque)
                product_info["tight_angle"] = json.loads(res.tight_angle)
                product_info["record_date"] = res.record_date.strftime(
                    "%Y-%m-%d %H:%M:%S")
                return product_info
    except Exception as e:
        logger.warning(e)
        return


def query_id():
    with db.getQuery(SerialComTable) as query:
        res = query.order_by(SerialComTable.id.desc()).first()
        return res.id


def query_barcode():
    with db.getQuery(SerialComTable) as query:
        res = query.order_by(SerialComTable.id.desc()).first()
        return res.barcode


def query_tight_torque():
    with db.getQuery(SerialComTable) as query:
        res = query.order_by(SerialComTable.id.desc()).first()
        return json.loads(res.tight_torque)


def query_tight_torque():
    with db.getQuery(SerialComTable) as query:
        res = query.order_by(SerialComTable.id.desc()).first()
        return json.loads(res.tight_angle)


def query_datetime():
    with db.getQuery(SerialComTable) as query:
        res = query.order_by(SerialComTable.id.desc()).first()
        return res.record_date


# 查询最新count条数据
def query_last_few_items(count):
    with db.getQuery(SerialComTable) as query:
        res = query.order_by(SerialComTable.id.desc()).limit(count)
        return res


# 查询指定id的信息
def query_byID(id):
    with db.getQuery(SerialComTable) as query:
        res = query.get(id)
        return res


# 查询指定数据的上一条信息
def query_pre(id):
    with db.getQuery(SerialComTable) as query:
        res = query.get(id - 1)
        return res


def query_next(id):
    with db.getQuery(SerialComTable) as query:
        res = query.get(id + 1)
        return res


def query_assigned_ID(begin_id, end_id):
    with db.getQuery(SerialComTable) as query:
        res = query.filter(SerialComTable.id >= begin_id,
                           SerialComTable.id <= end_id).order_by(
            SerialComTable.id.desc()).all()
        return res


def queryByDate(begin_date, end_date):
    with db.getQuery(SerialComTable) as query:
        res = query(SerialComTable).filter(
            SerialComTable.record_date >= begin_date,
            SerialComTable.record_date <= end_date).order_by(
            SerialComTable.id).all()
        return res
