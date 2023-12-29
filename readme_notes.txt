-- создать файл с установленными зависимостями
pip freeze > requirements.txt

-- Проект разработан на Python 3.11 (Windows 11)

-- Собираем .exe файл
Вводим команду в консоль:
pyinstaller app.spec

-- Папка notebook_setup содержит файл Notebook_setup.iss для сборки setup файла программой Inno Setup Compiler 6.2
!!! Файл Notebook_setup.iss имеет кодировку windows-1251 (того требует программа Inno Setup Compiler 6.2)
