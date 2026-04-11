        
import logging
from logging.handlers import RotatingFileHandler

def get_logger(name="backend"):
    logger = logging.getLogger(name)
    if logger.handlers:  # 已经初始化过就不重复添加 handler
        return logger

    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(
        "record.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

if __name__ == '__main__':
    # logging_config = {
    #     'filename': 'record.log',
    #     'format': "%(asctime)s | [%(levelname)s] | %(name)s | %(message)s",
    #     'datefmt': "%Y-%m-%d %H:%M:%S",
    #     'level':logging.DEBUG,

    # }
    # logging.basicConfig(**logging_config)
    # logging.debug('debug message')

    logger = logging.getLogger('backend')
    logger.setLevel(logging.DEBUG)


    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler = logging.FileHandler('record.log','a')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    print(logger.handlers)
    logger.debug('debug message')
    

