import logging
import datetime

logger = logging.getLogger('client')
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s ")
date = datetime.datetime.now()
fh = logging.FileHandler("client.log", encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    pass
