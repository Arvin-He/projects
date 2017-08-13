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
    tight_torque = Column(Text)
    tight_angle = Column(Text)
    record_date = Column(DateTime)


def insert_productItem(barcode=None, tight_torque=None, tight_angle=None):
    product_data = SerialComTable(barcode=barcode,
                                  tight_torque=json.dumps(tight_torque),
                                  tight_angle=json.dumps(tight_angle),
                                  record_date=datetime.now())
    db.add(product_data)


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
                logger.info("id = ".format(product_info["id"]))
                product_info["barcode"] = res.barcode
                logger.info("barcode = ".format(res.barcode))

                tight_torque_dict = json.loads(res.tight_torque)
                logger.info("tight_torque = ".format(
                    json.loads(res.tight_torque)))
                product_info["tight_torque"] = tight_torque_dict["tight_torque"]
                tight_angle_dict = json.loads(res.tight_angle)
                product_info["tight_angle"] = tight_angle_dict["tight_angle"]
                product_info["record_date"] = res.record_date.strftime(
                    "%Y-%m-%d %H:%M:%S")
                return product_info
            else:
                return None
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
                tight_torque_dict = json.loads(res.tight_torque)
                product_info["tight_torque"] = tight_torque_dict["tight_torque"]
                tight_angle_dict = json.loads(res.tight_angle)
                product_info["tight_angle"] = tight_angle_dict["tight_angle"]
                product_info["record_date"] = res.record_date.strftime(
                    "%Y-%m-%d %H:%M:%S") if res else None
                return product_info
            else:
                return None
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
        res = query(SerialComTable).filter(SerialComTable.record_date >= begin_date,
                                           SerialComTable.record_date <= end_date).order_by(
            SerialComTable.id).all()
        return res


# def updateProductItem():
#     with basic.db.getQuery(ProductInfoTable) as query:
#         res = query.order_by(ProductInfoTable.id.desc()).first()
#         assert res is not None
#         last_gross_count = res.gross_count
#         last_sum_time = res.all_process_time
#         if res:
#             res.gross_count = getGrossCount(last_gross_count)
#             res.all_process_time = getAllProcessTime(last_sum_time)
#             res.end_time = getProcessEndTime()
#             if isCoordinationChanged():
#                 coords = json.loads(res.coordination)
#                 coord = coordinationInfo()
#                 coords.append(coord)
#                 res.coordination = json.dumps(coords)


# def updateProductName(item_id, value):
#     with basic.db.getQuery(ProductInfoTable) as query:
#         query.filter(ProductInfoTable.id == item_id).update(
#                 {ProductInfoTable.product_name: value})


# def updateWasteCount(item_id, value):
#     with basic.db.getQuery(ProductInfoTable) as query:
#         query.filter(ProductInfoTable.id == item_id).update(
#                 {ProductInfoTable.waste_count: value})


# def updateClipFile(item_id, value):
#     with basic.db.getQuery(ProductInfoTable) as query:
#         query.filter(ProductInfoTable.id == item_id).update(
#                 {ProductInfoTable.clip_file: value})
