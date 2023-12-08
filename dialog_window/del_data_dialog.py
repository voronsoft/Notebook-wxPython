import wx
import wx.xrc
from utils.database_queries import request_to_get_all_modules, request_to_get_all_commands


###########################################################################
# Class DelCmdOrMod
###########################################################################

class DelCmdOrMod(wx.Dialog):
    """Главное окно удалить: Команду или Модуль"""

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Удалить данные", pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        # Главный сайзер окна
        self.sizer_main_dialog = wx.BoxSizer(wx.VERTICAL)

        self.sizer_main_dialog.SetMinSize(wx.Size(600, 600))
        sizer_radio_button = wx.BoxSizer(wx.HORIZONTAL)

        # КНОПКА - Удалить МОДУЛЬ
        self.radio_del_module = wx.RadioButton(self, wx.ID_ANY, "Удалить МОДУЛЬ", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.radio_del_module.SetValue(True)
        sizer_radio_button.Add(self.radio_del_module, 0, wx.ALL | wx.EXPAND, 5)

        # сайзер заполнитель
        self.static_text_empty = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        self.static_text_empty.Wrap(-1)
        sizer_radio_button.Add(self.static_text_empty, 0, wx.ALL, 5)

        # КНОПКА - Удалить КОМАНДУ
        self.radio_del_command = wx.RadioButton(self, wx.ID_ANY, "Удалить КОМАНДУ", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_radio_button.Add(self.radio_del_command, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer_main_dialog.Add(sizer_radio_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        # Привязываем обработчик on_radio_change к событию изменения радио кнопок
        self.radio_del_module.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
        self.radio_del_command.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)

        # Сайзер - Разделительной линии
        sizer_line = wx.BoxSizer(wx.VERTICAL)
        self.static_line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_line.Add(self.static_line, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer_main_dialog.Add(sizer_line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        # ------------------- Динамический сайзер для активации нужного класса ------------
        # При выборе активной радио-кнопки сайзер будет подключать соответствующий класс диалога
        # или удалить модуль - Class PanelDelModule
        # или удалить команду - Class PanelDelCommand
        self.sizer_DYNAMIC_del = wx.BoxSizer(wx.VERTICAL)
        self.sizer_main_dialog.Add(self.sizer_DYNAMIC_del, 1, wx.EXPAND, 5)
        # ------------------------------------------ END ----------------------------------

        # Сайзер кнопок OK/CANCEL
        sizer_bottom = wx.StdDialogButtonSizer()
        self.sizer_bottomOK = wx.Button(self, wx.ID_OK)
        sizer_bottom.AddButton(self.sizer_bottomOK)
        self.sizer_bottomCancel = wx.Button(self, wx.ID_CANCEL)
        sizer_bottom.AddButton(self.sizer_bottomCancel)
        sizer_bottom.Realize()
        self.sizer_main_dialog.Add(sizer_bottom, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.sizer_main_dialog)
        self.Layout()
        self.sizer_main_dialog.Fit(self)
        self.Centre(wx.BOTH)

    # Обработчик поведения на выбор активной радиокнопки
    def on_radio_change(self, event):
        # Удаляем все дочерние элементы из self.sizer_DYNAMIC_del
        for child in self.sizer_DYNAMIC_del.GetChildren():
            child.GetWindow().Destroy()

        if self.radio_del_module.GetValue():
            print('активна кнопка удалить модуль')
            del_mod_connect = PanelDelModule(self)  # Создаем экземпляр класса
            self.sizer_DYNAMIC_del.Add(del_mod_connect, 1, wx.EXPAND | wx.ALL, 5)

        elif self.radio_del_command.GetValue():
            print('активна кнопка удалить команду')
            del_cmd_connect = PanelDelCommand(self)  # Создаем экземпляр класса
            self.sizer_DYNAMIC_del.Add(del_cmd_connect, 1, wx.EXPAND | wx.ALL, 5)

        # Перераспределяем элементы и подгоняем размер
        self.Layout()
        self.sizer_DYNAMIC_del.Fit(self)


###########################################################################
# Class PanelDelModule
###########################################################################

class PanelDelModule(wx.Panel):
    """Удалить Модуль"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL, name="Удалить МОДУЛЬ"):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        sizer_main_panel_del_mod = wx.BoxSizer(wx.VERTICAL)
        sizer_main_panel_del_mod.SetMinSize(wx.Size(600, 600))

        sizer_top_inf = wx.BoxSizer(wx.VERTICAL)
        # КНОПКА - Удалить МОДУЛЬ
        self.info_mod_label = wx.StaticText(self, wx.ID_ANY, "Удалить модуль:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL | wx.BORDER_SIMPLE)
        self.info_mod_label.Wrap(-1)
        self.info_mod_label.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top_inf.Add(self.info_mod_label, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        choice_modChoices = [mod_item['module_name'] for mod_item in request_to_get_all_modules()]  # Получаем список модулей
        self.choice_mod = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_modChoices, 0)
        # Привязываем обработчик события к выбору модуля
        self.choice_mod.Bind(wx.EVT_CHOICE, self.on_module_select)

        self.choice_mod.SetSelection(0)
        self.choice_mod.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top_inf.Add(self.choice_mod, 0, wx.ALL | wx.EXPAND, 5)
        sizer_main_panel_del_mod.Add(sizer_top_inf, 0, wx.EXPAND, 5)

        sizer_data = wx.BoxSizer(wx.VERTICAL)

        self.info_cmd_label = wx.StaticText(self, wx.ID_ANY, "Связанные команды с модулем (их так же можно удалить):", wx.DefaultPosition, wx.DefaultSize, 0)
        self.info_cmd_label.Wrap(-1)
        self.info_cmd_label.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_data.Add(self.info_cmd_label, 0, wx.ALL, 5)

        # Скроллинг для окна
        self.scrolled_window = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.scrolled_window.SetScrollRate(5, 5)

        # ------------------- Динамический сайзер для активации нужного класса ------------
        self.sizer_cmd_list = wx.GridSizer(0, 5, 0, 0)

        # self.button_del_TEST = wx.Button(self.scrolled_window, wx.ID_ANY, "Тестовая кнопка", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.sizer_cmd_list.Add(self.button_del_TEST, 0, wx.ALL, 5)

        self.scrolled_window.SetSizer(self.sizer_cmd_list)
        self.scrolled_window.Layout()
        self.sizer_cmd_list.Fit(self.scrolled_window)
        # --------------------------------- END ----------------------------

        sizer_data.Add(self.scrolled_window, 1, wx.EXPAND | wx.ALL, 5)
        sizer_main_panel_del_mod.Add(sizer_data, 1, wx.EXPAND, 5)

        self.SetSizer(sizer_main_panel_del_mod)
        self.Layout()
        sizer_main_panel_del_mod.Fit(self)

    def on_module_select(self, event):
        """Обработчик события выбора модуля"""
        selected_module = self.choice_mod.GetStringSelection()  # Получаем выбранный модуль
        commands = request_to_get_all_commands(selected_module)  # Запрашиваем команды для выбранного модуля

        for ind, cmd in enumerate(commands):
            # btn = wx.Button(self.scrolled_window, wx.ID_ANY, cmd['commands_name'], wx.DefaultPosition, wx.DefaultSize, 0)
            self.sizer_cmd_list.Add(wx.Button(self.scrolled_window, wx.ID_ANY, cmd['commands_name'], wx.DefaultPosition, wx.DefaultSize, 0), 0, wx.ALL, 5)


###########################################################################
# Class PanelDelCommand
###########################################################################

class PanelDelCommand(wx.Panel):
    """Удалить Команду"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        # Главный сайзер
        sizer_main_panel__del_cmd = wx.BoxSizer(wx.VERTICAL)
        # Сайзер TOP
        sizer_top_inf = wx.BoxSizer(wx.VERTICAL)
        self.info_cmd_label = wx.StaticText(self, wx.ID_ANY, "Удалить команду:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL | wx.BORDER_SIMPLE)
        self.info_cmd_label.Wrap(-1)
        sizer_top_inf.Add(self.info_cmd_label, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        sizer_main_panel__del_cmd.Add(sizer_top_inf, 0, wx.EXPAND, 5)

        # Динамический сайзер
        sizer_Dynamic_data = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_Dynamic_data.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        sizer_main_panel__del_cmd.Add(sizer_Dynamic_data, 1, wx.EXPAND, 5)

        self.SetSizer(sizer_main_panel__del_cmd)
        self.Layout()
        sizer_main_panel__del_cmd.Fit(self)

        self.add_tabs_item()  # Добавляем вкладки по названиям модулей

    # Добавляем вкладки по количеству модулей из БД
    def add_tabs_item(self):
        """Функция для добавления вкладок по количеству модулей из БД"""

        result = request_to_get_all_modules()  # Запрос к бд на получение модулей

        # Создаем вкладки исходя из количества модулей
        for ind, obj in enumerate(result):
            page_name = obj['module_name']
            page = wx.ScrolledWindow(self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
            page.SetScrollRate(5, 5)
            sizer_window_Modul = wx.BoxSizer(wx.VERTICAL)

            # Получаем данные перечня команд из БД для текущего модуля
            commands_data = request_to_get_all_commands(modul_name=page_name)

            # Добавляем данные о командах
            for command in commands_data:
                command_name = command['commands_name']

                name_cmd = wx.Button(page, wx.ID_ANY, command_name, wx.DefaultPosition, wx.DefaultSize, 0)
                name_cmd.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет текста названия команды

                # Добавляем данные в сайзер
                sizer_window_Modul.Add(name_cmd, 0, wx.ALL | wx.EXPAND, 3)

                # --------------- Связываем событие с обработчиками
                name_cmd.Bind(wx.EVT_LEFT_DOWN, lambda event, cmd=command: self.del_command(cmd))

            page.SetSizer(sizer_window_Modul)
            page.Layout()
            sizer_window_Modul.Fit(page)

            self.notebook.AddPage(page, page_name, False)

    # Обработчик удаления команды из связанного модуля
    def del_command(self, cmd):
        ...
        print(f'Была нажата кнопка - команда {cmd["commands_name"]} будет удалена')
