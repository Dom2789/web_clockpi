import logging

def setup_logging(path_logfile:str, debug = False):
    
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        filename = path_logfile + "openweatherAPI.log",
        level = level,
        style = "{",
        format = "{asctime} {levelname:8}] {message}",
        datefmt = "%d.%m.%Y %H:%M:%S"
     )
