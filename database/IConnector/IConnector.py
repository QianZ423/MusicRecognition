

import abc


class IConnector(abc.ABC):


    def __init__(self):

        pass

    # 连接的方法
    @abc.abstractmethod
    def _connection(self):
        raise NotImplementedError(u"出错了，你没有实现_connection抽象方法")

    # 存储指纹
    @abc.abstractmethod
    def store_finger_prints(self, hashes, music_id_fk):
        raise NotImplementedError(u"出错了，你没有实现store_finger_prints抽象方法")

    # 保存一个指纹的方法
    @abc.abstractmethod
    def _add_finger_print(self, item, music_id_fk):
        raise NotImplementedError(u"出错了，你没有实现add_finger_print抽象方法")

    # 根据音乐的路径查找音乐
    @abc.abstractmethod
    def find_music_by_music_path(self, music_path):
        raise NotImplementedError(u"出错了，你没有实现find_music_by_music_path抽象方法")

    # 根据音乐id查找这首歌曲有多少Hash个数
    @abc.abstractmethod
    def calculation_hash_num_by_music_id(self, music_id):
        raise NotImplementedError(u"出错了，你没有实现calculation_hash_num_by_music_id抽象方法")

    # 添加歌曲
    @abc.abstractmethod
    def add_music(self, music_path):
        raise NotImplementedError(u"出错了，你没有实现add_music抽象方法")

    # 查找一个指纹
    @abc.abstractmethod
    def _find_finger_print(self, hash):
        raise NotImplementedError(u"出错了，你没有实现_find_finger_print抽象方法")

    # 查找指纹
    @abc.abstractmethod
    def find_math_hash(self, hashes):
        raise NotImplementedError(u"出错了，你没有实现find_math_hash抽象方法")

    pass