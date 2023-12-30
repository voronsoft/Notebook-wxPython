import os
import wx
import wx.html
import wx.richtext
from instance.app_config import icons_folder_path


###########################################################################
# Class ViewCommandData
###########################################################################

class ViewCommandData(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='Данные о команде', pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)  # Задаем шрифт
        self.SetFont(font)

        # Устанавливаем иконку для окна
        icon = wx.Icon(f'{os.path.join(icons_folder_path, "notebook.ico")}', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Главный сайзер окна
        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_top = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top.SetMinSize(wx.Size(-1, 70))
        bSizer2_a = wx.BoxSizer(wx.VERTICAL)
        self.command_label = wx.StaticText(self, wx.ID_ANY, "Команда:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.command_label.Wrap(-1)
        bSizer2_a.Add(self.command_label, 0, wx.ALL, 5)
        self.command_db_label = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.command_db_label.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет для красного
        self.command_db_label.Wrap(-1)

        bSizer2_a.Add(self.command_db_label, 0, wx.ALL, 5)
        sizer_top.Add(bSizer2_a, 1, wx.EXPAND, 5)
        bSizer2_b = wx.BoxSizer(wx.VERTICAL)
        self.modul_label = wx.StaticText(self, wx.ID_ANY, "Модуль родитель:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.modul_label.Wrap(-1)
        bSizer2_b.Add(self.modul_label, 0, wx.ALL, 5)
        self.modul_db_label = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.modul_db_label.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет красный
        self.modul_db_label.Wrap(-1)

        bSizer2_b.Add(self.modul_db_label, 0, wx.ALL, 5)
        sizer_top.Add(bSizer2_b, 1, wx.EXPAND, 5)
        sizer_main.Add(sizer_top, 0, wx.ALL | wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer3_a = wx.BoxSizer(wx.HORIZONTAL)
        bSizer3_a.SetMinSize(wx.Size(100, -1))  # Устанавливаем ширину
        self.description_label = wx.StaticText(self, wx.ID_ANY, "Описание:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.description_label.Wrap(-1)
        bSizer3_a.Add(self.description_label, 0, wx.ALL, 5)
        bSizer3.Add(bSizer3_a, 0, wx.EXPAND, 5)
        bSizer3_b = wx.BoxSizer(wx.VERTICAL)
        self.description_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                         wx.DefaultSize, 0 | wx.BORDER_THEME | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        self.description_text.SetEditable(False)  # Делаем текст только для чтения

        bSizer3_b.Add(self.description_text, 1, wx.EXPAND | wx.ALL, 5)
        bSizer3.Add(bSizer3_b, 1, wx.EXPAND, 5)
        sizer_main.Add(bSizer3, 1, wx.ALL | wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer4_a = wx.BoxSizer(wx.VERTICAL)
        bSizer4_a.SetMinSize(wx.Size(100, -1))  # Устанавливаем ширину
        self.example_label = wx.StaticText(self, wx.ID_ANY, "Пример:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.example_label.Wrap(-1)
        bSizer4_a.Add(self.example_label, 1, wx.ALL, 5)
        bSizer4.Add(bSizer4_a, 0, wx.EXPAND, 5)
        bSizer4_b = wx.BoxSizer(wx.VERTICAL)
        self.example_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                     wx.DefaultSize, 0 | wx.BORDER_THEME | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        self.example_text.SetEditable(False)  # Делаем текст только для чтения

        bSizer4_b.Add(self.example_text, 1, wx.EXPAND | wx.ALL, 5)
        bSizer4.Add(bSizer4_b, 1, wx.EXPAND, 5)
        sizer_main.Add(bSizer4, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        self.Centre(wx.BOTH)
