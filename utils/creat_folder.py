import os
from instance.app_config import local_appdata


def creat_folder_app():
    """Функция создания папки приложения в windows по пути C:\\Users\\User\\AppData\\Local\\Notebook"""
    # Создаем путь к папке программы - 'Notebook'
    program_folder = os.path.join(local_appdata, 'Notebook')
    # Создаем путь к папке для логов - 'Logs'
    log_folder = os.path.join(local_appdata, 'Notebook', 'Logs')

    # Проверяем существование папки программы
    if not os.path.exists(program_folder):
        try:
            os.makedirs(program_folder)
        except Exception as e:
            print(f'Ошибка при создании папки приложения Notebook: {e}')

    # Проверяем существование папки дл логов
    if not os.path.exists(log_folder):
        try:
            os.makedirs(log_folder)
        except Exception as e:
            print(f'Ошибка при создании папки логов Logs: {e}')
