import logging
import sys

format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
logging.basicConfig(format=format)

fire_logger = logging.getLogger("fire_logger")
handler = logging.StreamHandler(sys.stdout)
fire_logger.addHandler(handler)
