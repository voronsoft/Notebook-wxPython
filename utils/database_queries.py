# Импортируем необходимые модули
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Module, Command

# Получаем корневую директорию проекта
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Строим путь к файлу базы данных
path_to_DB = os.path.join(root_directory, 'db', 'db_notebook.db')  # Путь к БД относительно вызова функции

engine = create_engine(f'sqlite:///{path_to_DB}', echo=True)  # Создаем соединение с базой данных
Session = sessionmaker(bind=engine)  # Создаем сессию для взаимодействия с базой данных


# Функция для выполнения запроса и получения данных о всех модулях
def request_to_get_all_modules(command=None):
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


def request_to_get_all_commands(modul_name=None):
    """Получение списка команд исходя из названия модуля. Если модуля нет выбираем всё"""
    with Session() as session:
        try:
            if not modul_name:
                # Если modul_name не задан, получаем все команды без фильтрации по модулю
                commands = session.query(Command).all()  # Выполняем запрос ко всем командам
            else:
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


if __name__ == "__main__":
    # # Вызываем функцию и получаем данные о всех модулях
    # all_modules_data = request_to_get_all_modules()
    # # Выводим результат
    # print("Data for all modules:")
    # for module_data in all_modules_data:
    #     print(module_data)
    #
    # # Вызываем функцию и получаем данные о всех командах
    # all_cmd_module = request_to_get_all_commands('string')
    # print("=====================================")
    # for cmd_data in all_cmd_module:
    #     print(cmd_data)

    # Вызываем функцию и получаем данные о конкретной команде
    show_full_command_info('list.append(x)')
