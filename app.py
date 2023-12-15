import wx
import wx.xrc
from dialog_window.search_dialog import SearchDialog
from dialog_window.del_data_dialog import DelCmdOrMod
from dialog_window.panel_center_dialog import PanelCenter
from dialog_window.about_program_dialog import AboutProgram
from dialog_window.add_data_dialog import AddCommandOrModule
from dialog_window.edit_data_dialig import EditCommandOrModule


###########################################################################
# Class FrameMain
###########################################################################

class FrameMain(wx.Frame):
    """
    Схема расположения сайзеров
    #################################
    #             MAIN              #
    #   #########################   #
    #   #         TOP           #   #
    #   #########################   #
    #   #         DATA          #   #
    #   #    (PanelCenter)      #   #
    #   #########################   #
    #   #        BOTTOM         #   #
    #   #########################   #
    #   #     status bar        #   #
    #   #########################   #
    #################################

    """

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Блокнот команд", pos=wx.Point(1, 1), size=wx.Size(-1, -1),
                          style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE_BOX | wx.TAB_TRAVERSAL)
        # Устанавливаем пропорциональность окна в зависимости от разности разрешений мониторов
        # Это гарантирует что окно при запуске программы не будет больше самого разрешения монитора
        # и не будет сжато до состояния искажения контента в окне
        self.SetSizeHints(wx.Size(-1, -1), wx.DefaultSize)
        # Установка цвета фона окна (белый)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        # Устанавливаем минимальные размеры окна
        self.SetMinSize(wx.Size(600, 600))

        # Создаем системное меню
        menu_bar = wx.MenuBar()
        # Меню "Файл"
        file_menu = wx.Menu()
        add_data_menu_item = file_menu.Append(wx.ID_ANY, "Добавить данные", "Добавить Команду или Модуль")
        self.Bind(wx.EVT_MENU, self.add_data_button_click, add_data_menu_item)
        exit_menu_item = file_menu.Append(wx.ID_EXIT, "Выход", "Закрыть программу")
        self.Bind(wx.EVT_MENU, self.close_program, exit_menu_item)
        menu_bar.Append(file_menu, "Файл")
        # Меню "Справка"
        help_menu = wx.Menu()
        documentation_menu_item = help_menu.Append(wx.ID_ANY, "Документация", "Открыть документацию")
        about_menu_item = help_menu.Append(wx.ID_ANY, "About (о программе)", "About (о программе)")
        self.Bind(wx.EVT_MENU, self.show_documentation, documentation_menu_item)
        self.Bind(wx.EVT_MENU, self.about_info, about_menu_item)
        menu_bar.Append(help_menu, "Help")
        # Устанавливаем созданное меню
        self.SetMenuBar(menu_bar)

        # Главный сайзер MAIN
        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.SetMinSize(wx.Size(600, 600))

        # Сайзер - TOP
        sizer_top_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top_button.SetMinSize(wx.Size(600, 50))

        self.add_button_data = wx.Button(self, wx.ID_ANY, "Добавить", wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_button_data.SetLabelMarkup("Добавить")
        self.add_button_data.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top_button.Add(self.add_button_data, 1, wx.ALL | wx.EXPAND, 5)

        self.edit_button_data = wx.Button(self, wx.ID_ANY, "Изменить", wx.DefaultPosition, wx.DefaultSize, 0)
        self.edit_button_data.SetLabelMarkup("Изменить")
        self.edit_button_data.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top_button.Add(self.edit_button_data, 1, wx.ALL | wx.EXPAND, 5)

        self.del_button_data = wx.Button(self, wx.ID_ANY, "Удалить", wx.DefaultPosition, wx.DefaultSize, 0)
        self.del_button_data.SetLabelMarkup("Удалить")
        self.del_button_data.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top_button.Add(self.del_button_data, 1, wx.ALL | wx.EXPAND, 5)

        self.search_button = wx.Button(self, wx.ID_ANY, "Поиск", wx.DefaultPosition, wx.DefaultSize, 0)
        self.search_button.SetLabelMarkup("Поиск")
        self.search_button.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top_button.Add(self.search_button, 1, wx.ALL | wx.EXPAND, 5)
        sizerMain.Add(sizer_top_button, 0, wx.EXPAND, 5)  # Добавляем сайзер TOP в главный сайзер MAIN

        # Сайзер - DATA (основное размещение данных из бд)
        sizer_data = wx.BoxSizer(wx.VERTICAL)
        panel_center = PanelCenter(self)  # Экземпляр класса PanelCenter (данные из бд в основном сайзере DATA)
        sizer_data.Add(panel_center, 0, wx.EXPAND, 5)  # Добавляем в сайзер DATA экземпляр класса PanelCenter
        sizerMain.Add(sizer_data, 1, wx.EXPAND, 5)  # Добавляем в сайзер MAIN сайзер DATA

        # Сайзер - BOTTOM
        sizer_bottom = wx.BoxSizer(wx.VERTICAL)
        self.close_button = wx.Button(self, wx.ID_ANY, "Выход", wx.DefaultPosition, wx.DefaultSize, 0)
        self.close_button.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_bottom.Add(self.close_button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizerMain.Add(sizer_bottom, 0, wx.EXPAND, 5)  # Добавляем в сайзер MAIN сайзер BOTTOM

        self.SetSizer(sizerMain)  # Задаём основной сайзер для приложения
        self.Layout()  # Перестраиваем интерфейс
        sizerMain.Fit(self)

        # Статус бар (нижняя часть окна)
        self.statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.Maximize()  # Максимизируем окно на весь экран

        # Подключение обработчиков
        self.add_button_data.Bind(wx.EVT_LEFT_DOWN, self.add_data_button_click)
        self.edit_button_data.Bind(wx.EVT_LEFT_DOWN, self.edit_data_button_click)
        self.del_button_data.Bind(wx.EVT_LEFT_DOWN, self.del_data_button_click)
        self.search_button.Bind(wx.EVT_LEFT_DOWN, self.search)
        self.close_button.Bind(wx.EVT_LEFT_DOWN, self.close_program)

    # ---------------- Обработчики события---------------
    def add_data_button_click(self, event):
        """Открытие диалога добавить данные о команде или модуле"""
        add_dialog = AddCommandOrModule(self)
        add_dialog.radio_edit_command.Hide()  # Скрываем радиокнопку - Изменить КОМАНДУ
        add_dialog.ShowModal()
        add_dialog.Destroy()

    def edit_data_button_click(self, event):
        """Открытие диалога изменить данные о команде или модуле"""
        add_dialog = EditCommandOrModule(self)
        add_dialog.ShowModal()
        add_dialog.Destroy()

    def del_data_button_click(self, event):
        """Открытие окна Удалить данные"""
        print('Включен диалог - "Удалить данные"')
        del_dialog = DelCmdOrMod(self)
        del_dialog.ShowModal()
        del_dialog.Destroy()

    def search(self, event):
        """Открытие диалога поиска"""
        search_dialog = SearchDialog(self)
        search_dialog.ShowModal()
        search_dialog.Destroy()

    # ----------------  Обработчики событий для пунктов системного меню ----------------
    def show_documentation(self, event):
        """Открытие диалога документации"""
        pass

    def about_info(self, event):
        """Отображение информации о программе"""
        dialog = AboutProgram(self)
        dialog.ShowModal()
        dialog.Destroy()

    def close_program(self, event):
        """Закрытие программы"""
        self.Destroy()

    def add_cmd_mod_data(self):
        """Открытие диалога для добавления данных в программу"""
        dialog = AddCommandOrModule(self)
        dialog.ShowModal()
        dialog.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = FrameMain(None)
    frame.Show(True)
    app.MainLoop()
