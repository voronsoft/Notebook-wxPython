"""Файл для создания БД db-notebook (sqlite3)"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from instance.app_config import path_to_DB, local_appdata
from db.models import Base, Module, Command, CommandModuleAssociation
from logs.app_logger import logger_debug


def create_database():
    """Создание базы данных"""

    # Создаем путь к папке программы и файлу БД
    program_folder = os.path.join(local_appdata, 'Notebook')
    # Создаем путь к папке для логов
    log_folder = os.path.join(local_appdata, 'Notebook', 'Logs')

    # Проверяем существование папки программы, если нет - создаем
    if not os.path.exists(program_folder):
        os.makedirs(program_folder)
        # Добавляем папку для логов
        os.makedirs(log_folder)

    # Создаем соединение с базой данных
    engine = create_engine(f'sqlite:///{path_to_DB}', echo=False)  # Создаем соединение с базой данных echo=False отключит вывод запросов в консоль
    logger_debug.debug(f'Бд db_notebook.db создана по пути: sqlite:///{path_to_DB}')

    # Создаем сессию для взаимодействия с базой данных
    Session = sessionmaker(bind=engine)
    with Session() as session:
        try:
            # Создаем таблицы в базе данных
            Base.metadata.create_all(engine)
            # Сохранение изменений в базе данных
            session.commit()
            logger_debug.debug("Бд db_notebook.db создана")
        except Exception as e:
            logger_debug.exception(f'{e}')
            session.rollback()  # Откатываем изменения в случае ошибки


def read_file(file_path=None):
    """Считывание файла с данными"""
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = [i.strip().split(':') for i in file.readlines()]
            name_modul_descr = data.pop(0)
            return name_modul_descr, data
    else:
        logger_debug.debug(f'Путь к файлу не указан!')


def added_command_data_db(path_file_data=None):
    """
    Добавление данных в таблицы БД
    :param path_file_data: path from file data
    """

    if not path_file_data:
        logger_debug.debug(f'Не указан путь к файлу данных!')
        return

    # Получаем данные из файла (название модуля, перечень команд с описанием)
    data_temp = read_file(path_file_data)
    name_modul, modul_description = data_temp[0][0], data_temp[0][1]  # Название модуля (первая строка!!)
    data_list = list(*data_temp[1:])  # Список команд

    # Создаем соединение с базой данных
    engine = create_engine(f'sqlite:///{path_to_DB}', echo=False)  # Создаем соединение с базой данных echo=False отключит вывод запросов в консоль
    # Создаем сессию для взаимодействия с базой данных
    Session = sessionmaker(bind=engine)

    with Session() as session:
        if name_modul:
            # Добавление модуля в БД
            try:
                # Проверяем есть ли модуль в БД
                existing_module = session.query(Module).filter_by(module_name=name_modul).first()
                if not existing_module:  # Если нет добавляем
                    module = Module(module_name=name_modul, description=modul_description)
                    session.add(module)
                    session.commit()
                    logger_debug.debug(f'Модуль {name_modul} создан.')
            except Exception as error:
                logger_debug.exception(f'Ошибка при добавлении Модуля в БД (Module таблица):\n{str(error)}')
                session.rollback()  # Откатываем изменения в случае ошибки

            # Добавление команды в БД
            try:
                # Добавляем команды в таблицу
                for line in data_list:
                    name, desc = line[0], line[1]
                    # Проверяем есть ли команда в БД
                    existing_command = session.query(Command).filter_by(command_name=name).first()
                    if not existing_command:  # Если нет добавляем
                        command = Command(command_name=name, description=desc)
                        session.add(command)
                        session.commit()
                        logger_debug.debug(f'Команда {name} добавлена.')
                        # Добавляем связи модуль - команда (таблицы command_module_association)
                        try:
                            modul = session.query(Module).filter_by(module_name=name_modul).first()
                            command = session.query(Command).filter_by(command_name=name).first()
                            association = CommandModuleAssociation(command_id=command.id, module_id=modul.id)
                            session.add(association)
                            session.commit()
                            logger_debug.debug(f'Связь модуль {modul.module_name}({modul.id}) - ({command.id}){command.command_name} команда добавлена')
                        except Exception as error:
                            logger_debug.exception(f'Ошибка при добавлении связи в БД (command_module_association - таблица):\n{str(error)}')
                            session.rollback()  # Откатываем изменения в случае ошибки
            except Exception as error:
                logger_debug.exception(f'Ошибка при добавлении данных в БД (Общая):\n{str(error)}')
                session.rollback()  # Откатываем изменения в случае ошибки
        else:
            logger_debug.debug(f'Не указано название модуля в файле !')


if __name__ == '__main__':
    # Создаем БД
    create_database()
    # Добавляем команды к модулям
    # ВАЖНО !! Первая строка в файлах с командами указывает на принадлежность к модулю
    # Остальные строки это команды
    added_command_data_db('data_add_db/list_data_add_db.txt')  # list
    added_command_data_db('data_add_db/string_data_add_db.txt')  # string
    added_command_data_db('data_add_db/dict_data_add_db.txt')  # dict
    added_command_data_db('data_add_db/tuple_data_add_db.txt')  # tuple
    added_command_data_db('data_add_db/set_data_add_db.txt')  # set
    added_command_data_db('data_add_db/python_func_data_add_db.txt')  # function python
    added_command_data_db('data_add_db/class_magic_methods_data_add_db.txt')  # class magic methods  python
