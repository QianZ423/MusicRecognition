

from utils.print_utils import print_error,print_message,print_warning
import numpy as np
import librosa
from utils.hparam import hp
from core.ICore.IMusicProcessorCreate import IMusicProcessorCreate



class STFTMusicProcessorCreate(IMusicProcessorCreate):

    # 创建指纹并且保存到数据库中
    def create_finger_prints_and_save_database(self, music_path, connector):
        '''
        创建指纹并且保存到数据库中
        :param music_path: 音乐路径
        :param connector: 连接数据库的
        :return: 无
        '''
        # 先查询看看数据库中是否有这首歌
        music_id = connector.find_music_by_music_path(music_path=music_path)

        # 如果数据库中没有这首歌
        if music_id is None:
            # 添加歌曲，拿到歌曲id
            music_id = connector.add_music(music_path)

            # 计算Hash
            hashes = list(self._calculation_hash(music_path=music_path))

            # 将Hash值保存到数据库中
            connector.store_finger_prints(hashes=hashes, music_id_fk=music_id)

            # 歌曲的Hash个数
            hash_num = connector.calculation_hash_num_by_music_id(music_id=music_id)
            # 打印提示信息
            print_message("歌曲：" + str(music_id) + " 添加成功! \nHash数目为：" + str(hash_num) + "\n")
            pass
        # 如果数据库中有这首歌
        else:
            # 计算这首歌曲的Hash个数
            hash_num = connector.calculation_hash_num_by_music_id(music_id=music_id)
            print_warning("这首歌曲 " + str(music_id) + " 已经存在，一共有" + str(hash_num) + "条Hash!!!")
            pass


        pass


    # 计算指纹
    def _calculation_hash(self, music_path):
        '''
        计算指纹
        :param music_path: 音乐的路径
        :return: 指纹 [(hash,t1), (hash,t1)...]
        '''
        # 音乐的预处理，转为频谱图(频谱矩阵)
        spectrogram = self._pre_music(music_path)

        # 处理频谱图
        spectrogram = self._spectrogram_handle(spectrogram)

        # 通过频谱图得到peakes
        peakes = self._fingerprint(spectrogram)

        # 通过peakes得到Hash并返回
        return self._generate_hash(peakes)


    # 音乐的预处理，转为频谱图(频谱矩阵)
    def _pre_music(self, music_path):
        '''
        音乐的预处理，转为频谱图(频谱矩阵)
        :param music_path: 音乐的路径
        :return: 频谱图
        '''
        # 加载歌曲
        y, sr = librosa.load(music_path, sr=hp.fingerprint.core.stft.sr)

        # 做短时傅里叶变化
        arr2D = librosa.stft(y,
                             n_fft=hp.fingerprint.core.stft.n_fft,
                             hop_length=hp.fingerprint.core.stft.hop_length,
                             win_length=hp.fingerprint.core.stft.win_length
                             )

        # 返回的是（频率，时间）
        return np.abs(arr2D)


