from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine

# Создаем базовый класс
Base = declarative_base()


# Модель таблицы - Команды
class Command(Base):
    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    command_name = Column(String, nullable=False)
    description = Column(String, default="No description this command")
    example = Column(String, default="No examples this command")
    modules = relationship('Module', secondary='command_module_association', back_populates='commands')


# Модель таблицы - Модули
class Module(Base):
    __tablename__ = 'modules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    module_name = Column(String, nullable=False, unique=True)
    commands = relationship('Command', secondary='command_module_association', back_populates='modules')


# Модель таблицы связей таблиц: Модуль-Команда/ Команда-Модуль
class CommandModuleAssociation(Base):
    __tablename__ = 'command_module_association'

    command_id = Column(Integer, ForeignKey('commands.id'), primary_key=True)
    module_id = Column(Integer, ForeignKey('modules.id'), primary_key=True)


# Функция для создания БД db-notebook (sqlite3)
def create_database():
    # Создаем соединение с базой данных
    engine = create_engine('sqlite:///db_notebook.db', echo=True)
    # Создаем сессию для взаимодействия с базой данных
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Создаем таблицы в базе данных
        Base.metadata.create_all(engine)
        # Сохранение изменений в базе данных
        session.commit()
    except Exception as e:
        print(f'Ошибка при создании БД:\n{str(e)}')
        session.rollback()  # Откатываем изменения в случае ошибки
    finally:
        # Закрываем соединение с базой данных, чтобы избежать утечек ресурсов
        session.close()


if __name__ == "__main__":
    # Создаем БД если есть необходимость
    create_database()
