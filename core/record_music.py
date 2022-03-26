

import argparse
from argparse import RawTextHelpFormatter
from core.listener import Listener

# 收听其他设备录制的音乐片段并保存到dataset/record_music目录下

def get_audio():

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-s', '--seconds', nargs='?')
    args = parser.parse_args()

    if not args.seconds:
        args.seconds = "7"

    seconds = int(args.seconds)

    chunksize = 2**12
    channels = 1
    record_forever = False

    listener = Listener()

    listener.start_recording(
        seconds=seconds,
        chunksize=chunksize,
        channels=channels
    )

    while True:
        bufferSize = int(listener.rate / listener.chunksize * seconds)
        print("正在录音......")
        for i in range(0, bufferSize):
            number = listener.process_recording()

        if not record_forever:break

    print("录音停止......")
    listener.stop_recording()

    listener.save_recorded("../dataset/record_music/xxx.mp3")


    return './xxx.mp3'

path = get_audio()
print(path)