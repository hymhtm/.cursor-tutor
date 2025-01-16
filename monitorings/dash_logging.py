import logging

logging.basicConfig(
    filename='monitorings.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#create a file handler
file_handler = logging.FileHandler('monitorings.log')
file_handler.setLevel(logging.DEBUG)

#create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

#add the handler to the logger
logger.addHandler(file_handler)