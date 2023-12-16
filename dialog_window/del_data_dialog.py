import wx
import wx.xrc
from utils import database_queries
from dialog_window import panel_center_dialog
from utils.database_queries import request_to_get_all_modules, request_get_commands, del_module, del_command


# TODO после удаления команды нужно обновить данные на главной странице (удаленные команды остаются в списке)

###########################################################################
# Class DelCmdOrMod
###########################################################################
class DelCmdOrMod(wx.Dialog):
    """Главное окно удалить: Команду или Модуль"""

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Удалить данные", pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.DEFAULT_DIALOG_STYLE)

        self.parent_dialog = parent  # Родитель окна

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        # Главный сайзер окна
        self.sizer_main_dialog = wx.BoxSizer(wx.VERTICAL)
        self.sizer_main_dialog.SetMinSize(wx.Size(600, 600))

        #  Сайзер TOP
        sizer_radio_button = wx.BoxSizer(wx.HORIZONTAL)
        # РАДИО-КНОПКА - "Удалить МОДУЛЬ"
        self.radio_del_module = wx.RadioButton(self, wx.ID_ANY, "Удалить МОДУЛЬ", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_radio_button.Add(self.radio_del_module, 0, wx.ALL | wx.EXPAND, 5)

        # сайзер заполнитель
        self.static_text_empty = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        self.static_text_empty.Wrap(-1)
        sizer_radio_button.Add(self.static_text_empty, 0, wx.ALL, 5)

        # РАДИО-КНОПКА - "Удалить КОМАНДУ"
        self.radio_del_command = wx.RadioButton(self, wx.ID_ANY, "Удалить КОМАНДУ", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_radio_button.Add(self.radio_del_command, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer_main_dialog.Add(sizer_radio_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

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
        # ================== Заглушка ===================
        # ================ END Заглушка =================
        self.sizer_main_dialog.Add(self.sizer_DYNAMIC_del, 1, wx.EXPAND, 5)

        # Искусственно генерируем событие выбора активной радио-кнопки
        self.on_radio_change(event=self.radio_del_module)
        # Привязываем событие для выбора активной радиокнопки обработчик - on_radio_change
        self.radio_del_module.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
        self.radio_del_command.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
        # Привязываем событие при закрытии окна
        self.Bind(wx.EVT_CLOSE, self.on_close_dialog)

        self.SetSizer(self.sizer_main_dialog)
        self.Layout()
        self.sizer_main_dialog.Fit(self)
        self.Centre(wx.BOTH)

    # Обработчик поведения на выбор активной радио-кнопки
    def on_radio_change(self, event):
        # -- Удаляем все дочерние элементы из self.sizer_DYNAMIC_del (очищаем)
        for child in self.sizer_DYNAMIC_del.GetChildren():
            child.GetWindow().Destroy()

        if self.radio_del_module.GetValue():  # Есл активна радио-кнопка - "Удалить МОДУЛЬ"
            print('В диалоге "Удалить данные" активна радио-кнопка - "Удалить МОДУЛЬ"')
            del_mod_connect = PanelDelModule(self)  # Создаем экземпляр класса
            self.sizer_DYNAMIC_del.Add(del_mod_connect, 1, wx.EXPAND | wx.ALL, 5)

            self.sizer_DYNAMIC_del.Layout()
        elif self.radio_del_command.GetValue():  # Есл активна радио-кнопка - "Удалить КОМАНДУ"
            print('В диалоге "Удалить данные" активна радио-кнопка - "Удалить КОМАНДУ"')
            del_cmd_connect = PanelDelCommand(self)  # Экземпляр класса PanelDelCommand
            self.sizer_DYNAMIC_del.Add(del_cmd_connect, 1, wx.EXPAND | wx.ALL, 5)
            self.sizer_DYNAMIC_del.Fit(self)

        # Перераспределяем элементы и подгоняем размер
        self.Layout()
        self.sizer_DYNAMIC_del.Fit(self)

    # Обработчик события закрытия окна
    def on_close_dialog(self, event):
        """Закрытие диалогового окна"""
        # Отображаем диалоговое окно с сообщением
        message = f"После закрытия окна основной интерфейс будет обновлен\nс учетом удаленных данных."
        wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)

        # Вызываем стандартное событие закрытия окна
        self.Destroy()
        event.Skip()

        # Получаем объект главного окна приложения
        main_obj = self.parent_dialog
        print(f'родитель======== {main_obj}')
        # Обновляем данные в главном окне
        main_obj.update_main_window()


###########################################################################
# Class PanelDelModule
###########################################################################
class PanelDelModule(wx.Panel):
    """Удалить Модуль"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL, name="Удалить МОДУЛЬ"):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        self.parent_dialog = parent  # Родитель окна

        # Главный сайзер окна
        sizer_main_panel_del_mod = wx.BoxSizer(wx.VERTICAL)
        sizer_main_panel_del_mod.SetMinSize(wx.Size(600, 600))

        # Верхний сайзер
        sizer_top_inf = wx.BoxSizer(wx.VERTICAL)

        # Текстовое поле
        self.info_mod_label = wx.StaticText(self, wx.ID_ANY, "Удалить модуль (выберите из списка):", wx.DefaultPosition, wx.Size(-1, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.info_mod_label.Wrap(-1)
        sizer_top_inf.Add(self.info_mod_label, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        # Поле выбора удаляемого модуля из списка
        choice_modChoices = [mod_item['module_name'] for mod_item in request_to_get_all_modules()]  # Получаем список модулей
        self.choice_mod = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_modChoices, 0)
        self.choice_mod.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.choice_mod.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет для красного
        sizer_top_inf.Add(self.choice_mod, 0, wx.ALL | wx.EXPAND, 5)

        sizer_main_panel_del_mod.Add(sizer_top_inf, 0, wx.EXPAND, 5)

        # Сайзер данных
        sizer_data = wx.BoxSizer(wx.VERTICAL)
        self.info_cmd_label = wx.StaticText(self, wx.ID_ANY, "ВНИМАНИЕ !!! Связанные команды будут автоматически удалены:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.info_cmd_label.Wrap(-1)
        sizer_data.Add(self.info_cmd_label, 0, wx.ALL, 5)
        # Скроллинг для окна
        self.scrolled_window = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.scrolled_window.SetScrollRate(15, 15)
        sizer_data.Add(self.scrolled_window, 1, wx.EXPAND | wx.ALL, 5)

        sizer_main_panel_del_mod.Add(sizer_data, 1, wx.EXPAND, 5)

        # Сайзер кнопок
        sizer_bottom = wx.BoxSizer(wx.VERTICAL)
        self.button_apply = wx.Button(self, wx.ID_ANY, "Применить", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_bottom.Add(self.button_apply, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer_main_panel_del_mod.Add(sizer_bottom, 0, wx.EXPAND, 5)

        self.SetSizer(sizer_main_panel_del_mod)
        sizer_main_panel_del_mod.Fit(self)
        self.Layout()
        # Привязываем обработчик события к выбору модуля
        self.choice_mod.Bind(wx.EVT_CHOICE, self.on_module_select)
        # Привязываем обработчик для кнопки Применить
        self.button_apply.Bind(wx.EVT_BUTTON, self.del_module)

    # -------------------------- Обработчики ------------------------------
    def on_module_select(self, event):
        """Обработчик события выбора модуля"""
        selected_module = self.choice_mod.GetStringSelection()  # Получаем имя выбранного модуля
        commands = request_get_commands(selected_module)  # Запрашиваем команды для выбранного модуля
        # Создаем новый сайзер
        sizer_cmd_list = wx.BoxSizer(wx.VERTICAL)

        if self.scrolled_window.GetSizer():
            # Удаляем старый сайзер
            self.scrolled_window.DestroyChildren()
        # Добавляем команды
        for cmd in commands:
            btn_cmd = wx.Button(self.scrolled_window, wx.ID_ANY, cmd['commands_name'], wx.DefaultPosition, wx.DefaultSize, 0)
            btn_cmd.Enable(False)
            sizer_cmd_list.Add(btn_cmd, 0, wx.EXPAND | wx.ALL, 5)
            self.scrolled_window.Layout()

        self.scrolled_window.SetSizer(sizer_cmd_list)
        # Перестраиваем элементы в сайзере
        sizer_cmd_list.Fit(self.scrolled_window)
        self.Layout()

    def del_module(self, event):
        """Удаление модуля с его командами"""
        selected_module = self.choice_mod.GetStringSelection()  # Получаем имя выбранного модуля
        # Удаляем модуль и его команды из БД
        del_module(selected_module)

        # Обновляем список модулей в choice_mod
        choice_modChoices = [mod_item['module_name'] for mod_item in request_to_get_all_modules()]
        self.choice_mod.SetItems(choice_modChoices)

        # Очищаем окно от команд, которые были удалены
        if self.scrolled_window.GetSizer():
            sizer_cmd_list = self.scrolled_window.GetSizer()
            sizer_cmd_list.Clear(delete_windows=True)
            self.scrolled_window.Layout()
            self.Layout()


###########################################################################
# Class PanelDelCommand
###########################################################################
class PanelDelCommand(wx.Panel):
    """Удалить команду"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        self.parent_dialog = parent  # Родитель окна

        # Главный сайзер окна
        sizer_main_panel_del_cmd = wx.BoxSizer(wx.VERTICAL)
        sizer_main_panel_del_cmd.SetMinSize(wx.Size(600, 600))

        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), 0)
        sizer_main_panel_del_cmd.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer_main_panel_del_cmd)
        self.Layout()

        # Добавляем вкладки в главную панель
        self.add_tabs()

        # Список вкладок (модулей) панели notebook
        self.list_tabs_mod = [self.notebook.GetPage(i) for i in range(self.notebook.GetPageCount())]

        # ######################################
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
            tab = panel_center_dialog.TabModule(self.notebook)  # Экземпляр вкладки
            # Добавляем объекты вкладки в список объект self.notebook
            self.notebook.AddPage(tab, mod_name, False)

    def on_page_changed(self, event):
        """Обработчик события выбираемой вкладки"""
        tab_selected_index = event.GetSelection()  # Получаем индекс выбранной вкладки
        obj_selected_tab = self.list_tabs_mod[tab_selected_index]  # Получаем объект выбранной вкладки
        selected_tab_name = self.notebook.GetPageText(tab_selected_index)  # Получаем имя активной вкладки
        # Запускаем загрузку команд для активной вкладки
        self.add_cmd_to_tab(obj_selected_tab, selected_tab_name)
        event.Skip()

    def add_cmd_to_tab(self, tab, name_mod):
        """Функция добавления связанных команд в активную вкладку"""
        # Получаем список связанных с вкладкой-модулем команд из БД на основании имени вкладки
        lst_cmd = database_queries.request_get_commands(name_mod)
        sizer_all_cmd = tab.scrol_wind.GetSizer()  # Получаем из scrol_wind(скроллинг) дочерний сайзер sizer_all_cmd (сайзер для списка команд)

        # если сайзер не пустой очищаем, во избежании добавления команд после перезагрузки списка
        if sizer_all_cmd.GetChildren():
            sizer_all_cmd = tab.scrol_wind.GetSizer()  # Получаем сайзер со всеми командами
            sizer_all_cmd.Clear(delete_windows=True)  # Очищаем сайзер от старых данных
            # Обновляем расположение элементов в вкладке
            tab.scrol_wind.Layout()
            tab.Layout()

        for cmd_obj in lst_cmd:  # Добавляем текст вкладки из списка
            # ---------------------------------------------------------
            sizer_cmd = wx.BoxSizer(wx.HORIZONTAL)  # Создаем новый сайзер-КОМАНДЫ
            # Кнопки ИМЯ команды
            btn_cmd = wx.Button(tab.scrol_wind, wx.ID_ANY, cmd_obj['commands_name'], wx.DefaultPosition, wx.DefaultSize, 0)
            sizer_cmd.Add(btn_cmd, 1, wx.EXPAND | wx.ALL, 5)
            sizer_all_cmd.Add(sizer_cmd, 0, wx.EXPAND, 5)
            # Привязываем событие к каждой кнопке (удалить команду в БД)
            btn_cmd.Bind(wx.EVT_LEFT_DOWN, lambda event, cmd=cmd_obj: self.del_cmd(event, cmd, tab))
            # ---------------------------------------------------------

        # Обновляем расположение элементов в вкладке
        tab.scrol_wind.Layout()
        tab.Layout()

    def del_cmd(self, event, cmd, tab):
        """Удаление команды с БД и перезагрузка (обновление) активной вкладки"""
        del_command(cmd)  # Удаляем команду из БД
        # Обновляем флаг количества команд в объекте вкладке
        if tab.num_fields_cmd > 0:
            tab.num_fields_cmd -= 1

        # Очищаем элементы вкладки
        sizer_all_cmd = tab.scrol_wind.GetSizer()  # Получаем сайзер со всеми командами
        sizer_all_cmd.Clear(delete_windows=True)  # Очищаем сайзер от старых данных
        # Заново добавляем команды на вкладку (обновляем список команд с учетом того что удалили)
        self.add_cmd_to_tab(tab, self.notebook.GetPageText(self.notebook.GetSelection()))
        # Обновляем расположение элементов в вкладке
        tab.scrol_wind.Layout()
        tab.Layout()
