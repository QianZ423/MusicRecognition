

from core.STFT.STFTMusicProcessorPredict import STFTMusicProcessorPredict
from database.MySQLConnector import MySQLConnector
from utils.hparam import hp
import os
from utils.print_utils import print_error, print_message, print_warning
import numpy as np
import threading


class MyThread(threading.Thread):

    def __init__(self, all_path):
        super(MyThread, self).__init__()
        self.all_path = all_path
        pass

    def run(self) -> None:
        predict(self.all_path)
        pass


    pass


def predict(all_path):

    # 获取数据库的连接
    connector = MySQLConnector()
    # 获取核心的预测处理器
    music_processor = STFTMusicProcessorPredict()


    # 一个一个的预测数据
    for path in all_path:

        try:
            # 获取音乐的相对路径
            # music_path = os.path.join(hp.fingerprint.path.query_path, path)
            music_path = path
            # 预测歌曲
            music_info = music_processor.predict_music(music_path=music_path, connector=connector)

            # 根据music_info输出
            print_message("预测歌曲：" + str(music_info['music_id']) + ", --- 线性匹配的Hash个数为：" + str(music_info['max_hash_count']) + ", --- 歌曲偏移：" + str(music_info['music_offset']))


            pass
        except BaseException as e:
            print_error("Error: " + str(path) + "\n" + str(e))
            continue
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