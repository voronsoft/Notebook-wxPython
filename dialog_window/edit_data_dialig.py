import wx
import wx.xrc
import wx.richtext
from utils import database_queries


###########################################################################
# Class EditCommandOrModule
###########################################################################
class EditCommandOrModule(wx.Dialog):
    """Главное окно изменить: Команду или Модуль"""

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Изменить данные", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        # Главный сайзер окна
        sizer_main_dialog = wx.BoxSizer(wx.VERTICAL)
        sizer_main_dialog.SetMinSize(wx.Size(600, 600))

        # Сайзер радио-кнопок
        sizer_radio_button = wx.BoxSizer(wx.HORIZONTAL)
        # КНОПКА - "Изменить МОДУЛЬ"
        self.radio_edit_module = wx.RadioButton(self, wx.ID_ANY, "Изменить МОДУЛЬ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.radio_edit_module.SetValue(True)
        sizer_radio_button.Add(self.radio_edit_module, 0, wx.ALL | wx.EXPAND, 5)
        # Заполнитель
        self.static_text_empty = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        sizer_radio_button.Add(self.static_text_empty, 0, wx.ALL, 5)
        # КНОПКА - "Изменить КОМАНДУ"
        self.radio_edit_command = wx.RadioButton(self, wx.ID_ANY, "Изменить КОМАНДУ", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_radio_button.Add(self.radio_edit_command, 0, wx.ALL | wx.EXPAND, 5)
        sizer_main_dialog.Add(sizer_radio_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        # Сайзер разделительной линии
        sizer_line = wx.BoxSizer(wx.VERTICAL)
        self.static_line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_line.Add(self.static_line, 0, wx.EXPAND | wx.ALL, 5)
        sizer_main_dialog.Add(sizer_line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        # ------------------- Динамический сайзер для активации нужного класса ------------
        # При выборе активной радио-кнопки сайзер будет подключать соответствующий класс диалога
        # или изменить модуль - Class PanelDelModule
        # или изменить команду - Class PanelDelCommand
        self.sizer_DYNAMIC_edit = wx.BoxSizer(wx.VERTICAL)
        sizer_main_dialog.Add(self.sizer_DYNAMIC_edit, 1, wx.EXPAND, 5)
        # --------------------------------- END ----------------------------

        # Искусственно генерируем событие выбора активной радио-кнопки
        self.on_radio_change(event=self.radio_edit_module)
        # Привязываем обработчик on_radio_change к событию изменения радио кнопок
        self.radio_edit_module.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
        self.radio_edit_command.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
        # Привязываем событие при закрытии окна
        self.Bind(wx.EVT_CLOSE, self.on_close_dialog)

        self.SetSizer(sizer_main_dialog)
        self.Layout()
        sizer_main_dialog.Fit(self)
        self.Centre(wx.BOTH)

    # -------------------------- Обработчики ------------------------------
    # Обработчик поведения на выбор активной радиокнопки
    def on_radio_change(self, event):
        """Обработчик поведения на выбор активной радиокнопки"""
        # Удаляем все дочерние элементы из self.sizer_DYNAMIC_edit
        for child in self.sizer_DYNAMIC_edit.GetChildren():
            child.GetWindow().Destroy()

        if self.radio_edit_command.GetValue():
            command_connect = PanelEditCommand(self)  # Создаем экземпляр класса
            self.sizer_DYNAMIC_edit.Add(command_connect, 1, wx.EXPAND | wx.ALL, 5)

        elif self.radio_edit_module.GetValue():
            module_connect = PanelEditModule(self)  # Создаем экземпляр класса
            self.sizer_DYNAMIC_edit.Add(module_connect, 1, wx.EXPAND | wx.ALL, 5)

        # Перераспределяем элементы и подгоняем размер
        self.Layout()
        self.sizer_DYNAMIC_edit.Fit(self)

    # Обработчик события закрытия окна
    def on_close_dialog(self, event):
        """Закрытие диалогового окна"""
        self.Destroy()


###########################################################################
# Class PanelEditModule
###########################################################################
class PanelEditModule(wx.Panel):
    """Изменить модуль"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=0, name="Удалить МОДУЛЬ"):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        # Главный сайзер
        sizer_main_panel_edit_mod = wx.BoxSizer(wx.VERTICAL)
        sizer_main_panel_edit_mod.SetMinSize(wx.Size(600, 600))

        # Сайзер с данными
        sizer_data = wx.BoxSizer(wx.VERTICAL)
        #
        self.choice_mod_label = wx.StaticText(self, wx.ID_ANY, "Выберите модуль:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.choice_mod_label.Wrap(-1)
        sizer_data.Add(self.choice_mod_label, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)
        # Поле выбора модуля
        self.lst_mod_obj = database_queries.request_to_get_all_modules()
        choice_modChoices = [mod_item['module_name'] for mod_item in self.lst_mod_obj]  # Получаем список модулей
        self.choice_mod = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_modChoices, 0)
        self.choice_mod.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.choice_mod.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет для красного
        self.choice_mod.SetSelection(-1)
        sizer_data.Add(self.choice_mod, 0, wx.ALL | wx.EXPAND, 5)
        #
        self.name_mod_label = wx.StaticText(self, wx.ID_ANY, "Введите новое название (или оставьте пустым):", wx.DefaultPosition, wx.DefaultSize, 0)
        self.name_mod_label.Wrap(-1)
        sizer_data.Add(self.name_mod_label, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)
        # Поле ввода названия модуля
        self.name_mod_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_data.Add(self.name_mod_text, 0, wx.EXPAND | wx.ALL, 5)
        #
        self.descr_mod_label = wx.StaticText(self, wx.ID_ANY, "Введите описание модуля:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.descr_mod_label.Wrap(-1)
        sizer_data.Add(self.descr_mod_label, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)
        # Поле ввода описания для модуля
        self.descr_mod_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        sizer_data.Add(self.descr_mod_text, 1, wx.EXPAND | wx.ALL, 5)

        sizer_main_panel_edit_mod.Add(sizer_data, 1, wx.EXPAND, 5)

        # Сайзер кнопок
        sizer_bottom = wx.BoxSizer(wx.VERTICAL)
        self.button_apply = wx.Button(self, wx.ID_ANY, "Применить", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_bottom.Add(self.button_apply, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        sizer_main_panel_edit_mod.Add(sizer_bottom, 0, wx.EXPAND, 5)

        # Привязываем обработчик события к выбору модуля
        self.choice_mod.Bind(wx.EVT_CHOICE, self.on_module_select)
        # Привязываем событие для кнопки - "Применить"
        self.button_apply.Bind(wx.EVT_BUTTON, self.on_btn_apply)

        self.SetSizer(sizer_main_panel_edit_mod)
        self.Layout()
        sizer_main_panel_edit_mod.Fit(self)

    # -------------- Обработчики событий ----------------
    def on_btn_apply(self, event):
        """Изменение данных о модуле"""
        # Получаем название выбранного модуля
        select_mod_name = self.choice_mod.GetStringSelection()  # Получаем имя выбранного модуля
        name_new = self.name_mod_text.GetValue()  # Новое название модуля
        descr_new = self.descr_mod_text.GetValue()  # Новое описание модуля
        result = database_queries.edit_module(select_mod_name, name_new, descr_new)  # Изменяем данные

        if result:
            # Оповещение
            message = f"Модуль '{select_mod_name}'изменён."
            wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)

            # Очищаем поля
            self.choice_mod.SetSelection(-1)
            self.name_mod_text.Clear()
            self.descr_mod_text.Clear()

            # Обновляем список модулей в поле выбора
            self.lst_mod_obj = database_queries.request_to_get_all_modules()
            choice_modChoices = [mod_item['module_name'] for mod_item in self.lst_mod_obj]
            self.choice_mod.Clear()
            self.choice_mod.AppendItems(choice_modChoices)
            self.choice_mod.SetSelection(-1)
            self.Layout()

        elif result == 'error':
            # Оповещение
            message = f"Ошибка при изменении модуля: '{select_mod_name}'\nПовторите попытку."
            wx.MessageBox(message, "Ошибка", wx.OK | wx.ICON_ERROR)
        else:
            message = f"Модуль: '{select_mod_name}' не найден в БД."
            wx.MessageBox(message, "Нет совпадений", wx.OK | wx.ICON_WARNING)

    def on_module_select(self, event):
        """Обработчик события выбора модуля"""
        # Получаем название выбранного модуля
        selected_module_name = self.choice_mod.GetStringSelection()  # Получаем имя выбранного модуля
        # Получаем описание модуля
        descr_mod = ''.join(i['description'] for i in self.lst_mod_obj if selected_module_name in i.values())

        # Заполняем поля данными
        if self.name_mod_text.GetValue() or self.descr_mod_text.GetValue():
            # Если поля что то содержат, очищаем поля
            self.name_mod_text.Clear()
            self.descr_mod_text.Clear()

        self.name_mod_text.SetValue(selected_module_name)
        self.descr_mod_text.SetValue(descr_mod)

    # -------------- Функции ----------------
    def update_module_choices(self):
        """Обновляет список модулей в поле выбора"""
        self.lst_mod_obj = database_queries.request_to_get_all_modules()
        choice_modChoices = [mod_item['module_name'] for mod_item in self.lst_mod_obj]
        self.choice_mod.Clear()
        self.choice_mod.AppendItems(choice_modChoices)
        self.choice_mod.SetSelection(-1)
        self.Layout()


###########################################################################
# Class PanelEditCommand
###########################################################################
class PanelEditCommand(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        # Главный сайзер
        sizer_main_panel_edit_cmd = wx.BoxSizer(wx.VERTICAL)
        sizer_main_panel_edit_cmd.SetMinSize(wx.Size(600, 600))

        # Сайзер для контекстного меню
        sizer_ctx_edit_cmd = wx.GridSizer(0, 2, 0, 0)

        self.command_name_label = wx.StaticText(self, wx.ID_ANY, "Команда:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.command_name_label.Wrap(-1)
        sizer_ctx_edit_cmd.Add(self.command_name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        self.module_name_label = wx.StaticText(self, wx.ID_ANY, "Модуль:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.module_name_label.Wrap(-1)
        sizer_ctx_edit_cmd.Add(self.module_name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        self.cmd_data_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, -1), 0 | wx.BORDER_SIMPLE)
        self.cmd_data_name.SetMaxSize(wx.Size(300, -1))
        sizer_ctx_edit_cmd.Add(self.cmd_data_name, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        self.mod_data_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, -1), wx.TE_READONLY | wx.BORDER_SIMPLE)
        self.mod_data_name.SetMaxSize(wx.Size(300, -1))
        sizer_ctx_edit_cmd.Add(self.mod_data_name, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        sizer_main_panel_edit_cmd.Add(sizer_ctx_edit_cmd, 0, wx.EXPAND, 5)

        # Сайзер для выбора из списка команд
        sizer_indiv_edit_cmd = wx.BoxSizer(wx.VERTICAL)
        #
        self.choice_mod_label = wx.StaticText(self, wx.ID_ANY, "Выберите модуль:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.choice_mod_label.Wrap(-1)
        sizer_indiv_edit_cmd.Add(self.choice_mod_label, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)
        # Поле выбора модуля
        choice_modChoices = []
        self.choice_mod = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_modChoices, 0)
        sizer_indiv_edit_cmd.Add(self.choice_mod, 0, wx.ALL | wx.EXPAND, 5)
        #
        self.choice_cmd_label = wx.StaticText(self, wx.ID_ANY, "Выберите команду:", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_indiv_edit_cmd.Add(self.choice_cmd_label, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)
        # Поле выбора команды
        choice_cmdChoices = []
        self.choice_cmd = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_cmdChoices, 0)
        self.choice_cmd.SetSelection(-1)
        sizer_indiv_edit_cmd.Add(self.choice_cmd, 0, wx.ALL | wx.EXPAND, 5)

        sizer_main_panel_edit_cmd.Add(sizer_indiv_edit_cmd, 0, wx.EXPAND, 5)

        # Сайзер данных: нов-назв команды/описание/пример
        sizer_data = wx.BoxSizer(wx.VERTICAL)
        #
        self.new_name_label = wx.StaticText(self, wx.ID_ANY, "Новое название (если пусто используется старое):", wx.DefaultPosition, wx.DefaultSize, 0)
        self.new_name_label.Wrap(-1)
        sizer_data.Add(self.new_name_label, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)
        # Поле ввода нового названия команды
        self.new_name_inp_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_data.Add(self.new_name_inp_text, 0, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        #
        self.descr_label = wx.StaticText(self, wx.ID_ANY, "Описание:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.descr_label.Wrap(-1)
        sizer_data.Add(self.descr_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)
        # Поле описания команды
        self.descr_inp_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 200), 0 | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        self.descr_inp_text.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.descr_inp_text.SetMinSize(wx.Size(-1, 200))
        sizer_data.Add(self.descr_inp_text, 2, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        #
        self.exampl_label = wx.StaticText(self, wx.ID_ANY, "Пример:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.exampl_label.Wrap(-1)
        sizer_data.Add(self.exampl_label, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)
        # Поле пример
        self.exampl_inp_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 200), 0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        self.exampl_inp_text.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.exampl_inp_text.SetMinSize(wx.Size(-1, 100))
        sizer_data.Add(self.exampl_inp_text, 1, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        sizer_main_panel_edit_cmd.Add(sizer_data, 1, wx.EXPAND, 5)

        # Сайзер кнопок
        sizer_bottom = wx.BoxSizer(wx.VERTICAL)

        self.button_apply = wx.Button(self, wx.ID_ANY, "Применить", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_bottom.Add(self.button_apply, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer_main_panel_edit_cmd.Add(sizer_bottom, 0, wx.EXPAND, 5)
        # Привязываем событие для кнопки - "Применить"
        self.button_apply.Bind(wx.EVT_BUTTON, self.on_btn_apply)

        self.SetSizer(sizer_main_panel_edit_cmd)
        self.Layout()
        sizer_main_panel_edit_cmd.Fit(self)

    # --------------Обработчики событий --------------
    def on_btn_apply(self, event):
        """"Изменение команды в БД"""
        ...
        # TODO доделать функцию изменения команды


if __name__ == '__main__':
    app = wx.App(False)
    frame = EditCommandOrModule(None)
    frame.Show(True)
    app.MainLoop()
