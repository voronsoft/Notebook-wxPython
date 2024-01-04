import os
from instance.app_config import path_to_log


def logs_files():
    """Функция получения списка файлов логирования из папки логов"""
    # Проверяем существование папки для логов
    if os.path.exists(path_to_log):
        # Получаем список файлов в папке
        files_in_folder = os.listdir(path_to_log)
        # Выводим список файлов
        print("Список файлов в папке:", files_in_folder)
        return files_in_folder
    else:
        return []
