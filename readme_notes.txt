-- Создать файл с установленными зависимостями
    pip freeze > requirements.txt

-- Проект разработан на Python 3.11 (Windows 11)

-- Собираем .exe файл
    Вводим команду в консоль:
    pyinstaller app.spec (файл с настройками для сборки)
    Файл app.spec служит для настройки компиляции питон кода приложения в самостоятельный файл .exe
    Готовый файл .exe будет расположен в папке проекта dist/

-- Папка /notebook_setup содержит файл Notebook_setup.iss сценарий для сборки setup файла программой Inno Setup Compiler 6.2
    !!! Файл Notebook_setup.iss имеет кодировку windows-1251 (Этого требует программа Inno Setup Compiler 6.2)
    В фале Notebook_setup.iss в строке 12 #define MyFolder "C:\Notebook-wxPython\notebook_setup"
    Необходимо указать путь к папке/месту в которую будет сохранён готовый setup файл  (Notebook-setup-1.0.exe)

-- Логирование
    /logs - Функционал логинга
    Папка Logs для файлов логирования создается по пути - C:\Users\User\AppData\Local\Notebook\Logs

-- База Данных
    Файл БД располагается по пути  - C:\Users\Nirik\AppData\Local\Notebook\db_notebook.db