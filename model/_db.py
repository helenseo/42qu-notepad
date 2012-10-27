#coding:utf-8


# 初始化数据连接
import _env
import MySQLdb
from DBUtils.PersistentDB  import PersistentDB as DB
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB
def _connection(*args, **kwds):
    kwds['maxusage'] = False
    persist = DB (MySQLdb, *args, **kwds)
    conn = persist.connection()
    return conn

connection = _connection(
    host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB, charset='utf8'
)

try:
    from sae.kvdb import KVClient
    kv = KVClient()
except:
    from kvstore import kv
