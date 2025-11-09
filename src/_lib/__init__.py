from _lib.Config import config
import _lib.logger

# custom functions
path = config.get_path_prot()
_lib.logger.setup_logging(path)