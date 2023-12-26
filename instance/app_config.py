import os

# Получаем корневую директорию проекта
root_directory = os.getcwd()

# Путь к иконкам
icons_folder_path = os.path.join(root_directory, "icons")

# Путь к изображениям для HTML
img_folder_path = os.path.join(root_directory, 'html', 'img')

# Путь к файлу с восстановлением БД в исходное состояние
upd_db_folder_path = os.path.join(root_directory, "db", "data_add_db")

# Путь к файлу БД
path_to_DB = os.path.join(root_directory, 'db', 'db_notebook.db')
