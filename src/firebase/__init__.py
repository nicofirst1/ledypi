import logging
import sys

fire_logger = logging.getLogger("fire_logger")
fire_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s\n')
handler.setFormatter(formatter)
fire_logger.addHandler(handler)