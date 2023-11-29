from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint

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
    description = Column(String, nullable=True, default="No description this modul")
    commands = relationship('Command', secondary='command_module_association', back_populates='modules')


# Модель таблицы связей таблиц: Модуль-Команда/ Команда-Модуль
class CommandModuleAssociation(Base):
    __tablename__ = 'command_module_association'
    id = Column(Integer, primary_key=True, autoincrement=True)
    command_id = Column(Integer, ForeignKey('commands.id'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('command_id', 'module_id'),
    )
