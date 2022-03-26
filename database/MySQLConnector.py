



import pymysql
from utils.hparam import hp
from database.IConnector.IConnector import IConnector


class MySQLConnector(IConnector):

    def __init__(self):
        # 调用父类的构造方法
        super().__init__()

        # 获取的数据库连接
        self.conn = None

        # 初始化游标
        self.cursor = None

        # 连接数据库，赋值游标和数据库连接
        self._connection()

        pass

    # 连接的方法
    def _connection(self):

        # 获取到mysql的连接
        self.conn = pymysql.connect(
            # 主机名
            host=hp.fingerprint.database.host,
            # 端口号
            port=hp.fingerprint.database.port,
            # 用户名
            user=hp.fingerprint.database.user,
            # 用户密码
            password=hp.fingerprint.database.password,
            # 数据库名称
            database=hp.fingerprint.database.database,
            # 字符集
            charset=hp.fingerprint.database.charset
        )

        # 游标
        self.cursor = self.conn.cursor()
        pass

    # 保存一个指纹的方法
    def _add_finger_print(self, item, music_id_fk):

        # SQL
        sql = "insert into %s(%s, %s, %s) values(%s, '%s', '%s')" % (
            hp.fingerprint.database.tables.finger_prints.name,
            hp.fingerprint.database.tables.finger_prints.column.music_id_fk,
            hp.fingerprint.database.tables.finger_prints.column.hash,
            hp.fingerprint.database.tables.finger_prints.column.offset,
            music_id_fk,
            item[0],
            item[1]
        )

        # 执行SQL语句
        self.cursor.execute(sql)
        self.conn.commit()
        pass

    # 存储指纹
    def store_finger_prints(self, hashes, music_id_fk):
        # 遍历指纹，一个一个保存到数据库（hash,offset）
        for item in hashes:
            self._add_finger_print(item=item, music_id_fk=music_id_fk)
        pass

    # 根据音乐的路径查找音乐
    def find_music_by_music_path(self, music_path):
        # SQL
        sql = "select %s from %s where %s = '%s'" % (
            # 列名
            hp.fingerprint.database.tables.music.column.music_id,
            # 表名
            hp.fingerprint.database.tables.music.name,
            # 列名
            hp.fingerprint.database.tables.music.column.music_path,
            # 传入的参数
            music_path
        )

        # 执行SQL
        self.cursor.execute(sql)
        # 拿到返回值
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]


    # 根据音乐id查找这首歌曲有多少Hash个数
    def calculation_hash_num_by_music_id(self, music_id):

        # SQL
        sql = "select count('%s') from %s where %s = %s" % (
            hp.fingerprint.database.tables.finger_prints.column.id_fp,
            hp.fingerprint.database.tables.finger_prints.name,
            hp.fingerprint.database.tables.finger_prints.column.music_id_fk,
            music_id
        )

        # 执行SQL
        self.cursor.execute(sql)

        # 拿到返回值
        result = self.cursor.fetchone()
        if result is None:
            return 0
        else:
            return result[0]

    # 添加歌曲
    def add_music(self, music_path):

        # SQL
        sql = "insert into %s(%s, %s) values ('%s', '%s')" % (
            hp.fingerprint.database.tables.music.name,
            hp.fingerprint.database.tables.music.column.music_name,
            hp.fingerprint.database.tables.music.column.music_path,
            music_path.split(hp.fingerprint.path.split)[-1],
            music_path
        )

        # 执行SQL
        self.cursor.execute(sql)
        self.conn.commit()

        # 根据music_path查找歌曲id
        music_id = self.find_music_by_music_path(music_path=music_path)
        return music_id

    # 查找一个指纹
    def _find_finger_print(self, hash):

        # SQL
        sql = "select %s, %s from %s where %s = '%s'" % (
            hp.fingerprint.database.tables.finger_prints.column.music_id_fk,
            hp.fingerprint.database.tables.finger_prints.column.offset,
            hp.fingerprint.database.tables.finger_prints.name,
            hp.fingerprint.database.tables.finger_prints.column.hash,
            hash
        )

        # 执行SQL
        self.cursor.execute(sql)

        # 拿到返回值
        result = self.cursor.fetchone()

        return result

    # 查找指纹
    def find_math_hash(self, hashes):

        # 一个一个的查找指纹，[hash, offset]
        for item in hashes:
            music_id_fk, offset_database = self._find_finger_print(item[0])

            # 待查指纹对应数据库中的歌曲id，待查指纹在数据库中的偏移，待查指纹在待查音乐片段中的偏移
            yield music_id_fk, offset_database, item[1]

            pass
        pass

    pass




