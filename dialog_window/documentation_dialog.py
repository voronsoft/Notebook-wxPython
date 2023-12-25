import os
import wx
import wx.xrc
import wx.html2
from utils.database_queries import clear_database
from instance.app_config import icons_folder_path, upd_db_folder_path, root_directory
from db.creat_db_and_data import create_database, added_command_data_db


###########################################################################
# Class DocumentationDialog
###########################################################################

class DocumentationDialog(wx.Dialog):
    """Документация"""

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Документация", pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.DEFAULT_DIALOG_STYLE)

        self.parent_dialog = self.GetParent()  # Родитель окна

        self.SetSizeHints(wx.Size(600, 600), wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        # Главный сайзер
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(600, 600))
        # Сайзер TOP
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.text_label_top = wx.StaticText(self, wx.ID_ANY, "Документация:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_label_top.Wrap(-1)
        self.text_label_top.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top.Add(self.text_label_top, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        # Разделитель
        self.line_a = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_top.Add(self.line_a, 0, wx.EXPAND | wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)

        # Сайзер DATA
        sizer_data = wx.BoxSizer(wx.VERTICAL)
        sizer_data.SetMinSize(wx.Size(600, 600))

        # -------------------------- # --------------------------
        self.html_win = wx.html2.WebView.New(self)
        self.html_win.SetMinSize(wx.Size(600, 600))
        # Путь к локальному HTML-файлу с документацией
        local_html_path = os.path.join(root_directory, 'html', 'documentation.html')
        # Загружаем страницу
        self.html_win.LoadURL("file://" + local_html_path)
        sizer_data.Add(self.html_win, 1, wx.ALL, 5)
        # -------------------------- # --------------------------

        sizer_data.Add((0, 0), 1, wx.EXPAND, 5)

        sizer_main.Add(sizer_data, 1, wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)
