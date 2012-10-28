#coding:utf-8


# 初始化数据连接
import _env
import MySQLdb
from DBUtils.PersistentDB  import PersistentDB as DB
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB, DISABLE_LOCAL_CACHED
def _connection(*args, **kwds):
    kwds['maxusage'] = False
    persist = DB (MySQLdb, *args, **kwds)
    conn = persist.connection()
    return conn

connection = _connection(
    host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB, charset='utf8'
)
try:
    import sae.const
except ImportError:
    import cmemcached
    from config import MEMCACHED_ADDR
    kw = {}
    kw['comp_threshold'] = 4096
    mc = cmemcached.Client(MEMCACHED_ADDR)
else:
    import pylibmc
    mc = pylibmc.Client()


try:
    from sae.kvdb import KVClient
    kv = KVClient()
    _set_ = kv.set
    def set(key, val, time=0, min_compress_len=1024):
        _set_(key, val, time, min_compress_len)
    kv.set = set 
except ImportError:
    from kvstore import kv

from zorm_sae.mc_connection import init_mc
import zorm_sae.config 

zorm_sae.config.mc = mc = init_mc(
    mc,
    disable_local_cached=DISABLE_LOCAL_CACHED
)

from zorm_sae.mc import McCacheM, McCache, McNum, McCache, McLimitA, McCacheA, McLimitM

if __name__ == "__main__":
    pass
