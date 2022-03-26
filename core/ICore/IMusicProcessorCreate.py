
import abc
from core.ICore.IMusicProcessor import IMusicProcessor



class IMusicProcessorCreate(IMusicProcessor):

    # 创建指纹并保存到数据库中的接口
    @abc.abstractmethod
    def create_finger_prints_and_save_database(self, music_path, connector):
        raise NotImplementedError(u"出错了，你没有实现create_finger_prints_and_save_database抽象方法")


    # 处理指纹
    @abc.abstractmethod
    def _calculation_hash(self, music_path):
        raise NotImplementedError(u"出错了，你没有实现_calculation_hash抽象方法")

    # 音乐的预处理，转为频谱图(频谱矩阵)
    @abc.abstractmethod
    def _pre_music(self, music_path):
        raise NotImplementedError(u"出错了，你没有实现_pre_music抽象方法")


    pass








