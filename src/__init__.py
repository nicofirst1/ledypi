import logging
import os
import pathlib

LOG_DIR = str(pathlib.Path(__file__).parent.absolute())
LOG_DIR += "/logs"

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
logging.basicConfig(format=formatter)

loggers = dict(
    rpi="rpi_logger",
    patterns="pattern_logger",
    firebase="firebase_logger",
)

loggers = {k: logging.getLogger(v) for k, v in loggers.items()}

for k, v in loggers.items():
    fileHandler = logging.FileHandler(f"{LOG_DIR}/{k}.log")
    fileHandler.setFormatter(formatter)
    v.addHandler(fileHandler)


def change_level(new_level, spec=None):
    """
    Change the level of a loggers
    :param new_level: logging.level, a logging level
    :param spec: list[str], list of loggers keys, if None the change all
    :return: None
    """
    if spec is None:
        for v in loggers.values():
            v.setLevel(new_level)
    else:
        if not isinstance(spec, list): spec = list(spec)
        for k in spec:
            loggers[k].setLevel(new_level)
