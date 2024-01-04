import os
import logging
from instance.app_config import path_to_log


# --------- Классы фильтров ----------
class DebugFilter(logging.Filter):
    def filter(self, record):
        if record.levelname == 'DEBUG':
            return True


class InfoFilter(logging.Filter):
    def filter(self, record):
        if record.levelname == 'INFO':
            return True


class WarningFilter(logging.Filter):
    def filter(self, record):
        if record.levelname == 'WARNING':
            return True


class ErrorFilter(logging.Filter):
    def filter(self, record):
        if record.levelname == 'ERROR':
            return True


# --------------- END ----------------


# Конфигурация логгера
logger_config = {
    # Версия конфигурации логгера
    'version': 1,
    # ФОРМАТЕРЫ логов
    'formatters': {
        'verbose_debug': {'format': '{levelname} | {asctime} | Filename:{filename} | {message}', 'style': '{', },
        'verbose_error': {'format': '{levelname} | {asctime} | {message} | Filename:{filename} Func:def {funcName}', 'style': '{', },
        'verbose_warning': {'format': '{levelname} | {asctime} | {message} | Filename:{filename} Func:def {funcName}', 'style': '{', },
    },
    # ОБРАБОТЧИКИ логов
    'handlers': {
        # Обработчик для записи логов в файл debug.log уровень - DEBUG
        'file_debug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose_debug',
            'filename': os.path.join(path_to_log, 'debug.log'),
            'encoding': 'utf-8',
            'filters': ['debug_filter'],
            'maxBytes': 1024 * 1024,  # Максимальный размер файла (1 мегабайт)
            'backupCount': 1,  # Количество ротируемых файлов
        },
        # Обработчик для вывода логов в консоль уровень - DEBUG
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose_debug', },
        # Обработчик для записи логов в файл error.log уровень - WARNING
        'file_warning': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'WARNING',
            'formatter': 'verbose_warning',
            'filename': os.path.join(path_to_log, 'warning.log'),
            'encoding': 'utf-8',
            'filters': ['warning_filter'],
            'maxBytes': 1024 * 1024,  # Максимальный размер файла (1 мегабайт)
            'backupCount': 1,  # Количество ротируемых файлов
        },
        # Обработчик для записи логов в файл error.log уровень - ERROR
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'verbose_error',
            'filename': os.path.join(path_to_log, 'error.log'),
            'encoding': 'utf-8',
            'filters': ['error_filter'],
            'maxBytes': 1024 * 1024,  # Максимальный размер файла (1 мегабайт)
            'backupCount': 1,  # Количество ротируемых файлов
        },
    },

    # ФИЛЬТРЫ логов
    'filters': {
        #
        'debug_filter': {'()': DebugFilter, },
        #
        'info_filter': {'()': InfoFilter, },
        #
        'warning_filter': {'()': WarningFilter, },
        #
        'error_filter': {'()': ErrorFilter, },
    },

    # ЛОГГЕРЫ
    'loggers': {
        # Логгер DEBUG
        'app_logger_debug': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_debug', 'file_error', 'file_warning'],
        },
    },
}
