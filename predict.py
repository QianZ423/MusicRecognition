

from core.STFT.STFTMusicProcessorPredict import STFTMusicProcessorPredict
from database.MySQLConnector import MySQLConnector
from utils.hparam import hp
import os
from utils.print_utils import print_error, print_message, print_warning




def predict():

    # 获取数据库的连接
    connector = MySQLConnector()
    # 获取核心的预测处理器
    music_processor = STFTMusicProcessorPredict()


    # 一个一个的预测数据
    for path in os.listdir(hp.fingerprint.path.query_path):

        try:
            # 获取音乐的相对路径
            music_path = os.path.join(hp.fingerprint.path.query_path, path)

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
    predict()