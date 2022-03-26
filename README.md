# MusicRecognition
This is a song listening and music recognition project based on audio fingerprint algorithm.
## Installing
First of all, you should have installed MySql software, Python version 3.7 and pip.
```
pip install numpy termcolor pyaudio wave pydub librosa pymysql matplotlib
```
## How to use
There are two steps : database building and query. The songs used for database building are placed in the dataset / key directory, and the songs queried and predicted are placed in the dataset / query directory. In addition, you can also run record_ music.py file to record music clips and save them to dataset / record_music and predict them.

1. Run create_database.py to initialize your database
```
python create_database.py
```
2. Run predict.py to get the result of music recognition
```
python predict.py
```
3. Done!
### Attention
This project provides multi-threaded running mode. If you want to speed up library building and song prediction, please run create_database_thread.py and predict_thread.py
## How is it work
This project is to implement the algorithm in <<An Industrial-Strength Audio Search Algorithm>>. This paper is placed in the referPaper directory.
## Dependencies
  * Python 3.7
  * numpy
  * termcolor
  * wave
  * pydub
  * pyaudio
  * librosa
  * pymysql
  * matplotlib
  * MySql software and workbench
## Contributing
  * if you want to contribute to codes, create pull request.
  * if you find any bugs or error, create an issue.
## License
  This project is licensed under the GNU GPLv3 License
  

