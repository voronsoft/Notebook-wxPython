# import wx
# import wx.xrc
#
# from dialog_window.add_data_dialog import PanelEditCommand, AddCommandOrModule
# from utils.database_queries import request_to_get_all_modules, request_to_get_all_commands, show_full_command_info
# from dialog_window.view_command_dialog import ViewCommandData
#
#
# ###########################################################################
# # Class PanelCenter
# ###########################################################################
#
# class PanelCenter(wx.Panel):
#
#     def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
#         wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
#         SizerPanel = wx.BoxSizer(wx.VERTICAL)
#         self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), 0)
#         SizerPanel.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
#
#         self.SetSizer(SizerPanel)
#         self.Layout()
#
#         # Добавляем вкладки по названиям модулей
#         self.add_tabs_item()
#
#     # Добавляем вкладки по количеству модулей из БД
#     def add_tabs_item(self):
#         """Функция для добавления вкладок по количеству модулей из БД"""
#
#         result = request_to_get_all_modules()  # Запрос к бд на получение модулей
#
#         # Создаем вкладки исходя из количества модулей
#         for ind, obj in enumerate(result):
#             page_name = obj['module_name']
#             scrol_wind = wx.ScrolledWindow(self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
#             scrol_wind.SetScrollRate(5, 5)
#             sizer_window_Modul = wx.BoxSizer(wx.VERTICAL)
#
#             # Получаем данные перечня команд из БД для текущего модуля
#             commands_data = request_to_get_all_commands(modul_name=page_name)
#
#             # Добавляем данные в текстовые поля каждой вкладки
#             for command in commands_data:
#                 command_name = command['commands_name']
#                 description = command['description_command']
#
#                 text_ctrl_command = wx.StaticText(scrol_wind, wx.ID_ANY, command_name, wx.DefaultPosition, wx.Size(300, -1), 0 | wx.BORDER_THEME)
#                 text_ctrl_command.Wrap(299)  # Устанавливаем максимальную ширину для обеспечения переноса текста
#                 text_ctrl_command.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
#                 text_ctrl_command.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет текста названия команды
#
#                 text_ctrl_description = wx.TextCtrl(scrol_wind, wx.ID_ANY, description, wx.DefaultPosition, wx.Size(-1, -1), wx.TE_READONLY)
#                 text_ctrl_description.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
#
#                 sizer_command_data = wx.BoxSizer(wx.HORIZONTAL)
#                 sizer_command_data.Add(text_ctrl_command, 0, wx.ALL | wx.EXPAND, 0)
#                 sizer_command_data.Add(text_ctrl_description, 3, wx.ALL | wx.EXPAND, 0)
#
#                 # Добавляем данные в сайзер
#                 sizer_window_Modul.Add(sizer_command_data, 0, wx.EXPAND, 3)
#
#                 # --------------- Связываем событие с обработчиками
#                 # Открытие окна при нажатии (левой кнопкой мыши)
#                 text_ctrl_description.Bind(wx.EVT_LEFT_DOWN, lambda event, cmd=command: self.show_command_details(cmd))  # - на описание команды
#                 text_ctrl_command.Bind(wx.EVT_LEFT_DOWN, lambda event, cmd=command: self.show_command_details(cmd))  # - на название команды
#
#                 # Открытие контекстного меню при нажатии (правой кнопкой мыши)
#                 # - Копировать - в буфер обмена
#                 # - Подробно - открывает окно с подробной информацией
#                 text_ctrl_command.Bind(wx.EVT_RIGHT_DOWN, lambda event, cmd=command: self.show_context_menu(cmd))
#
#             scrol_wind.SetSizer(sizer_window_Modul)
#             scrol_wind.Layout()
#             sizer_window_Modul.Fit(scrol_wind)
#
#             self.notebook.AddPage(scrol_wind, page_name, False)
#
#     # Обработчики
#     def show_command_details(self, command):
#         """Функция открытия диалога для просмотра подробной информации о команде (для контекстного меню)"""
#         dialog = ViewCommandData(self)  # Создаем экземпляр класса
#         # Задаем полям значения
#         dialog.command_db_label.SetLabel(command['commands_name'])
#         dialog.modul_db_label.SetLabel(command['cmd_assoc_module'][0])
#         dialog.description_text.WriteText(command['description_command'])
#         dialog.example_text.WriteText(command['command_example:'])
#         dialog.ShowModal()
#         dialog.Destroy()
#
#     def show_context_menu(self, data):
#         """Функция для контекстного меню"""
#         # Создаем меню
#         context_menu = wx.Menu()
#
#         # Добавляем опцию "Копировать"
#         copy_item = context_menu.Append(wx.ID_COPY, "Копировать")
#         self.Bind(wx.EVT_MENU, lambda event, cmd=data['commands_name']: self.copy_to_clipboard(cmd), copy_item)
#
#         # Добавляем опцию "Подробно"
#         show_item = context_menu.Append(wx.ID_ANY, "Подробно")
#         self.Bind(wx.EVT_MENU, lambda event, cmd=data: self.show_command_details(cmd), show_item)
#
#         # Добавляем опцию "Изменить"
#         edit_item = context_menu.Append(wx.ID_ANY, "Изменить")
#         self.Bind(wx.EVT_MENU, lambda event, cmd=data: self.edit_command(cmd), edit_item)
#
#         # Показываем контекстное меню
#         self.PopupMenu(context_menu)
#         context_menu.Destroy()
#
#     def copy_to_clipboard(self, value):
#         """Функция для копирования значения в буфер обмена"""
#         clipboard_data = wx.TextDataObject()
#         clipboard_data.SetText(value)
#         if wx.TheClipboard.Open():
#             wx.TheClipboard.SetData(clipboard_data)
#             wx.TheClipboard.Close()
#
#     # Обработчик для опции "Изменить"
#     def edit_command(self, command):
#         """Функция для редактирования команды"""
#         edit_dialog = AddCommandOrModule(parent=self)  # Создаем экземпляр класса
#         # делаем активной радиокнопку Изменить КОМАНДУ
#         edit_dialog.radio_edit_command.SetValue(True)
#         # Отключаем активность кнопок
#         edit_dialog.radio_add_command.Enable(False)
#         edit_dialog.radio_add_module.Enable(False)
#         # Явно вызываем обработчик, чтобы загрузить соответствующую панель в динамический сайзер
#         edit_dialog.on_radio_change(None)
#
#         # Задаем полям значения
#         # Устанавливаем значения в поля динамической панели
#         edit_dialog.sizer_DYNAMIC.GetChildren()[0].GetWindow().set_values(
#             command['commands_name'],
#             command['cmd_assoc_module'][0],
#             command['description_command'],
#             command['command_example:']
#         )
#
#         edit_dialog.ShowModal()
#         edit_dialog.Destroy()

import wx
from dialog_window.add_data_dialog import AddCommandOrModule
from dialog_window.view_command_dialog import ViewCommandData
from utils import database_queries


###########################################################################
# Class MyFrame
###########################################################################
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Блокнот команд", pos=wx.Point(0, 0), size=wx.Size(-1, -1),
                          style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE_BOX | wx.TAB_TRAVERSAL)
        # Устанавливаем пропорциональность окна в зависимости от разности разрешений мониторов
        # Это гарантирует что окно при запуске программы не будет больше самого разрешения монитора
        # и не будет сжато до состояния искажения контента в окне
        self.SetSizeHints(wx.Size(-1, -1), wx.DefaultSize)
        # Установка цвета фона окна (белый)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        # Устанавливаем минимальные размеры окна
        self.SetMinSize(wx.Size(600, 600))

        # Главный сайзер MAIN
        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.SetMinSize(wx.Size(600, 600))

        # ============== PanelCenter основное размещение данных из бд
        panel_center = PanelCenter(self)  # Экземпляр класса PanelCenter
        sizerMain.Add(panel_center, 1, wx.EXPAND, 5)  # Добавляем в сайзер DATA экземпляр класса PanelCenter
        # ==============================
        # panel = PanelCenter(self)
        # self.Show(True)

        self.SetSizer(sizerMain)  # Задаём основной сайзер для приложения
        self.Layout()
        sizerMain.Fit(self)


###########################################################################
# Class PanelCenter
###########################################################################
class PanelCenter(wx.Panel):
    """Центральная панель"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        sizer_main_panel = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), 0)
        sizer_main_panel.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer_main_panel)
        self.Layout()

        # Добавляем вкладки в главную панель
        self.add_tabs()

        # Список вкладок (модулей) панели notebook
        self.list_tabs_mod = [self.notebook.GetPage(i) for i in range(self.notebook.GetPageCount())]

        # ######################################
        # Загружаем данные для первой вкладки при запуске главной страницы (что-бы страница не была пустой)
        if not self.list_tabs_mod[0].data_loaded:
            first_tab = self.list_tabs_mod[0]
            # Запускаем загрузку команд для активной вкладки
            name_first_tb = self.notebook.GetPageText(0)
            self.add_cmd_to_tab(first_tab, name_first_tb)
        # ######################################

        # Привязываем событие выбора вкладки
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed, self.notebook)

    def add_tabs(self):
        """Функция для добавления вкладок в notebook"""
        # Получаем список объектов модулей из Бд
        lst_modules = database_queries.request_to_get_all_modules()
        for mod in lst_modules:
            mod_name = mod['module_name']
            tab = TabModule(self.notebook)  # Экземпляр вкладки
            # Добавляем объекты вкладки в список объект self.notebook
            self.notebook.AddPage(tab, mod_name, False)

    def on_page_changed(self, event):
        """Обработчик события выбираемой вкладки"""
        tab_selected_index = event.GetSelection()  # Получаем индекс выбранной вкладки
        obj_selected_tab = self.list_tabs_mod[tab_selected_index]  # Получаем объект выбранной вкладки
        selected_tab_name = self.notebook.GetPageText(tab_selected_index)  # Получаем имя активной вкладки
        # Проверяем, были ли данные уже загружены
        if not obj_selected_tab.data_loaded:
            # Запускаем загрузку команд для активной вкладки
            self.add_cmd_to_tab(obj_selected_tab, selected_tab_name)
            event.Skip()

    def add_cmd_to_tab(self, tab, name_mod):
        """Функция добавления связанных команд в активную вкладку"""
        # Получаем список связанных с вкладкой-модулем команд из БД на основании имени вкладки
        lst_cmd = database_queries.request_to_get_all_commands(name_mod)
        sizer_all_cmd = tab.scrol_wind.GetSizer()  # Получаем из scrol_wind(скроллинг) дочерний сайзер sizer_all_cmd (сайзер для списка команд)

        for cmd_obj in lst_cmd:  # Добавляем текст вкладки из списка
            print('cmd_obj', cmd_obj)
            # имя команды - cmd_obj['commands_name']
            # описание команды - cmd_obj['description']
            # ---------------------------------------------------------
            sizer_cmd = wx.BoxSizer(wx.HORIZONTAL)  # Создаем новый сайзер-КОМАНДЫ
            # Поле ИМЯ команды
            cmd_name = wx.StaticText(tab.scrol_wind, wx.ID_ANY, cmd_obj['commands_name'], wx.DefaultPosition, wx.Size(300, -1), 0 | wx.BORDER_STATIC)
            cmd_name.Wrap(-1)
            cmd_name.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет текста названия команды
            cmd_name.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
            sizer_cmd.Add(cmd_name, 0, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 5)
            # Поле ОПИСАНИЕ команды
            cmd_descr = wx.StaticText(tab.scrol_wind, wx.ID_ANY, cmd_obj['description_command'], wx.DefaultPosition, wx.Size(900, -1), 0 | wx.BORDER_STATIC)
            cmd_descr.Wrap(850)
            cmd_descr.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
            sizer_cmd.Add(cmd_descr, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

            sizer_all_cmd.Add(sizer_cmd, 0, wx.EXPAND, 5)
            # Плавная загрузка
            tab.scrol_wind.Layout()
            # ---------------------------------------------------------

            # --------------- Связываем событие с обработчиками -------
            # Открытие окна при нажатии (левой кнопкой мыши) на имени и описании команды
            cmd_name.Bind(wx.EVT_LEFT_DOWN, lambda event, cmd=cmd_obj: self.show_command_details(cmd))  # - на название команды
            cmd_descr.Bind(wx.EVT_LEFT_DOWN, lambda event, cmd=cmd_obj: self.show_command_details(cmd))  # - на описание команды

            # Открытие контекстного меню при нажатии (правой кнопкой мыши) на имени команды
            # - Копировать - в буфер обмена
            # - Подробно - открывает окно с подробной информацией
            cmd_name.Bind(wx.EVT_RIGHT_DOWN, lambda event, cmd=cmd_obj: self.show_context_menu(cmd))
            # --------------- END ------------------------------------

        # Отмечаем в объекте у флага data_loaded что данные о командах загружены
        tab.data_loaded = True
        # Обновляем расположение элементов в сайзере
        tab.scrol_wind.SetSizer(sizer_all_cmd)
        # tab.scrol_wind.Layout()
        sizer_all_cmd.Fit(tab.scrol_wind)
        tab.Layout()

    # Обработчики
    def show_command_details(self, command):
        """Функция открытия диалога для просмотра подробной информации о команде (для контекстного меню)"""
        dialog = ViewCommandData(self)  # Создаем экземпляр класса
        # Задаем полям значения
        dialog.command_db_label.SetLabel(command['commands_name'])
        dialog.modul_db_label.SetLabel(command['cmd_assoc_module'][0])
        dialog.description_text.WriteText(command['description_command'])
        dialog.example_text.WriteText(command['command_example:'])
        dialog.ShowModal()
        dialog.Destroy()

    def show_context_menu(self, data):
        """Функция для контекстного меню"""
        # Создаем меню
        context_menu = wx.Menu()

        # Добавляем опцию "Копировать"
        copy_item = context_menu.Append(wx.ID_COPY, "Копировать")
        self.Bind(wx.EVT_MENU, lambda event, cmd=data['commands_name']: self.copy_to_clipboard(cmd), copy_item)

        # Добавляем опцию "Подробно"
        show_item = context_menu.Append(wx.ID_ANY, "Подробно")
        self.Bind(wx.EVT_MENU, lambda event, cmd=data: self.show_command_details(cmd), show_item)

        # Добавляем опцию "Изменить"
        edit_item = context_menu.Append(wx.ID_ANY, "Изменить")
        self.Bind(wx.EVT_MENU, lambda event, cmd=data: self.edit_command(cmd), edit_item)

        # Показываем контекстное меню
        self.PopupMenu(context_menu)
        context_menu.Destroy()

    def copy_to_clipboard(self, value):
        """Функция для копирования значения в буфер обмена"""
        clipboard_data = wx.TextDataObject()
        clipboard_data.SetText(value)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard_data)
            wx.TheClipboard.Close()

    # Обработчик для опции "Изменить"
    def edit_command(self, command):
        """Функция для редактирования команды"""
        edit_dialog = AddCommandOrModule(parent=self)  # Создаем экземпляр класса
        # делаем активной радиокнопку Изменить КОМАНДУ
        edit_dialog.radio_edit_command.SetValue(True)
        # Скрываем радио-кнопки (добавить команду/модуль)
        edit_dialog.radio_add_command.Hide()
        edit_dialog.radio_add_module.Hide()
        # Явно вызываем обработчик, чтобы загрузить соответствующую панель в динамический сайзер
        edit_dialog.on_radio_change(None)

        # Задаем полям значения
        # Устанавливаем значения в поля динамической панели
        edit_dialog.sizer_DYNAMIC.GetChildren()[0].GetWindow().set_values(
            command['commands_name'],
            command['cmd_assoc_module'][0],
            command['description_command'],
            command['command_example:']
        )

        edit_dialog.ShowModal()
        edit_dialog.Destroy()


###########################################################################
# Class TabModule
###########################################################################
class TabModule(wx.Panel):
    """Вкладки-модули"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        self.data_loaded = False  # Флаг для отслеживания загружены ли данные о связанных командах в вкладку
        # -- Главный сайзер
        sizer_main_tab = wx.BoxSizer(wx.HORIZONTAL)

        # -- Скроллинг
        self.scrol_wind = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), wx.ALWAYS_SHOW_SB | wx.HSCROLL | wx.VSCROLL)
        self.scrol_wind.SetScrollRate(15, 15)

        # -- Сайзер СПИСКА команд
        sizer_all_cmd = wx.BoxSizer(wx.VERTICAL)

        # # -- Сайзер-КОМАНДЫ
        # sizer_cmd = wx.BoxSizer(wx.HORIZONTAL)
        # # Поле ИМЯ команды
        # self.cmd_name = wx.StaticText(self.scrol_wind, wx.ID_ANY, "Команда-1", wx.DefaultPosition, wx.Size(300, -1), 0 | wx.BORDER_STATIC)
        # self.cmd_name.Wrap(-1)
        # self.cmd_name.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        # sizer_cmd.Add(self.cmd_name, 0, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 5)
        # # Поле ОПИСАНИЕ команды
        # self.cmd_descr = wx.StaticText(self.scrol_wind, wx.ID_ANY, "Описание команды", wx.DefaultPosition, wx.Size(900, -1), 0 | wx.BORDER_STATIC)
        # self.cmd_descr.Wrap(-1)
        # self.cmd_descr.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        # sizer_cmd.Add(self.cmd_descr, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 5)
        #
        # sizer_all_cmd.Add(sizer_cmd, 0, wx.EXPAND, 5)

        self.scrol_wind.SetSizer(sizer_all_cmd)
        self.scrol_wind.Layout()
        sizer_all_cmd.Fit(self.scrol_wind)
        sizer_main_tab.Add(self.scrol_wind, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_main_tab)
        self.Layout()


###########################################################################
# Class LoadData
###########################################################################

class LoadData(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(350, 100), style=0)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.SetMinSize(wx.Size(350, -1))
        self.load = wx.StaticText(self, wx.ID_ANY, "Загрузка ...", wx.DefaultPosition, wx.DefaultSize, 0)
        self.load.Wrap(-1)

        self.load.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        main_sizer.Add(self.load, 0, wx.ALIGN_CENTER | wx.ALL, 15)

        self.m_gauge1 = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.m_gauge1.SetValue(100)
        main_sizer.Add(self.m_gauge1, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)


