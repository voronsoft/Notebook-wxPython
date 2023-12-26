-- создать файл с установленными зависимостями
pip freeze > requirements.txt

-- Проект разработан на Python 3.11 (Windows 11)

-- Собираем .exe файл
Вводим команду в консоль
pyinstaller app.spec

pyinstaller --onefile --add-data "html;." --add-data "icons;." --add-data "db;." ваш_основной_скрипт.py

