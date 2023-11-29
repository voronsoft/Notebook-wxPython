import wx
import wx.xrc
from utils.database_queries import request_to_get_all_modules, request_to_get_all_commands, show_full_command_info
from dialog_window.view_command_dialog import ViewCommandData


###########################################################################
# Class PanelCenter
###########################################################################

class PanelCenter(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        # Установка цвета фона окна (например, белый)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        SizerPanel = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), 0)

        SizerPanel.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(SizerPanel)
        self.Layout()

        # Добавляем вкладки по названиям модулей
        self.add_tabs_to_scroll_window()

    # Добавляем вкладки по количеству модулей из БД
    def add_tabs_to_scroll_window(self):
        """Функция для добавления вкладок по количеству модулей из БД"""

        result = request_to_get_all_modules()  # Запрос к бд на получение модулей

        # Создаем вкладки исходя из количества модулей
        for ind, obj in enumerate(result):
            page_name = obj['module_name']
            page = wx.ScrolledWindow(self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
            page.SetScrollRate(5, 5)
            sizer_window_Modul = wx.BoxSizer(wx.VERTICAL)

            # Получаем данные из базы данных для текущего модуля
            commands_data = request_to_get_all_commands(modul_name=page_name)

            # Добавляем данные в текстовые поля каждой вкладки
            for command in commands_data:
                command_name = command['commands_name']
                description = command['description_command']

                text_ctrl_command = wx.TextCtrl(page, wx.ID_ANY, command_name, wx.DefaultPosition, wx.Size(300, -1), wx.TE_READONLY)
                text_ctrl_command.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
                text_ctrl_command.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет текста названия команды

                text_ctrl_description = wx.TextCtrl(page, wx.ID_ANY, description, wx.DefaultPosition, wx.Size(1300, -1), wx.TE_READONLY)
                text_ctrl_description.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

                sizer_command_data = wx.BoxSizer(wx.HORIZONTAL)
                sizer_command_data.Add(text_ctrl_command, 0, wx.ALL | wx.EXPAND, 0)
                sizer_command_data.Add(text_ctrl_description, 3, wx.ALL | wx.EXPAND, 0)

                # Добавляем данные в сайзер (каждую итерацию)
                sizer_window_Modul.Add(sizer_command_data, 0, wx.EXPAND, 3)
                # Связываем событие с открытием окна при нажатии на имя команды
                text_ctrl_command.Bind(wx.EVT_LEFT_DOWN, lambda event, cmd=command: self.show_command_details(cmd))

            page.SetSizer(sizer_window_Modul)
            page.Layout()
            sizer_window_Modul.Fit(page)

            self.notebook.AddPage(page, page_name, False)

    def show_command_details(self, command):
        print(command)
        dialog = ViewCommandData(self)
        dialog.command_db_label.SetLabel(command['commands_name'])
        dialog.modul_db_label.SetLabel(command['cmd_assoc_module'][0])
        # x['cmd_assoc_module'][0]
        dialog.description_text.WriteText(command['description_command'])
        dialog.example_text.WriteText(command['command_example:'])
        dialog.ShowModal()
        dialog.Destroy()
