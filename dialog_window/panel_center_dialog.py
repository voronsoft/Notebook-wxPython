import wx
from utils import database_queries
from dialog_window.add_data_dialog import AddCommandOrModule
from dialog_window.view_command_dialog import ViewCommandData


###########################################################################
# Class PanelCenter
###########################################################################
class PanelCenter(wx.Panel):
    """Центральная панель"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        # Главный сайзер диалога
        sizer_main_panel = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), 0)
        sizer_main_panel.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer_main_panel)
        self.Layout()

        # Добавляем вкладки в главную панель
        self.add_tabs()

        # Список вкладок (модулей) панели notebook
        self.list_tabs_mod = [self.notebook.GetPage(i) for i in range(self.notebook.GetPageCount())]

        # TODO если удалить все модули то приложение не запускается из за ошибки в строке 31
        # ######################################
        # Загружаем данные для первой вкладки при запуске главной страницы (что-бы страница не была пустой)
        if self.list_tabs_mod[0].scrol_wind.GetSizer().GetItemCount() == 0:
            first_tab = self.list_tabs_mod[0]
            # Запускаем загрузку команд для активной вкладки
            name_first_tb = self.notebook.GetPageText(0)
            self.add_cmd_to_tab(first_tab, name_first_tb)

        elif self.list_tabs_mod[0].scrol_wind.GetSizer().GetItemCount() > 0:
            name_mod = self.notebook.GetPageText(0)  # Получаем имя первой вкладки
            num_cmd_mod_obj = self.list_tabs_mod[0].num_fields_cmd  # Получаем кол команд в объекте
            num_cmd_mod_db = database_queries.count_commands_in_module(name_mod)  # Получаем кол команд из БД
            if num_cmd_mod_db != num_cmd_mod_obj:
                print(f'Количество команд:')
                print(f'В объекте: {num_cmd_mod_obj}')
                print(f'В БД для объекта: {num_cmd_mod_db}')

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
        num_fields_cmd_db = database_queries.count_commands_in_module(selected_tab_name)  # Получаем количество команд из БД для активной вкладки

        # Проверяем, были ли данные уже загружены
        if obj_selected_tab.num_fields_cmd == 0:  # Если нет команд
            # Запускаем загрузку команд для активной вкладки
            self.add_cmd_to_tab(obj_selected_tab, selected_tab_name)
            event.Skip()

        # Если что-то было загружено, сравниваем кол команд из БД с кол в самом объекте.
        if obj_selected_tab.num_fields_cmd != num_fields_cmd_db:
            # Очищаем сайзер от прошлых команд
            sizer_all_cmd = obj_selected_tab.scrol_wind.GetSizer()  # Получаем сайзер со всеми командами
            sizer_all_cmd.Clear(delete_windows=True)  # Очищаем сайзер от старых данных
            # Запускаем загрузку команд для активной вкладки
            self.add_cmd_to_tab(obj_selected_tab, selected_tab_name)
            # Обновляем расположение элементов в вкладке
            obj_selected_tab.scrol_wind.Layout()
            obj_selected_tab.Layout()

            event.Skip()

    def add_cmd_to_tab(self, tab, name_mod):
        """Функция добавления связанных команд в активную вкладку"""
        # Получаем список связанных с вкладкой-модулем команд из БД на основании имени вкладки
        lst_cmd = database_queries.request_get_commands(name_mod)
        sizer_all_cmd = tab.scrol_wind.GetSizer()  # Получаем из scrol_wind(скроллинг) дочерний сайзер sizer_all_cmd (сайзер для списка команд)

        for cmd_obj in lst_cmd:  # Добавляем текст вкладки из списка
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
            # Открытие окна "ПОДРОБНО О КОМАНДЕ" при нажатии (левой кнопкой мыши) на имени и описании команды
            cmd_name.Bind(wx.EVT_LEFT_DOWN, lambda event, cmd=cmd_obj: self.show_command_details(cmd))  # - на название команды
            cmd_descr.Bind(wx.EVT_LEFT_DOWN, lambda event, cmd=cmd_obj: self.show_command_details(cmd))  # - на описание команды

            # Открытие контекстного меню при нажатии (правой кнопкой мыши) на названии команды
            # - Копировать - в буфер обмена
            # - Подробно - открывает окно с подробной информацией
            cmd_name.Bind(wx.EVT_RIGHT_DOWN, lambda event, cmd=cmd_obj: self.show_context_menu(cmd))
            # --------------- END ------------------------------------

        # Отмечаем в объекте у флага num_fields_cmd количество загруженных команд
        tab.num_fields_cmd = tab.scrol_wind.GetSizer().GetItemCount()
        # Обновляем расположение элементов в вкладке
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
        """Функция контекстного меню"""
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

    # ----------- Функции ----------
    def update_cmd(self):
        """Обновление сайзера c перечнем команд"""


###########################################################################
# Class TabModule
###########################################################################
class TabModule(wx.Panel):
    """Вкладки-модули"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        # Флаг для отслеживания количества загруженных команд в вкладку
        self.num_fields_cmd = 0

        # -- Главный сайзер
        sizer_main_tab = wx.BoxSizer(wx.HORIZONTAL)

        # -- Скроллинг
        self.scrol_wind = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), wx.ALWAYS_SHOW_SB | wx.HSCROLL | wx.VSCROLL)
        self.scrol_wind.SetScrollRate(15, 15)

        # -- Сайзер СПИСКА команд
        sizer_all_cmd = wx.BoxSizer(wx.VERTICAL)
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
