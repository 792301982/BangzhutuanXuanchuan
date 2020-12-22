import pymysql

Admin = """
create table if not exists Admin(
    id INT NOT NULL auto_increment PRIMARY KEY,  
    username varchar(100) not null,
    password varchar(100) not null
    )
"""

First_admin = """INSERT INTO Admin(username,password) VALUES ("%s","%s")
""" % (
    'admin', '123456',
)

Form ="""
create table if not exists Form(
    id INT NOT NULL auto_increment PRIMARY KEY,  
    text varchar(500) not null,
    name varchar(10) not null,
    phonenumber varchar(20) not null,
    email varchar(20) not null,
    address varchar(100) not null
    )
"""

class Sql:
    def __init__(self):
        self.db = pymysql.connect(host='134.175.156.189',  # 指定连接本地服务器
                                  user='root',    # 登录服务器 用的用户名
                                  password='yangning',  # 登录服务器用的密码
                                  database='bangzhutuan',    # 指定目标数据库
                                  charset='utf8')
        # 规定返回的值为字典类型，否则默认返回元组类型
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        # 关闭数据库连接
        self.db.close()

    def sqlstr(self, sql_str):
        try:
            # 执行sql语句
            self.cursor.execute(sql_str)
            # 提交到数据库执行
            self.db.commit()
        except Exception as err:
            # 如果发生错误则回滚
            self.db.rollback()
            raise err

    def search(self, sql_str):
        try:
            # 执行SQL语句
            self.cursor.execute(sql_str)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results
        except Exception as err:
            self.db.rollback()
            raise err


if __name__ == "__main__":
    '''
    建表
    '''
    s = Sql()
    try:
        # 执行sql语句
        s.cursor.execute(Form)
        s.cursor.execute(Admin)
        s.cursor.execute(First_admin)

        # 提交到数据库执行
        s.db.commit()
    except Exception as err:
        # 如果发生错误则回滚
        s.db.rollback()
        raise err