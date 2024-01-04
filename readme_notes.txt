-- Создать файл с установленными зависимостями
pip freeze > requirements.txt

-- Проект разработан на Python 3.11 (Windows 11)

-- Собираем .exe файл
Вводим команду в консоль:
pyinstaller app.spec (файл с настройками для сборки)
Файл app.spec служит для настройки компиляции питон кода приложения в самостоятельный файл .exe
Готовый файл будет .exe расположен в папке проекта dist/

-- Папка /notebook_setup содержит файл Notebook_setup.iss для сборки setup файла программой Inno Setup Compiler 6.2
!!! Файл Notebook_setup.iss имеет кодировку windows-1251 (Этого требует программа Inno Setup Compiler 6.2)
В фале Notebook_setup.iss в строке 12 #define MyFolder "C:\Users\Nirik\Desktop\notebook_setup"
Необходимо указать путь к папке/месту в которую будет сохранён готовый setup файл  (Notebook-setup-1.0.exe)

-- Логирование
/logs - Функционал логинга
/log_data_files - Папка с сообщениями по уровням сообщений.
    debug.log: - Файл для отладочных сообщений.
    info.log: - Файл для информационных сообщений.
    warning.log: - Файл для предупреждений.
    error.log: - Файл для сообщений об ошибках.
    critical.log: - Файл для критических сообщений.