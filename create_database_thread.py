
import os
from utils.hparam import hp
from utils.print_utils import print_error, print_message, print_warning
from database.MySQLConnector import MySQLConnector
from core.STFT.STFTMusicProcessorCreate import STFTMusicProcessorCreate
import threading
import numpy as np

class MyThread(threading.Thread):

    def __init__(self, all_path):
        super(MyThread, self).__init__()
        self.all_path = all_path
        pass

    def run(self) -> None:
        create_database(self.all_path)
        pass


    pass


def create_database(all_path):

    # 获取数据库的连接
    connector = MySQLConnector()

    # 短时傅里叶变化的处理
    music_processor = STFTMusicProcessorCreate()

    # 获取到歌曲的路径
    for path in all_path:

        try:
            # 获得歌曲的路径
            # music_path = os.path.join(hp.fingerprint.path.music_path, path)
            music_path = path
            # 创建指纹并保存到数据库中
            music_processor.create_finger_prints_and_save_database(
                music_path=music_path,
            connector=connector
            )
        # 异常处理
        except BaseException as e:
            print_error("Error: " + str(path) + "\n" + str(e))
            continue

        print_message("创建完成！！！")

        pass

    pass


if __name__ == '__main__':
    # 拿到歌曲的全部路径
    path_list = []
    for path in os.listdir(hp.fingerprint.path.music_path):
        path = os.path.join(hp.fingerprint.path.music_path, path)
        path_list.append(path)

    # 把list中的内容等分为3份
    path_list = np.array_split(path_list, hp.fingerprint.thread_num)

    # 线程池
    thread_list = []
    # 一个一个的开启线程
    for path in path_list:
        t = MyThread(path)
        thread_list.append(t)

    for thread_ in thread_list:
        thread_.run()











