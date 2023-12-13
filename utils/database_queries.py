import os
from sqlalchemy import create_engine, func
from db.models import Module, Command
from sqlalchemy.orm import sessionmaker

# Получаем корневую директорию проекта
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Строим путь к файлу базы данных
path_to_DB = os.path.join(root_directory, 'db', 'db_notebook.db')  # Путь к БД относительно вызова функции

engine = create_engine(f'sqlite:///{path_to_DB}', echo=True)  # Создаем соединение с базой данных
Session = sessionmaker(bind=engine)  # Создаем сессию для взаимодействия с базой данных


# Функция для выполнения запроса и получения данных о модулях
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


# Функция для выполнения запроса и получения данных о командах
# def request_get_commands(modul_name=None):
#     """Получение списка команд исходя из названия модуля (modul_name)."""
#     with Session() as session:
#         try:
#             if modul_name:
#                 # Если modul_name задан, фильтруем команды по ассоциированным модулям
#                 commands = session.query(Command).join(Command.modules).filter(Module.module_name == modul_name).all()
#                 # Преобразуем результат в список словарей для удобства использования
#                 commands_data = []
#                 for command in commands:
#                     data = {
#                         'id': command.id,
#                         'commands_name': command.command_name,
#                         'description_command': command.description,
#                         'command_example:': command.example,
#                         'cmd_assoc_module': tuple(*[(module.module_name, module.id) for module in command.modules])
#                     }
#                     commands_data.append(data)
#                 return commands_data
#
#         except Exception as e:
#             # Обрабатываем возможные ошибки, например, выводим сообщение об ошибке
#             print(f"Ошибка при получении списка команд: {e}")
#             return []
# Функция для получения списка команд связанных с модулем
def request_get_commands(modul_name):
    """Получение списка команд исходя из названия модуля (modul_name)."""
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
    """Получение полной информации о команде из БД"""
    with Session() as session:
        try:
            if command_name:
                existing_command = session.query(Command).filter_by(command_name=command_name).first()
                if not existing_command:  # Проверяем есть ли команда
                    print('Команда не найдена (нет совпадений, проверьте написание)')
                    return 'Команда не найдена (нет совпадений, проверьте написание)'

                command_data = {'id': existing_command.id,
                                'commands_name': existing_command.command_name,
                                'description_command': existing_command.description,
                                'command_example:': existing_command.example,
                                'cmd_assoc_module': tuple(*[(module.module_name, module.id) for module in existing_command.modules])
                                }
                print(command_data)
                return command_data

        except Exception as e:
            # Обрабатываем возможные ошибки, например, выводим сообщение об ошибке
            print(f"Ошибка при получении полных данных о команде: {e}")
            return []


# Функция добавления новой КОМАНДЫ
def add_command(name, description, example, modules):
    """Функция добавления новой КОМАНДЫ"""
    ...


# Функция изменения данных КОМАНДЫ
def edit_command(name, description, example, modules):
    """Функция изменения данных КОМАНДЫ"""
    ...


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
def add_module(name, description, commands):
    """Функция добавления нового МОДУЛЯ"""
    ...


# Функция изменения данных МОДУЛЯ
def edit_module(name, description):
    """Функция изменения данных МОДУЛЯ"""
    ...


# Функция удаления МОДУЛЯ и связанных с ним команд.
def del_module(name_mod):
    """Функция удаления МОДУЛЯ и связанных с ним команд."""
    ...
