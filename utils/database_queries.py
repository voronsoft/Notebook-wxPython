import os
import wx
import json
from db.models import Module, Command
from sqlalchemy.orm import sessionmaker
from logs.app_logger import logger_debug
from instance.app_config import path_to_DB
from sqlalchemy import create_engine, func, inspect, text

# Строим путь к файлу базы данных
engine = create_engine(f'sqlite:///{path_to_DB}', echo=False)  # Создаем соединение с базой данных echo=False отключит вывод запросов в консоль
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
            logger_debug.exception(f"Ошибка при получении списка модулей: {e}")
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
            logger_debug.exception(f"Ошибка при получении объекта-модуля: {e}")
            return 'error'


# Функция получение КОЛИЧЕСТВА модулей из БД.
def get_module_count():
    """Получение количества модулей из БД."""
    with Session() as session:
        try:
            # Выполняем запрос для подсчета количества модулей
            module_count = session.query(Module).count()

            # Возвращаем количество модулей
            return module_count

        except Exception as e:
            # Обрабатываем возможные ошибки, например, выводим сообщение об ошибке
            logger_debug.exception(f"Ошибка при получении количества модулей: {e}")
            return 0  # Если произошла ошибка, возвращаем 0


# Функция получение списка команд исходя из названия модуля (modul_name)
def request_get_commands(modul_name):
    """
    Получение списка команд исходя из названия модуля (modul_name).
    :param modul_name: - название (str)
    :return: - список команд (obj)
    """
    with Session() as session:
        try:
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
            # Обрабатываем возможные ошибки.
            logger_debug.exception(f"Ошибка при получении списка команд: {e}")
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
            logger_debug.exception(f"Ошибка при получении количества команд: {e}")
            return 0


# Функция для выполнения запроса получения данных о конкретной команде
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
            logger_debug.exception(f"Ошибка при получении полных данных о команде: {e}")
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
                logger_debug.debug(f"Команда {name_cmd} успешно добавлена в БД.")
                return True
            else:
                logger_debug.debug(f"Команда {name_cmd} есть в БД.")
                return False
        except Exception as e:
            # Ошибка при добавлении в БД команды
            logger_debug.exception(f"Ошибка добавления команды {name_cmd}: {e}")
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
            logger_debug.exception(f"Ошибка при изменении команды {cmd}: {e}")
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
                logger_debug.debug(f"Команда {name_cmd} не найдена в БД.")
                return False
        except Exception as e:
            # Ошибка при удалении из БД данных о команде
            logger_debug.exception(f"Ошибка при удалении из БД данных о команде: {e}")
            session.rollback()  # Откатываем изменения в случае ошибки
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
                logger_debug.debug(f'Модуль {name} успешно добавлен в БД.')
                return True
            else:
                logger_debug.debug(f"Модуль {name} есть в БД.")
                return False
        except Exception as e:
            # Ошибка при добавлении в БД модуля
            logger_debug.exception(f"Ошибка добавлении модуля {name}: {e}")
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
            logger_debug.exception(f"Ошибка при изменении модуля {select_mod_name}: {e}")
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
                logger_debug.debug(f"Модуль {name_mod} успешно удален, вместе с {len(related_commands)} связанными командами.")
                return True
            else:
                logger_debug.debug(f"Модуль {name_mod} не найден в БД.")
                return False
        except Exception as e:
            # Ошибка при удалении из БД данных о модуле или командах
            logger_debug.exception(f"Ошибка при удалении модуля {name_mod}: {e}")
            session.rollback()  # Откатываем изменения в случае ошибки
            return 'error'


# Функция очистки базы данных
def clear_database():
    """Функция удаления всех данных из таблиц в базе данных"""
    with Session() as session:
        try:
            # Получаем инспектора для анализа структуры базы данных
            inspector = inspect(engine)

            # Получаем список всех таблиц в базе данных
            tables = inspector.get_table_names()

            # Очищаем каждую таблицу
            for table in tables:
                delete_query = text(f"DELETE FROM {table}")
                session.execute(delete_query)

            # Фиксируем изменения
            session.commit()
            logger_debug.debug('База данных успешно очищена.')

        except Exception as e:
            # Ошибка при удалении данных
            logger_debug.exception(f'Ошибка при удалении данных из БД: {e}')
            session.rollback()  # Откатываем изменения в случае ошибки
            return 'error'


# Функция ИМПОРТА данных в файл типа .json
def import_data_json_from_db(path_file_json_data, gauge=None):
    """Функция импорте данных в файл типа .json"""
    import wx
    if path_file_json_data:
        with Session() as session:
            try:
                # Открываем файл JSON и загружаем данные
                with open(path_file_json_data, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    total_entries = len(data)

                    # Устанавливаем максимальное значение прогресс-бара
                    gauge.SetRange(total_entries)

                    # Счетчик добавленных команд
                    added_commands = 0

                    # Импортируем данные в базу данных
                    for idx, entry in enumerate(data, start=1):
                        module_name = entry['module_name']
                        command_name = entry['command_name']

                        # Проверяем, существует ли команда с таким именем
                        command = session.query(Command).filter_by(command_name=command_name).first()
                        if not command:
                            # Если команда не существует, создаем новую
                            command = Command(
                                command_name=command_name,
                                description=entry['command_description'],
                                example=entry['command_example'],
                            )
                            session.add(command)  # Сохраняем команду, чтобы получить ей ID
                            session.commit()

                            # Проверяем, существует ли модуль с таким именем
                            module = session.query(Module).filter_by(module_name=module_name).first()
                            if not module:
                                module = Module(
                                    module_name=module_name,
                                    description='',
                                )
                                session.add(module)  # Сохраняем модуль, чтобы получить ему ID
                                session.commit()

                            # Создаем связь команды с модулем
                            module.commands.append(command)
                            command.modules.append(module)
                            # Сохраняем изменения
                            session.commit()

                            # Увеличиваем счетчик добавленных команд для прогрес бара
                            added_commands += 1

                        # Устанавливаем текущее значение прогресс-бара
                        gauge.SetValue(added_commands)
                        wx.Yield()  # Позволяет интерфейсу обновиться

            except Exception as e:
                # Ошибка при импорте данных
                logger_debug.exception(f'Ошибка при импорте данных в БД из файла json: {e}')
                session.rollback()  # Откатываем изменения в случае ошибки
                return False
        return True
    else:
        logger_debug.warning("Импорт данных отменён. Путь к файлу json указан неверно.")


# Функция ЭКСПОРТА данных в файл типа .json
def export_data_db_to_json_file(name_text_module=None, gauge=None):
    """Функция экспорта данных в файл типа .json"""
    # Счетчик добавленных команд для прогресс бара
    added_commands = 0

    # --------------- Если в функцию был передан модуль формируем json файл с записями для модуля---------------
    if name_text_module:
        with Session() as session:
            try:
                lst_cmd_module = request_get_commands(name_text_module)
                # Создаем список для хранения словарей
                updated_commands_list = []
                # Устанавливаем максимальное значение для прогрес бара
                total_entries = len(lst_cmd_module)
                gauge.SetRange(total_entries)

                # Проходим по каждой команде
                for cmd in lst_cmd_module:
                    # Преобразуем запись в словарь с необходимыми полями
                    # с учетом, что файл в последующем может быть так же
                    # импортирован в программу
                    cmd_dict = {
                        'module_name': cmd['cmd_assoc_module'][0],
                        'command_name': cmd['commands_name'],
                        'command_description': cmd['description_command'],
                        'command_example': cmd['command_example:']
                    }
                    # Добавляем обновленный словарь в список
                    updated_commands_list.append(cmd_dict)
                    # Увеличиваем счетчик добавленных команд для прогрес бара
                    added_commands += 1
                    # Устанавливаем текущее значение прогрес бара
                    gauge.SetValue(added_commands)
                    wx.Yield()  # Позволяет интерфейсу обновиться

                # Экспортируем в JSON с более читабельным форматированием (используем - ensure_ascii=False)
                json_data = json.dumps(updated_commands_list, ensure_ascii=False, indent=4)
                logger_debug.debug(f"Объект JSON успешно сформирован (json_data), приступаем к записи данных в файл.")
            except Exception as json_error:
                # Оповещение
                message = f"Произошла ошибка при формировании JSON объекта:\n{json_error}"
                wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)
                # Обработка ошибок при формировании JSON
                logger_debug.exception(f"Произошла ошибка при формировании JSON объекта: {json_error}")
                return 'error'

            if json_data:
                try:
                    # Определяем путь для сохранения файла по пути в операционной системе - C:\Users\user\Documents\Notebook-export-json\all_data.json
                    file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Notebook-export-json', f'{name_text_module}.json')

                    # Проверяем и создаем директорию, если она не существует
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                    # Записываем данные в файл
                    with open(file_path, 'w', encoding='utf-8') as json_file:
                        json_file.write(json_data)
                        logger_debug.debug(f"Был создан файл 'Notebook_DB.json', по пути: {file_path}")

                    # Оповещение
                    message = f"Данные успешно экспортированы в файл: {name_text_module}.json.\nПуть к файлу: {file_path}"
                    wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)
                    gauge.SetValue(0)  # Обнуляем шкалу прогресс бара
                except Exception as file_error:
                    # Оповещение
                    message = f"Произошла ошибка при создании и записи файла 'Notebook_DB.json':\n{file_error}"
                    wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)
                    gauge.SetValue(0)  # Обнуляем шкалу прогресс бара
                    # Обработка ошибок при записи в файл
                    logger_debug.exception(f"Произошла ошибка при создании и записи файла 'Notebook_DB.json':\n {file_error}")
                    return 'error'

    # --------------- Если в функцию ничего не передали формируем json файл с записями Всей БД---------------
    else:
        with Session() as session:
            try:
                # Получаем все записи из таблицы
                all_commands = session.query(Command).all()
                # Создаем список для хранения словарей
                updated_commands_list = []

                # Устанавливаем максимальное значение для прогресс-бара
                total_entries = len(all_commands)
                gauge.SetRange(total_entries)

                # Проходим по каждой команде
                for cmd in all_commands:
                    # Получаем связанные модули
                    associated_modules = str(*[module.module_name for module in cmd.modules])

                    # Преобразуем запись в словарь с необходимыми полями
                    # с учетом, что файл в последующем может быть так же
                    # импортирован в программу
                    cmd_dict = {
                        'module_name': associated_modules,
                        'command_name': cmd.command_name,
                        'command_description': cmd.description,
                        'command_example': cmd.example
                    }
                    # Добавляем обновленный словарь в список
                    updated_commands_list.append(cmd_dict)
                    # Увеличиваем счетчик добавленных команд для прогрес бара
                    added_commands += 1
                    # Устанавливаем текущее значение прогрес бара
                    gauge.SetValue(added_commands)
                    wx.Yield()  # Позволяет интерфейсу обновиться

                # Экспортируем в JSON с более читабельным форматированием (используем - ensure_ascii=False)
                json_data = json.dumps(updated_commands_list, ensure_ascii=False, indent=4)
            except Exception as json_error:
                # Оповещение
                message = f"Произошла ошибка при формировании объекта JSON:\n{json_error}"
                wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)
                # Обработка ошибок при формировании JSON
                logger_debug.exception(f"Произошла ошибка при формировании JSON: {json_error}")
                return 'error'

            if json_data:
                try:
                    # Определяем путь для сохранения файла по пути в операционной системе - C:\Users\user\Documents\Notebook-export-json\Notebook_DB.json
                    file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Notebook-export-json', 'Notebook_DB.json')

                    # Проверяем и создаем директорию, если она не существует
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                    # Записываем данные в файл
                    with open(file_path, 'w', encoding='utf-8') as json_file:
                        json_file.write(json_data)
                        logger_debug.debug(f"Был создан файл 'Notebook_DB.json', по пути: {file_path}")

                    # Оповещение
                    message = f"Данные успешно экспортированы в файл: 'Notebook_DB.json'.\nПуть к файлу: {file_path}"
                    wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)
                    gauge.SetValue(0)  # Обнуляем шкалу прогресс бара
                except Exception as file_error:
                    # Оповещение
                    message = f"Произошла ошибка при создании и записи файла 'Notebook_DB.json':\n{file_error}"
                    wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)
                    gauge.SetValue(0)
                    # Обработка ошибок при записи в файл
                    print(f"Произошла ошибка при записи в файл: {file_error}")
                    logger_debug.exception(f"Произошла ошибка при создании и записи файла 'Notebook_DB.json':\n {file_error}")
                    return 'error'
