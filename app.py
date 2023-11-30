import wx
import wx.xrc
from dialog_window.search_dialog import SearchDialog
from dialog_window.edit_data_dialog import EditCommandData
from dialog_window.panel_center_dialog import PanelCenter
from dialog_window.about_program_dialog import AboutProgram


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

        # Создаем системное меню
        menu_bar = wx.MenuBar()
        # Меню "Файл"
        file_menu = wx.Menu()
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
        self.add_button_data = wx.Button(self, wx.ID_ANY, "Добавить данные", wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_button_data.SetLabelMarkup("Добавить данные")
        self.add_button_data.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top_button.Add(self.add_button_data, 1, wx.ALL | wx.EXPAND, 5)
        self.show_button = wx.Button(self, wx.ID_ANY, "Поиск", wx.DefaultPosition, wx.DefaultSize, 0)
        self.show_button.SetLabelMarkup("Поиск")
        self.show_button.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top_button.Add(self.show_button, 1, wx.ALL | wx.EXPAND, 5)
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
        self.Layout()
        sizerMain.Fit(self)

        # Статус бар (нижняя часть окна)
        self.statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.Maximize()  # Максимизируем окно на весь экран

        # Подключение обработчиков
        self.add_button_data.Bind(wx.EVT_LEFT_DOWN, self.on_add_data_button_click)
        self.show_button.Bind(wx.EVT_LEFT_DOWN, self.search)
        self.close_button.Bind(wx.EVT_LEFT_DOWN, self.close_program)

    # ---------------- Обработчик события для кнопки "Добавить данные" ---------------
    def on_add_data_button_click(self, event):
        """Открытие диалога добавить данные"""
        dialog = EditCommandData(self)
        dialog.ShowModal()
        dialog.Destroy()

    # Обработчик события для кнопки "Поиск"
    def search(self, event):
        """Открытие диалога поиска"""
        dialog = SearchDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    # Обработчики событий для пунктов меню
    def show_documentation(self, event):
        """Открытие диалога документации"""
        pass

    def about_info(self, event):
        """Отображение информации о программе"""
        dialog = AboutProgram(self)
        dialog.ShowModal()
        dialog.Destroy()

    # Обработчик для кнопки "ВЫХОД"
    def close_program(self, event):
        """Закрытие программы"""
        self.Close()


if __name__ == '__main__':
    app = wx.App(False)
    frame = FrameMain(None)
    frame.Show(True)
    app.MainLoop()
