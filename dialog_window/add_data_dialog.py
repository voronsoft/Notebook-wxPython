import wx
import wx.xrc
import wx.richtext
from utils import database_queries
from utils.database_queries import request_to_get_all_modules


###########################################################################
#  Class AddCommandOrModule
###########################################################################
class AddCommandOrModule(wx.Dialog):
    """Главное окно добавить: Команду или Модуль"""

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Добавить данные", pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        # Главный сайзер окна
        self.sizer_main_dialog = wx.BoxSizer(wx.VERTICAL)
        self.sizer_main_dialog.SetMinSize(wx.Size(600, 600))

        # Сайзер радио-кнопок
        self.sizer_radio_button = wx.BoxSizer(wx.HORIZONTAL)
        # КНОПКА - Добавить КОМАНДУ
        self.radio_add_command = wx.RadioButton(self, wx.ID_ANY, "Добавить КОМАНДУ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.sizer_radio_button.Add(self.radio_add_command, 0, wx.ALL | wx.EXPAND, 5)
        # Заполнитель
        self.static_text_empty = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        self.sizer_radio_button.Add(self.static_text_empty, 0, wx.ALL, 5)
        # КНОПКА - Добавить МОДУЛЬ
        self.radio_add_module = wx.RadioButton(self, wx.ID_ANY, "Добавить МОДУЛЬ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.sizer_radio_button.Add(self.radio_add_module, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer_main_dialog.Add(self.sizer_radio_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        # Заполнитель
        self.static_text_empty1 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        self.sizer_radio_button.Add(self.static_text_empty1, 0, wx.ALL, 5)
        # КНОПКА - Изменить КОМАНДУ
        self.radio_edit_command = wx.RadioButton(self, wx.ID_ANY, "Изменить КОМАНДУ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.radio_edit_command.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.sizer_radio_button.Add(self.radio_edit_command, 0, wx.ALL | wx.EXPAND, 5)

        # Сайзер - Разделительной линии
        self.sizer_line = wx.BoxSizer(wx.VERTICAL)
        self.static_line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        self.sizer_line.Add(self.static_line, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer_main_dialog.Add(self.sizer_line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        # ------------------- Динамический сайзер для активации нужного класса ------------
        # При выборе активной радио-кнопки сайзер будет подключать соответствующий класс диалога
        # или добавить новую команду к существующему модулю
        # или добавить новый модуль
        self.sizer_DYNAMIC = wx.BoxSizer(wx.VERTICAL)
        self.sizer_main_dialog.Add(self.sizer_DYNAMIC, 1, wx.EXPAND, 5)
        # --------------------------------- END ----------------------------

        # Искусственно генерируем событие выбора активной радио-кнопки
        self.on_radio_change(event=self.radio_add_command)
        # Привязываем обработчик on_radio_change к событию изменения радио кнопок
        self.radio_add_command.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
        self.radio_add_module.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
        self.radio_edit_command.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
        # Привязываем событие при закрытии окна
        self.Bind(wx.EVT_CLOSE, self.on_close_dialog)

        self.SetSizer(self.sizer_main_dialog)
        self.Layout()
        self.sizer_main_dialog.Fit(self)
        self.Centre(wx.BOTH)

    # Обработчик поведения на выбор активной радиокнопки
    def on_radio_change(self, event):
        # Удаляем все дочерние элементы из sizer_DYNAMIC
        for child in self.sizer_DYNAMIC.GetChildren():
            child.GetWindow().Destroy()

        if self.radio_add_command.GetValue():
            command_connect = PanelAddCommand(self)  # Создаем экземпляр класса
            self.sizer_DYNAMIC.Add(command_connect, 1, wx.EXPAND | wx.ALL, 5)

        elif self.radio_add_module.GetValue():
            module_connect = PanelAddModule(self)  # Создаем экземпляр класса
            self.sizer_DYNAMIC.Add(module_connect, 1, wx.EXPAND | wx.ALL, 5)

        elif self.radio_edit_command.GetValue():
            module_connect = PanelEditCommand(self)  # Создаем экземпляр класса
            self.sizer_DYNAMIC.Add(module_connect, 1, wx.EXPAND | wx.ALL, 5)

        # Перераспределяем элементы и подгоняем размер
        self.Layout()
        self.sizer_DYNAMIC.Fit(self)

    # Обработчик события закрытия окна
    def on_close_dialog(self, event):
        """Закрытие диалогового окна"""
        self.Destroy()


###########################################################################
# Class PanelAddCommand
###########################################################################
class PanelAddCommand(wx.Panel):
    """Добавление данных о команде"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.NO_FULL_REPAINT_ON_RESIZE | wx.TAB_TRAVERSAL | wx.WANTS_CHARS, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        # Главный сайзер панели
        sizer_main_panel_cmd = wx.BoxSizer(wx.VERTICAL)
        sizer_main_panel_cmd.SetMinSize(wx.Size(600, 600))

        # Сайзер TOP
        sizer_top_inf = wx.GridSizer(0, 2, 0, 0)
        #
        self.cmd_label = wx.StaticText(self, wx.ID_ANY, "Команда:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.cmd_label.Wrap(-1)
        sizer_top_inf.Add(self.cmd_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        #
        self.choice_label = wx.StaticText(self, wx.ID_ANY, "Подключить к модулю:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.choice_label.Wrap(-1)
        sizer_top_inf.Add(self.choice_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        # Поле название - "Команда:"
        self.cmd_data_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, -1), 0 | wx.BORDER_STATIC)
        self.cmd_data_name.SetMaxSize(wx.Size(300, -1))
        sizer_top_inf.Add(self.cmd_data_name, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        # Поле выбора - "Подключить к модулю:"
        choice_module_dataChoices = [mod_item['module_name'] for mod_item in request_to_get_all_modules()]  # Получаем список модулей
        self.choice_module_data = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(250, -1), choice_module_dataChoices, 0 | wx.BORDER_SIMPLE)
        self.choice_module_data.SetSelection(0)
        self.choice_module_data.SetMaxSize(wx.Size(300, -1))
        sizer_top_inf.Add(self.choice_module_data, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        sizer_main_panel_cmd.Add(sizer_top_inf, 0, wx.EXPAND, 5)

        # Сайзер основных данных
        sizer_data_descr = wx.BoxSizer(wx.VERTICAL)
        #
        self.cmd_description_label = wx.StaticText(self, wx.ID_ANY, "Описание:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cmd_description_label.Wrap(-1)
        sizer_data_descr.Add(self.cmd_description_label, 0, wx.ALL, 5)
        # Поле - "Описание:"
        self.cmd_description_data = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_SIMPLE | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        sizer_data_descr.Add(self.cmd_description_data, 1, wx.EXPAND | wx.ALL, 5)
        #
        self.cmd_example_label = wx.StaticText(self, wx.ID_ANY, "Пример:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cmd_example_label.Wrap(-1)
        sizer_data_descr.Add(self.cmd_example_label, 0, wx.ALL, 5)
        # Поле - "Пример:"
        self.cmd_example_data = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_SIMPLE | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        sizer_data_descr.Add(self.cmd_example_data, 1, wx.EXPAND | wx.ALL, 5)

        sizer_main_panel_cmd.Add(sizer_data_descr, 1, wx.EXPAND, 5)

        # Сайзер кнопок
        sizer_bottom = wx.BoxSizer(wx.VERTICAL)
        self.button_apply = wx.Button(self, wx.ID_ANY, "Применить", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_bottom.Add(self.button_apply, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer_main_panel_cmd.Add(sizer_bottom, 0, wx.EXPAND, 5)

        # Привязываем событие для кнопки - "Применить"
        self.button_apply.Bind(wx.EVT_BUTTON, self.on_btn_apply)

        self.SetSizer(sizer_main_panel_cmd)
        self.Layout()
        sizer_main_panel_cmd.Fit(self)

    # TODO добавить обновление интерфейса главного окна, после закрытия окна !!!
    # --------------Обработчики событий --------------
    def on_btn_apply(self, event):
        """"Добавление команды в БД"""
        name_cmd_new = self.cmd_data_name.GetValue()  # Получаем Название
        descr_cmd_new = self.cmd_description_data.GetValue()  # Получаем описание
        example_cmd_new = self.cmd_example_data.GetValue()  # Получаем пример использования
        assoc_mod = self.choice_module_data.GetSelection()  # Получаем модуль к которому присоединяется команда

        if len(name_cmd_new) >= 2 and len(descr_cmd_new) >= 5 and assoc_mod >= 0:
            # Получение значения индекса выбранного модуля
            selection_index_choice = self.choice_module_data.GetSelection()
            # Получаем текстовое значение поля выбора
            name_text_choice = self.choice_module_data.GetString(selection_index_choice)
            # Получаем объект-модуля из БД по текстовому значению из поля выбора choice
            mod_obj = database_queries.request_get_module(name_text_choice)

            if mod_obj:  # Если объект существует
                # Добавляем команду в БД
                result = database_queries.add_command(name_cmd_new, descr_cmd_new, example_cmd_new, mod_obj)
                if result:
                    # Оповещение
                    message = f"Новая Команда '{name_cmd_new}'добавлена в БД"
                    wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)
                    # Очищаем поля
                    self.cmd_data_name.Clear()
                    self.cmd_description_data.Clear()
                    self.cmd_example_data.Clear()
                    self.choice_module_data.SetSelection(-1)
                elif result == 'error':
                    # Оповещение
                    message = f"Ошибка при добавлении команды: '{name_cmd_new}'\nПовторите попытку."
                    wx.MessageBox(message, "Ошибка", wx.OK | wx.ICON_ERROR)
                    # Очищаем поля
                else:
                    message = f"Команда: '{name_cmd_new}'\nУже есть в БД."
                    wx.MessageBox(message, "Найдено совпадение", wx.OK | wx.ICON_WARNING)
        else:
            # Отображаем диалоговое окно с сообщением
            message = (f"Необходимо ввести данные:\nНазвание >= 2 знаков.\n"
                       f"Описание >= 5 знаков.\nПример не обязательно\nВыбрать модуль для связи.")
            wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_WARNING)


###########################################################################
# Class PanelAddModule
###########################################################################
class PanelAddModule(wx.Panel):
    """Добавление данных о модуле"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        # Сайзер основной
        sizer_main_panel_mod = wx.BoxSizer(wx.VERTICAL)
        sizer_main_panel_mod.SetMinSize(wx.Size(600, 600))

        # Сайзер TOP
        sizer_top_inf = wx.GridSizer(0, 1, 0, 0)

        self.mod_name_label = wx.StaticText(self, wx.ID_ANY, "Модуль:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.mod_name_label.Wrap(-1)
        sizer_top_inf.Add(self.mod_name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        #  Поле ввода названия модуля
        self.mod_data_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, -1), 0 | wx.BORDER_SIMPLE)
        self.mod_data_name.SetMaxSize(wx.Size(300, -1))
        sizer_top_inf.Add(self.mod_data_name, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        sizer_main_panel_mod.Add(sizer_top_inf, 0, wx.EXPAND, 5)

        # Сайзер описание модуля
        sizer_data_descr = wx.BoxSizer(wx.VERTICAL)

        self.mod_description_label = wx.StaticText(self, wx.ID_ANY, "Описание:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.mod_description_label.Wrap(-1)
        sizer_data_descr.Add(self.mod_description_label, 0, wx.ALL, 5)
        #  Поле описание модуля
        self.mod_description_data = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_SIMPLE | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        sizer_data_descr.Add(self.mod_description_data, 1, wx.EXPAND | wx.ALL, 5)
        sizer_main_panel_mod.Add(sizer_data_descr, 1, wx.EXPAND, 5)

        # Сайзер кнопок
        sizer_bottom = wx.BoxSizer(wx.VERTICAL)
        self.button_apply = wx.Button(self, wx.ID_ANY, "Применить", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_bottom.Add(self.button_apply, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer_main_panel_mod.Add(sizer_bottom, 0, wx.EXPAND, 5)

        # Привязываем событие для кнопки - "Применить"
        self.button_apply.Bind(wx.EVT_BUTTON, self.on_btn_apply)

        self.SetSizer(sizer_main_panel_mod)
        self.Layout()
        sizer_main_panel_mod.Fit(self)

    # --------------Обработчики событий --------------
    def on_btn_apply(self, event):
        """"Добавление модуля в БД"""
        # TODO добавить обновление интерфейса главного окна, после закрытия окна !!!
        name_mod = self.mod_data_name.GetValue()  # Получаем Название
        descr_mod = self.mod_description_data.GetValue()  # Получаем описание

        if len(name_mod) >= 3 and len(descr_mod) >= 5:
            # Добавляем модуль в БД
            answer = database_queries.add_module(name_mod, descr_mod)
            if answer:
                # Оповещение
                message = f"Новый модуль '{name_mod}'добавлен в БД"
                wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)
                # Очищаем поля
                self.mod_data_name.Clear()
                self.mod_description_data.Clear()
            elif answer == 'error':
                # Оповещение
                message = f"Ошибка при добавлении модуля: '{name_mod}'\nПовторите попытку."
                wx.MessageBox(message, "Ошибка", wx.OK | wx.ICON_ERROR)
                # Очищаем поля
            else:
                message = f"Модуль: '{name_mod}'\nУже есть в БД."
                wx.MessageBox(message, "Найдено совпадение", wx.OK | wx.ICON_WARNING)
        else:
            # Отображаем диалоговое окно с сообщением
            message = f"Необходимо ввести данные:\nНазвание (не менее 3 знака).\nОписание (не менее 5 знаков)."
            wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_WARNING)


###########################################################################
# Class PanelEditCommand
###########################################################################
class PanelEditCommand(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        # Главный сайзер
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(600, 600))

        # Сайзер TOP
        sizer_top = wx.GridSizer(0, 2, 0, 0)

        self.command_name_label = wx.StaticText(self, wx.ID_ANY, "Команда:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.command_name_label.Wrap(-1)
        sizer_top.Add(self.command_name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        self.module_name_label = wx.StaticText(self, wx.ID_ANY, "Модуль:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.module_name_label.Wrap(-1)
        sizer_top.Add(self.module_name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        # Поле имя команды
        self.cmd_data_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, -1), 0 | wx.BORDER_SIMPLE)
        self.cmd_data_name.SetMaxSize(wx.Size(300, -1))
        sizer_top.Add(self.cmd_data_name, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        # Поле имя модуля
        self.mod_data_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, -1), wx.TE_READONLY | wx.BORDER_SIMPLE)
        self.mod_data_name.SetMaxSize(wx.Size(300, -1))
        sizer_top.Add(self.mod_data_name, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        sizer_main.Add(sizer_top, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        # Сайзер данных (описание и пример команды)
        sizer_data = wx.BoxSizer(wx.VERTICAL)

        self.description_label = wx.StaticText(self, wx.ID_ANY, "Описание:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.description_label.Wrap(-1)
        sizer_data.Add(self.description_label, 0, wx.ALL, 5)
        # Поле описание команды
        self.description_data = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_SIMPLE | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        sizer_data.Add(self.description_data, 1, wx.EXPAND | wx.ALL, 5)

        self.example_label = wx.StaticText(self, wx.ID_ANY, "Пример:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.example_label.Wrap(-1)
        sizer_data.Add(self.example_label, 0, wx.ALL, 5)
        # Поле с примером
        self.example_data = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_SIMPLE | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        sizer_data.Add(self.example_data, 1, wx.EXPAND | wx.ALL, 5)

        sizer_main.Add(sizer_data, 1, wx.ALL | wx.EXPAND, 5)

        # Сайзер кнопок
        sizer_bottom = wx.BoxSizer(wx.VERTICAL)
        self.button_apply = wx.Button(self, wx.ID_ANY, "Применить", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_bottom.Add(self.button_apply, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer_main.Add(sizer_bottom, 0, wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

    def set_values(self, name, module, description, example):
        """Функция принимает на вход данные о команде и задает значения нужным полям"""
        self.cmd_data_name.SetLabel(name)
        self.mod_data_name.SetLabel(module)
        self.description_data.WriteText(description)
        self.example_data.WriteText(example)


if __name__ == '__main__':
    app = wx.App(False)
    frame = AddCommandOrModule(None)
    frame.Show(True)
    app.MainLoop()
