
import librosa
from core.ICore.IMusicProcessorPredict import IMusicProcessorPredict
from utils.hparam import hp
import numpy as np
from utils.data_utils import start_time, end_time
import matplotlib.pyplot as plt


class STFTMusicProcessorPredict(IMusicProcessorPredict):

    # 预测歌曲
    def predict_music(self, music_path, connector):
        # 计算Hash
        hash = list(self._calculation_hash(music_path=music_path))

        # 看是否开启了显示时间
        if hp.fingerprint.show_time:
            start = start_time()

        # 根据Hash在数据库中查找，[hash, offset]
        match_hash_list = set(connector.find_math_hash(hashes=hash))

        if hp.fingerprint.show_plot.predict_plot.hash_plot:
            self._show_line_plot(match_hash_list)

        # 看是否开启了显示时间
        if hp.fingerprint.show_time:
            end_time(start,'在数据库中查找花费的时间')

        return self._align_match(match_hash_list=match_hash_list)

    # 匹配的核心
    def _align_match(self, match_hash_list):
        # 待查指纹对应数据库中的歌曲id，待查指纹在数据库中的偏移，待查指纹在待查音乐片段中的偏移

        # 最终返回的歌曲id
        music_id = -1
        # 最终返回的歌曲的偏移
        music_offset = -1
        # 最终返回的查找到匹配的Hash个数
        max_hash_count = -1

        # 保存返回的结果
        result = {}

        for matches in match_hash_list:
            # 拿到音乐的id, 数据库中的偏移，查询片段自身的偏移
            music_id_fk, offset_database, offset_query = matches

            # 计算数据库中音乐的偏移和查询片段自身的偏移之间的差值
            offset = int(int(offset_database) - int(offset_query))

            # 如果offset不存在字典里，则添加进去
            if offset not in result:
                result[offset] = {}

            if music_id_fk not in result[offset]:
                result[offset][music_id_fk] = 0

            # 统计在当前偏移下，歌曲的出现次数
            result[offset][music_id_fk] += 1

            if result[offset][music_id_fk] > max_hash_count:
                # 更新max_hash_count的值
                max_hash_count = result[offset][music_id_fk]
                # 赋值歌曲id
                music_id = music_id_fk
                # 赋值歌曲的offset
                music_offset = offset
                pass
            pass


            pass

        return {
            "music_id":music_id,
            "music_offset":music_offset,
            "max_hash_count":max_hash_count
        }


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



    pass

    # 绘制线性关系的图
    def _show_line_plot(self, match_hash):

        c = [item[0] for item in match_hash]

        x_and_y = [(item[1], item[2]) for item in match_hash]

        x = [int(item[0]) for item in x_and_y]
        y = [int(item[0]) for item in x_and_y]

        plt.scatter(x, y, c=c, marker='o')
        plt.show()

        pass