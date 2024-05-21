import pymysql


# 步骤：
# 1.安装MYSQL数据库软件；
# 2.在pycharm中的库接口设置中安装pymysql；
# 3.安装Navicat，便于可视化操作数据库;
# 4.打开数据库连接,安装MySQL数据库时，设置了数据库用户名：root;密码为：824626


class Mysql(object):

    def __init__(self, db_name, *group):
        self.db_name = "兵棋数据库"
        self.table_name = "算子数据表"
        self.conn = pymysql.connect(
            host="localhost",  # 主机名称或者用127.0.0.1
            port=3306,
            user="root",
            passwd="990228",
            db=db_name,  # 在navicat中定义的数据库名称
            charset='utf8'
        )
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.conn.cursor()
        # 使用 execute()  方法执行 SQL 查询
        self.cursor.execute("SELECT VERSION()")
    
    def insert(self, sql, *data):
        # 将data中数据插入到mysql数据库中move_history表格中
        try:
            self.cursor.executemany(sql, data)
            self.conn.commit()  # 统一提交数据
            # 使用 fetchone() 方法获取单条数据.
            # print("读取数据： %s " % data)
        except Exception as e:
            self.conn.rollback()
            print('Failed:', e)
    
    def close_db(self):
        # 关闭数据库连接
        self.cursor.close()
        self.conn.close()
    
    def creat_table(self):
        pass
    
    def delete_data(id):
        pass
