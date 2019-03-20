import logging
from util import pad
from datetime import datetime

def setup(prefix):
    now = datetime.now()
    year = pad.two(now.year)
    month = pad.two(now.month)
    day = pad.two(now.day)
    hour = pad.two(now.hour)
    minute = pad.two(now.minute)
    second = pad.two(now.second)
    LOG_FILENAME = f'Logs\\{prefix}_{year}{month}{day}{hour}{minute}{second}.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

def exe(log):
    logging.info(log)

def now():
    return datetime.now()