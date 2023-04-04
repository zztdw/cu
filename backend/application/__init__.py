

# 导入 Flask 模块
from flask import Flask
# 导入 SQLAlchemy 相关模块
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import sqlalchemy

# 创建 Flask 应用程序
app = Flask(__name__)
# 配置应用程序的 SECRET KEY
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# 创建数据库引擎对象，指定 SQLite 数据库文件的位置，并设置 check_same_thread=False 参数避免多线程问题
db_engine = create_engine('sqlite:///db.sqlite?check_same_thread=False')
# 创建自动映射基类对象
Base = automap_base()
# 使用 Base.prepare() 方法将数据库表格映射为 Python 类，并将映射好的类附加到 Base 对象上
Base.prepare(autoload_with=db_engine)
# 调用 sqlalchemy.orm.configure_mappers() 方法，配置 SQLAlchemy 的映射关系，确保所有映射关系都被正确地配置
sqlalchemy.orm.configure_mappers()
# 创建一个数据库会话对象，用于后续数据库操作
session = Session(db_engine)

# 导入 Flask 应用程序的路由信息
from application import routes