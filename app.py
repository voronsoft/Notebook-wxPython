import wx
from add_data_dialog import AddDataDialog
from command import ViewCommand


###########################################################################
# Class MainWindow
###########################################################################
class MainWindow(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)

        # Задаем параметры шрифта по умолчанию
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(font)
        wx.Font.SetWeight(font, wx.FONTWEIGHT_BOLD)

        # Создаем Меню
        self.menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        item = wx.MenuItem(fileMenu, wx.ID_EXIT, "Выход", "Выход из приложения")
        item.SetBitmap(wx.Bitmap("icons/exit.png"))
        fileMenu.Append(item)
        self.menubar.Append(fileMenu, "&File")

        search = wx.Menu()
        item5 = wx.MenuItem(search, wx.ID_EXIT, "Найти:", "Поиск команды в списке")
        item5.SetBitmap(wx.Bitmap("icons/search.png"))
        search.Append(item5)
        self.menubar.Append(search, "&Поиск")
        self.SetMenuBar(self.menubar)
        self.Maximize(True)
        # END Создаем меню

        # создаем панель
        panel = wx.Panel(self)

        # Создаем горизонтальный сизер для кнопок управления
        button_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Добавляем кнопку "Добавить данные"
        add_data_button = wx.Button(panel, label="Добавить данные")
        add_data_button.SetBitmap(wx.Bitmap("icons/add_data.png"))
        add_data_button.Bind(wx.EVT_BUTTON, self.on_add_data)
        # Добавляем кнопку "Посмотреть данные"
        view_data_button = wx.Button(panel, label="Посмотреть данные")
        view_data_button.SetBitmap(wx.Bitmap("icons/see_data.png"))
        view_data_button.Bind(wx.EVT_BUTTON, self.on_view_data)
        button_horizontal_sizer.Add(add_data_button, 0, wx.ALL, 5)
        button_horizontal_sizer.Add(view_data_button, 0, wx.ALL, 5)

        # Создаем вертикальный сизер
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        # Добавляем горизонтальный сизер в вертикальный
        vertical_sizer.Add(button_horizontal_sizer, 0, wx.ALL, 5)

        # Устанавливаем вертикальный сизер для окна
        panel.SetSizer(vertical_sizer)

    # обработчик события для кнопки - Добавить данные
    def on_add_data(self, event):
        add_data_dialog = AddDataDialog(self, title="Добавление данных")
        add_data_dialog.ShowModal()

    # обработчик события для кнопки - Посмотреть данные
    def on_view_data(self, event):
        add_data_dialog = ViewCommand(self, title="Данные о команде")
        add_data_dialog.ShowModal()
        print("Кнопка 'Посмотреть данные' нажата")


if __name__ == '__main__':
    app = wx.App(False)

    frame = MainWindow(None, title='Блокнот команд - PYTHON')
    frame.Show()
    app.MainLoop()
