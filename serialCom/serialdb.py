# -*- encoding:utf-8 -*-

from database import db
# from sqlalchemy import Column, Integer, DateTime, String, Text, JsonType, Float
from sqlalchemy import Column, Integer, DateTime, String, JsonType, Float


class SerialComTable(db.BaseModel):
    __tablename__ = "serialdata"
    id = Column(Integer, primary_key=True)
    barcode = Column(String(64))
    # tight_torque = Column(Float)
    # tight_angle = Column(Float)
    tight_torque = Column(JsonType)
    tight_angle = Column(JsonType)
    record_time = Column(DateTime)


with db.getQuery(SerialComTable) as query:
    res = query.all()
    print(res)



# import os, logging, json
# from datetime import datetime, timedelta
# from sqlalchemy import Column, Integer, DateTime, String, Text
# from PyQt5 import QtCore

# import basic

# _logger = logging.getLogger(__name__)
# _translate = QtCore.QCoreApplication.translate


# class ProcessInfoTable(basic.BaseModel):
#     __tablename__ = "processinfo"
#     id = Column(Integer, primary_key=True)
#     nc_file = Column(String(256))
#     process_time = Column(Integer)
#     finish_time = Column(DateTime)


# class ProductInfoTable(basic.BaseModel):
#     __tablename__ = "productinfo"
#     id = Column(Integer, primary_key=True)
#     product_name = Column(String(256))
#     nc_file = Column(String(256))
#     gross_count = Column(Integer)
#     waste_count = Column(Integer)
#     all_process_time = Column(Integer)
#     begin_time = Column(DateTime)
#     end_time = Column(DateTime)
#     coordination = Column(Text)
#     clip_file = Column(String(256))
#     tool = Column(Text)


# process_tb_cfg_path = basic.absSysDataPath('ini/db/process_tb_cfg.json')
# product_tb_cfg_path = basic.absSysDataPath('ini/db/product_tb_cfg.json')


# def read_db_config(file_name):
#     if not os.path.exists(file_name):
#         _logger.warning(_translate("processinfodb", "database config file doesn't exist!"))
#         return
#     try:
#         with open(file_name, 'r', encoding='utf-8') as f:
#             data = basic.json_load(f)
#         return data
#     except Exception:
#         _logger.error(_translate("processinfodb", 'read database config data failed!'))


# process_cfg_data = read_db_config(process_tb_cfg_path)
# product_cfg_data = read_db_config(product_tb_cfg_path)


# def check_process_info_table(db_config):
#     if db_config['mode'] == "month_mode":
#         with basic.db.getQuery(ProcessInfoTable) as query:
#             res = query.order_by(ProcessInfoTable.id).first()
#             res2 = query.order_by(ProcessInfoTable.id.desc()).first()
#             if res.finish_time < res2.finish_time - timedelta(days=(db_config[db_config['mode']]['save_count']) * 30):
#                 query.filter(ProcessInfoTable.finish_time < (res2.finish_time -
#                                                              timedelta(days=(db_config[db_config['mode']][
#                                                                                  'del_count']) * 30))).delete()
#     elif db_config['mode'] == "day_mode":
#         with basic.db.getQuery(ProcessInfoTable) as query:
#             res = query.order_by(ProcessInfoTable.id).first()
#             res2 = query.order_by(ProcessInfoTable.id.desc()).first()
#             if res.finish_time < res2.finish_time - timedelta(days=db_config[db_config['mode']]['save_count']):
#                 query.filter(ProcessInfoTable.finish_time < (res2.finish_time -
#                                                              timedelta(days=db_config[db_config['mode']][
#                                                                  'del_count']))).delete()
#     elif db_config['mode'] == "count_mode":
#         with basic.db.getSession() as session:
#             item_count = session.query(ProcessInfoTable).count()
#             if item_count >= db_config[db_config['mode']]['save_count']:
#                 res = session.query(ProcessInfoTable).limit(db_config[db_config['mode']]['del_count']).all()
#                 if res:
#                     for r in res:
#                         session.delete(r)
#     elif db_config['mode'] == 'clear_mode':
#         if db_config[db_config['mode']]['is_clear']:
#             with basic.db.getSession() as session:
#                 session.query(ProcessInfoTable).delete()


# def check_product_info_table(db_config):
#     if db_config['mode'] == "count_mode":
#         with basic.db.getSession() as session:
#             item_count = session.query(ProductInfoTable).count()
#             if item_count >= db_config[db_config['mode']]['save_count']:
#                 res = session.query(ProductInfoTable).limit(db_config[db_config['mode']]['del_count']).all()
#                 if res:
#                     for r in res:
#                         session.delete(r)
#     elif db_config['mode'] == 'clear_mode':
#         if db_config[db_config['mode']]['is_clear']:
#             with basic.db.getSession() as session:
#                 session.query(ProductInfoTable).delete()


# check_process_info_table(process_cfg_data)
# check_product_info_table(product_cfg_data)


# def getNCFile():
#     nc_file = basic.programFileName()
#     # assert nc_file is not None
#     return nc_file


# # 初始计时
# init_time = 0


# def getProcessTime():
#     global init_time
#     time = basic.get_start_time_content()
#     h_m_s = time.split(":")
#     seconds_count = int(h_m_s[0]) * 3600 + int(h_m_s[1]) * 60 + int(h_m_s[2])
#     if init_time >= seconds_count:
#         spare_time = seconds_count
#         init_time = seconds_count
#     else:
#         spare_time = seconds_count - init_time
#         init_time = seconds_count
#     return spare_time


# def getProductName():
#     product_name = os.path.basename(getNCFile())
#     return product_name


# def isNewNCFile():
#     nc_file = getNCFile()
#     with basic.db.getQuery(ProcessInfoTable) as query:
#         res = query.order_by(ProcessInfoTable.id.desc()).first()
#         last_id = res.id
#         if query.order_by(ProcessInfoTable.id).count() == 1:
#             return True
#         else:
#             res2 = query.get(last_id - 1)
#             if res2.nc_file != nc_file:
#                 return True
#             else:
#                 return False


# def getGrossCount(last_gross_count=0):
#     if isNewNCFile():
#         gross_num = 1
#     else:
#         gross_num = last_gross_count
#         gross_num += 1
#     return gross_num


# def getAllProcessTime(last_sum_time=0):
#     with basic.db.getQuery(ProcessInfoTable) as query:
#         res = query.order_by(ProcessInfoTable.id.desc()).first()
#         if res:
#             if isNewNCFile():
#                 sum_process_time = res.process_time
#             else:
#                 sum_process_time = res.process_time + last_sum_time
#         return sum_process_time


# def transferCoordSYS(coord_sys):
#     if coord_sys == 1:
#         return "G54"
#     elif coord_sys == 2:
#         return "G55"
#     elif coord_sys == 3:
#         return "G56"
#     elif coord_sys == 4:
#         return "G57"
#     elif coord_sys == 5:
#         return "G58"
#     elif coord_sys == 6:
#         return "G59"
#     else:
#         return None


# def isCoordinationChanged():
#     with basic.db.getQuery(ProductInfoTable) as query:
#         res = query.order_by(ProductInfoTable.id.desc()).first()
#         if res:
#             coords = json.loads(res.coordination)
#             coord_name = []
#             for coord in coords:
#                 coord_name.append(coord['coordination'])
#             curr_coord = transferCoordSYS(basic.currentCoordSYS)
#             if curr_coord not in coord_name:
#                 return True
#             else:
#                 compare_list = []
#                 for coor in coords:
#                     if coor['x'] == basic.getIndependentOffset(basic.currentCoordSYS, 0) and \
#                                     coor['y'] == basic.getIndependentOffset(basic.currentCoordSYS, 1) and \
#                                     coor['z'] == basic.getIndependentOffset(basic.currentCoordSYS, 2):
#                         compare_list.append("same")
#                 if "same" in compare_list:
#                     return False
#                 else:
#                     return True
#         else:
#             return True


# def coordinationInfo():
#     coordination_dict = {}
#     coordination_dict['nc_file'] = basic.programFileName()
#     coordination_dict['coordination'] = transferCoordSYS(basic.currentCoordSYS)
#     coordination_dict['x'] = basic.getIndependentOffset(basic.currentCoordSYS, 0)
#     coordination_dict['y'] = basic.getIndependentOffset(basic.currentCoordSYS, 1)
#     coordination_dict['z'] = basic.getIndependentOffset(basic.currentCoordSYS, 2)
#     return coordination_dict


# def getCoordinationInfo():
#     coordination_list = []
#     coord_info = coordinationInfo()
#     coordination_list.append(coord_info)
#     return coordination_list


# def getToolInfo():
#     tool_info = basic.programToolInfo()
#     tool_list = []
#     for tool in tool_info:
#         tool_list.append(tool[(tool.find('(') + 1): tool.find(')')])
#     return tool_list


# def getProcessBeginTime():
#     with basic.db.getQuery(ProcessInfoTable) as query:
#         res = query.order_by(ProcessInfoTable.id.desc()).first()
#         begin_time = res.finish_time - timedelta(seconds=res.process_time)
#         return begin_time


# def getProcessEndTime():
#     with basic.db.getQuery(ProcessInfoTable) as query:
#         res = query.order_by(ProcessInfoTable.id.desc()).first()
#         return res.finish_time


# def insertProcessItem():
#     process_info = ProcessInfoTable(nc_file=getNCFile(), \
#                                     process_time=getProcessTime(), finish_time=datetime.now())
#     basic.db.add(process_info)


# def insertProductItem():
#     product_info = ProductInfoTable(product_name=getProductName(), nc_file=getNCFile(),
#                                     gross_count=getGrossCount(), waste_count=0,
#                                     all_process_time=getAllProcessTime(), begin_time=getProcessBeginTime(),
#                                     end_time=getProcessEndTime(), coordination=json.dumps(getCoordinationInfo()),
#                                     clip_file="", tool=json.dumps(getToolInfo()))
#     basic.db.add(product_info)


# def queryProductsID(session):
#     res = session.query(ProductInfoTable).order_by(ProductInfoTable.id.desc()).all()
#     return res


# def queryProductByID(session, begin_id, end_id):
#     res = session.query(ProductInfoTable).filter(ProductInfoTable.id >= begin_id,
#                                                  ProductInfoTable.id <= end_id).order_by(
#             ProductInfoTable.id.desc()).all()
#     return res


# def queryProductItem(session, item_id):
#     res = session.query(ProductInfoTable).get(item_id)
#     return res


# def queryByDate(session, nc_file, begin_date, end_date):
#     res = session.query(ProcessInfoTable).filter(ProcessInfoTable.nc_file == nc_file,
#                                                  ProcessInfoTable.finish_time >= begin_date,
#                                                  ProcessInfoTable.finish_time <= end_date).order_by(
#             ProcessInfoTable.id).all()
#     return res


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
