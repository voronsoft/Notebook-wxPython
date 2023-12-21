import os
from db.models import Module, Command
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func

# Получаем корневую директорию проекта
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Строим путь к файлу базы данных
path_to_DB = os.path.join(root_directory, 'db', 'db_notebook.db')  # Путь к БД относительно вызова функции

engine = create_engine(f'sqlite:///{path_to_DB}', echo=True)  # Создаем соединение с базой данных
Session = sessionmaker(bind=engine)  # Создаем сессию для взаимодействия с базой данных


# Функция получения данных о модулях
def request_to_get_all_modules():
    """Получение списка модулей из БД"""
    with Session() as session:
        try:
            modules = session.query(Module).all()  # Выполняем запрос ко всем модулям
            # Преобразуем результат в список словарей для удобства использования
            modules_data = []
            for module in modules:
                data = {'id': module.id,
                        'module_name': module.module_name,
                        'description': module.description
                        }
                modules_data.append(data)
            return modules_data

        except Exception as e:
            # Обрабатываем возможные ошибки, например, выводим сообщение об ошибке
            print(f"Ошибка при получении списка модулей: {e}")
            return []


# Функция получения объект-модуля по названию
def request_get_module(name_mod_str):
    """
    Получение объекта-модуля по названию
    :param name_mod_str: - название модуля (str)
    :return: - object module
    """
    with Session() as session:
        try:
            # Получаем объект-модуля
            module_obj = session.query(Module).filter_by(module_name=name_mod_str).first()
            if module_obj:
                return module_obj
            else:
                return False
        except Exception as e:
            # Выводим сообщение об ошибке
            print(f"Ошибка при получении объекта-модуля: {e}")
            return 'error'


# Функция получение списка команд исходя из названия модуля (modul_name)
def request_get_commands(modul_name):
    """
    Получение списка команд исходя из названия модуля (modul_name).
    :param modul_name: - название (str)
    :return: - список команд (obj)
    """
    with Session() as session:
        try:
            # Если modul_name задан, фильтруем команды по ассоциированным модулям
            commands = session.query(Command).join(Command.modules).filter(Module.module_name == modul_name).all()
            # Преобразуем результат в список словарей для удобства использования
            commands_data = []
            for command in commands:
                data = {
                    'id': command.id,
                    'commands_name': command.command_name,
                    'description_command': command.description,
                    'command_example:': command.example,
                    'cmd_assoc_module': tuple(*[(module.module_name, module.id) for module in command.modules])
                }
                commands_data.append(data)
            return commands_data

        except Exception as e:
            # Обрабатываем возможные ошибки, например, выводим сообщение об ошибке
            print(f"Ошибка при получении списка команд: {e}")
            return []


# Функция получения КОЛИЧЕСТВА команд связанных с модулем
def count_commands_in_module(module_name):
    """Получение количества команд исходя из названия модуля (module_name)."""
    with Session() as session:
        try:
            # Фильтруем команды по ассоциированным модулям, если указан module_name
            count = session.query(func.count(Command.id)).join(Command.modules).filter(Module.module_name == module_name).scalar()
            return count if count is not None else 0

        except Exception as e:
            # Обрабатываем возможные ошибки, например, выводим сообщение об ошибке
            print(f"Ошибка при получении количества команд: {e}")
            return 0


# Функция для выполнения запроса для получения данных о конкретной команде
def show_full_command_info(command_name=None):
    """
    Получение полной информации о команде из БД
    :param command_name: - название команды (str)
    :return: - command details (dict)
    """
    with Session() as session:
        try:
            if command_name:
                existing_command = session.query(Command).filter_by(command_name=command_name).first()
                if not existing_command:  # Проверяем есть ли команда
                    return 'Команда не найдена (нет совпадений, проверьте написание)'

                command_data = {'id': existing_command.id,
                                'commands_name': existing_command.command_name,
                                'description_command': existing_command.description,
                                'command_example:': existing_command.example,
                                'cmd_assoc_module': tuple(*[(module.module_name, module.id) for module in existing_command.modules])
                                }
                return command_data

        except Exception as e:
            # Обрабатываем возможные ошибки, например, выводим сообщение об ошибке
            print(f"Ошибка при получении полных данных о команде: {e}")
            return []


# Функция добавления новой КОМАНДЫ
def add_command(name_cmd, description, example, module_obj):
    """
    Функция добавления новой КОМАНДЫ
    :param name_cmd: - имя команды (str)
    :param description: - описание команды (str)
    :param example: - пример описания (str)
    :param module_obj: - модуль (для связи) (object)
    :return: - возвращает булево значение (bool)
    """
    with Session() as session:
        try:
            # Ищем команду по имени
            existing_cmd = session.query(Command).filter_by(command_name=name_cmd).first()

            # Проверяем, найдена ли команда
            if existing_cmd is None:
                new_cmd = Command(command_name=name_cmd, description=description, example=example)

                # Если module_obj - это одиночный объект, создаем список из одного элемента
                modules_list = [module_obj] if module_obj else []

                # Связываем команду с модулями
                new_cmd.modules.extend(modules_list)

                # Добавляем команду в БД
                session.add(new_cmd)
                session.commit()  # Фиксируем

                # Возвращаем информацию о добавлении
                print(f"Команда {name_cmd} успешно добавлена в БД.")
                return True
            else:
                print(f"Команда {name_cmd} есть в БД.")
                return False
        except Exception as e:
            # Ошибка при добавлении в БД команды
            print(f"Ошибка добавления команды {name_cmd}: {e}")
            session.rollback()  # Откатываем изменения в случае ошибки
            return 'error'


# Функция изменения данных КОМАНДЫ
def edit_command(cmd=None, name_new=None, descr_new=None, example_new=None):
    """
    Функция изменения данных КОМАНДЫ
    :param cmd: - тип или dict или num
    :param name_new: - имя команды (str)
    :param descr_new: - описание команды (str)
    :param example_new: - пример описания (str)
    :return: - возвращает булево значение (bool) или 'error'
    """
    # TODO Доделать функцию изменения команды (логика записи в БД)
    with Session() as session:
        try:
            # Ищем команду по имени
            existing_command = session.query(Command).filter_by(command_name=cmd).first()

            # Проверяем, найдена ли команда
            if existing_command is not None:
                # Изменяем название, описание, пример
                existing_command.command_name = name_new  # Название
                existing_command.description = descr_new  # Описание
                existing_command.example = example_new  # Пример

                session.commit()  # Сохраняем изменения в базе данных
                return True
            else:
                return False

        except Exception as e:
            # Ошибка при изменении команды
            print(f"Ошибка при изменении команды {cmd}: {e}")
            session.rollback()  # Откатываем изменения в случае ошибки
            return 'error'


# Функция удаления КОМАНДЫ
def del_command(cmd_obj):
    """Функция удаления КОМАНДЫ из БД"""
    name_cmd = cmd_obj['commands_name']
    with Session() as session:
        try:
            # Ищем команду по имени
            existing_command = session.query(Command).filter_by(command_name=name_cmd).first()

            # Проверяем, найдена ли команда
            if existing_command:
                # Удаляем команду из БД
                session.delete(existing_command)
                session.commit()
                return True
            else:
                print(f"Команда {name_cmd} не найдена в БД.")
                return False
        except Exception as e:
            # Ошибка при удалении из БД данных о команде
            print(f"Ошибка при удалении из БД данных о команде: {e}")
            session.rollback()  # Откатываем изменения в случае ошибки
            print("Откат изменений.")
            return 'error'


# Функция добавления нового МОДУЛЯ
def add_module(name, descr):
    """Функция добавления нового МОДУЛЯ"""
    with Session() as session:
        try:
            # Ищем модуль по имени
            existing_module = session.query(Module).filter_by(module_name=name).first()

            # Проверяем, найден ли модуль
            if existing_module is None:
                new_module = Module(module_name=name, description=descr)
                # Добавляем модуль в БД
                session.add(new_module)
                session.commit()  # Фиксируем

                # Возвращаем информацию о добавлении
                print(f"Модуль {name} успешно добавлен в БД.")
                return True
            else:
                print(f"Модуль {name} есть в БД.")
                return False
        except Exception as e:
            # Ошибка при добавлении в БД модуля
            print(f"Ошибка добавлении модуля {name}: {e}")
            session.rollback()  # Откатываем изменения в случае ошибки
            return 'error'


# Функция изменения данных МОДУЛЯ
def edit_module(select_mod_name, name_new, descr_new):
    """Функция изменения данных МОДУЛЯ"""
    with Session() as session:
        try:
            # Ищем модуль по имени
            existing_module = session.query(Module).filter_by(module_name=select_mod_name).first()

            # Проверяем, найден ли модуль
            if existing_module is not None:
                # Изменяем имя и описание
                existing_module.module_name = name_new
                existing_module.description = descr_new

                # Сохраняем изменения в базе данных
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            # Ошибка при изменении модуля
            print(f"Ошибка при изменении модуля {select_mod_name}: {e}")
            session.rollback()  # Откатываем изменения в случае ошибки
            return 'error'


# Функция удаления МОДУЛЯ и связанных с ним команд.
def del_module(name_mod):
    """Функция удаления МОДУЛЯ и связанных с ним команд."""
    with Session() as session:
        try:
            # Ищем модуль по имени
            existing_module = session.query(Module).filter_by(module_name=name_mod).first()

            # Проверяем, найден ли модуль
            if existing_module is not None:
                # Получаем связанные с модулем команды
                related_commands = existing_module.commands
                # Удаляем модуль из БД
                session.delete(existing_module)
                session.commit()
                # Удаляем связанные с модулем команды
                for command in related_commands:
                    session.delete(command)

                session.commit()  # Фиксируем удаление команд

                # Возвращаем информацию об удалении
                print(f"Модуль {name_mod} успешно удален, вместе с {len(related_commands)} связанными командами.")
                return True
            else:
                print(f"Модуль {name_mod} не найден в БД.")
                return False
        except Exception as e:
            # Ошибка при удалении из БД данных о модуле или командах
            print(f"Ошибка при удалении модуля {name_mod}: {e}")
            session.rollback()  # Откатываем изменения в случае ошибки
            return 'error'
