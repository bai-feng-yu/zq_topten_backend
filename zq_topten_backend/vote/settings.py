import os

IP_NUM = 3      # 每天限制数
IP_TOTAL = 30    # 每阶限制数
DEVICE_NUM = 1      # 每天限制数
DEVICE_TOTAL = 30    # 每阶限制数
VOTE_MIN = 1
VOTE_MAX = 5
START_DATE = '2022-03-28' #TODO 配置项
END_DATE = '2022-04-04'
PERIOD = 7
PIC_PATH = './PIC_PATH/'
PIC_HIS_PATH = './PIC_HISTORY_PATH/'
PIC_URL = 'Photo/'
PIC_HIS_URL = 'HistoryPhoto/'
ROOT_PATH = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IP_whiteList = (
    # ('192.168.0.233', '192.168.0.233', 10, 100),  添加其为信任的IP, 信任投票次数为每天10次, 本阶段总共100次
    ('127.0.0.1', '127.0.0.1', 6, 60),
    ('59.172.0.0', '59.172.255.255', 6, 60),
    ('58.19.25.0', '58.19.25.31', 6, 60),
    ('125.220.128.0', '125.220.255.255', 6, 60),
    ('202.114.64.0', '202.114.255.255', 6, 60),
    ('183.86.194.0', '183.86.194.255', 0, 0),
    ('223.104.20.0', '223.104.20.255', 0, 0),
    ('220.202.152.0', '220.202.152.255', 0, 0),
    ('218.197.152.0', '218.197.153.255', 6, 60),
    #('113.57.0.0', '113.57.255.255', 0, 0),
)