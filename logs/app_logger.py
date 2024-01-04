import logging
import logging.config
from logs.config_logger import logger_config
from utils.creat_folder import creat_folder_app


# Так как логгер загружается первым в приложении
# для его корректной работы нужно создать папку Logs для запуска конфигурации
creat_folder_app()

# Задаем конфигурацию логгеру
logging.config.dictConfig(logger_config)
# Получение объекта логгера из файла конфигурации
logger_debug = logging.getLogger('app_logger_debug')
