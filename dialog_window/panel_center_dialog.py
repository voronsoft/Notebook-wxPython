import wx
from utils import database_queries
from dialog_window.view_command_dialog import ViewCommandData
from dialog_window.edit_data_dialig import EditCommandOrModule


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

        # Добавляем вкладки в главную панель
        self.add_tabs()

        # Список вкладок (модулей) панели notebook
        self.list_tabs_mod = [self.notebook.GetPage(i) for i in range(self.notebook.GetPageCount())]

        # TODO если удалить все модули то приложение не запускается из за ошибки в строке 31
        # ######### Загружаем данные для первой вкладки при запуске главной страницы (что-бы страница не была пустой)
        # Если вкладка пустая (без команд)
        if self.list_tabs_mod[0].scrol_wind.GetSizer().GetItemCount() == 0:
            first_tab = self.list_tabs_mod[0]
            # Запускаем загрузку команд для активной вкладки
            name_first_tb = self.notebook.GetPageText(0)
            self.add_cmd_to_tab(first_tab, name_first_tb)

        # Привязываем событие выбора вкладки
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed, self.notebook)

        self.SetSizer(sizer_main_panel)
        self.Layout()

    def add_tabs(self):
        """Функция для добавления вкладок в notebook"""
        # Получаем список объектов модулей из Бд
        lst_modules = database_queries.request_to_get_all_modules()
        self.Freeze()  # Замораживаем обновление окна (убираем мерцание экрана при обновлении)
        for mod in lst_modules:
            mod_name = mod['module_name']
            tab = TabModule(self.notebook)  # Экземпляр вкладки
            # Добавляем объекты вкладки в список объект self.notebook
            self.notebook.AddPage(tab, mod_name, False)

        self.Thaw()  # Размораживаем обновление окна (убираем мерцание экрана при обновлении)
        self.Layout()

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

        self.Freeze()  # Замораживаем обновление окна (убираем мерцание экрана при обновлении)
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
        # Перерисовываем интерфейс
        tab.scrol_wind.Layout()
        self.Thaw()  # Размораживаем обновление окна (убираем мерцание экрана при обновлении)
        tab.Layout()  # Обновляем расположение элементов в вкладке

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
        self.Bind(wx.EVT_MENU, lambda event, cmd=data: self.edit_cmd(cmd), edit_item)

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
    def edit_cmd(self, command):
        """Функция для редактирования команды из контекстного меню"""
        edit_dialog = EditCommandOrModule(self)  # Создаем экземпляр класса
        edit_dialog.radio_edit_command.SetValue(True)  # Делаем активной радиокнопку - Изменить КОМАНДУ
        edit_dialog.radio_edit_module.SetValue(False)  # Параллельно деактивируем кнопку - Изменить МОДУЛЬ
        edit_dialog.radio_edit_module.Hide()  # Скрываем кнопку - "Изменить МОДУЛЬ"

        # Получаем объект окна - изменение команды
        edit_wnd = edit_dialog.GetChildren()[-1]

        # Скрываем нужный сайзер в окне, так как команда редактируется из контекстного меню
        edit_wnd.hide_child_elements('ctx')

        # Заполняем форму данными от команды которую будем изменять
        edit_wnd.cmd_data_name.SetValue(command['commands_name'])  # Название
        edit_wnd.mod_data_name.SetValue(command['cmd_assoc_module'][0])  # Модуль команды
        edit_wnd.new_name_inp_text.SetValue(command['commands_name'])  # Новое название команды
        edit_wnd.descr_inp_text.SetValue(command['description_command'])  # Описание
        edit_wnd.exampl_inp_text.SetValue(command['command_example:'])  # Пример
        # TODO не работает изменение команды через контекстное меню
        # Привязываем событие для кнопки "Применить", в созданном объекте(edit_dialog)
        edit_wnd.button_apply.Bind(wx.EVT_BUTTON, lambda event, obj=edit_wnd: self.on_btn_apply(obj))

        edit_dialog.ShowModal()  # Отображаем окно

    # ----------- Обработчик ----------
    def on_btn_apply(self, obj):
        """Изменяем данные о команде (через контекстное меню)"""
        # Получаем данные о команде из полей
        cmd = obj.cmd_data_name.GetValue()
        name_new = obj.new_name_inp_text.GetValue()
        descr_new = obj.descr_inp_text.GetValue()
        example_new = obj.exampl_inp_text.GetValue()
        # Изменяем данные команды
        database_queries.edit_command(cmd=cmd, name_new=name_new, descr_new=descr_new, example_new=example_new)

        # Отображаем диалоговое окно с сообщением
        message = f"Команда '{cmd}' изменена"
        wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)

        # Очищаем поля
        obj.cmd_data_name.Clear()
        obj.mod_data_name.Clear()
        obj.new_name_inp_text.Clear()
        obj.descr_inp_text.Clear()
        obj.exampl_inp_text.Clear()

        obj.GetParent().Destroy()  # Закрываем окно (высвобождаем пямять) изменения команды
        # Обновляем сайзер Data в главном окне приложения
        self.GetParent().update_main_window(self)


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
