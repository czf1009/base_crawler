import config
import pymysql
import aiomysql


def connect_mysql():
    """
    Connect mysql and return conn,cur
    """
    conn = pymysql.connect(
        config.IP,
        user=config.USER,
        password=config.PASSWD,
        db=config.DB_NAME,
        charset='utf8mb4'
    )
    # except pymysql.Error as e:
    # raise SystemExit('Mysql Error %d: %s' % (e.args[0], e.args[1]))
    cur = conn.cursor()
    conn.ping(True)
    conn.autocommit(0)
    return conn, cur


async def connect_aiomysql(loop):
    """
    Connect mysql by aiomysql and return conn,cur
    """
    conn = await aiomysql.connect(
        host=config.IP, port=3306,
        user=config.USER, password=config.PASSWD,
        db=config.DB_NAME, loop=loop,
        charset='utf8mb4'
    )
    cur = await conn.cursor()
    return conn, cur
