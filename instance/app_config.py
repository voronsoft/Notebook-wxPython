import os

# Получаем корневую директорию проекта
root_directory = os.getcwd()

# Путь к иконкам
icons_folder_path = os.path.join(root_directory, "icons")

# Путь к изображениям для HTML
img_folder_path = os.path.join(root_directory, 'img')

# Путь к файлу с восстановлением БД в исходное состояние
upd_db_folder_path = os.path.join(root_directory, "db", "data_add_db")

# ============ БД ===========
# Получаем путь к локальной папке AppData для Windows
local_appdata = os.getenv('LOCALAPPDATA')

# Путь к файлу БД
path_to_DB = os.path.join(local_appdata, 'Notebook', 'db_notebook.db')
# ============ БД ===========

# ============ Логи ===========
# Путь к папке с логами
path_to_log = os.path.join(local_appdata, 'Notebook', 'Logs')
# C:\Users\User\AppData\Local\Notebook\Logs
# ============ Логи ===========
