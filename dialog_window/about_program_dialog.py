import os
import wx
import wx.xrc
import wx.adv
from instance.app_config import icons_folder_path


###########################################################################
# Class AboutProgram
###########################################################################

class AboutProgram(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="О программе", pos=wx.DefaultPosition, size=wx.Size(400, 200), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        # Устанавливаем иконку для окна
        icon = wx.Icon(f'{os.path.join(icons_folder_path, "notebook.ico")}', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(300, 150))

        sizer_top = wx.BoxSizer(wx.HORIZONTAL)

        self.icon_devel = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(os.path.join(icons_folder_path, "linkedIn24.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_top.Add(self.icon_devel, 0, wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        self.developer = wx.StaticText(self, wx.ID_ANY, "Разработчик:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.developer.Wrap(-1)
        self.developer.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top.Add(self.developer, 0, wx.ALL, 5)

        self.link_developer = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, "Alex Norov (LinkedIn)", "https://www.linkedin.com/in/alexandr-norov-71b26810b/", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE)
        self.link_developer.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top.Add(self.link_developer, 0, wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.ALL | wx.EXPAND, 5)

        sizer_line = wx.BoxSizer(wx.VERTICAL)

        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_line.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)

        sizer_main.Add(sizer_line, 0, wx.EXPAND, 5)

        sixer_center = wx.BoxSizer(wx.HORIZONTAL)

        self.m_bitmap2 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(os.path.join(icons_folder_path, "git_repo24.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        sixer_center.Add(self.m_bitmap2, 0, wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        self.repository = wx.StaticText(self, wx.ID_ANY, "Репозиторий программы:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.repository.Wrap(-1)
        self.repository.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sixer_center.Add(self.repository, 0, wx.ALL, 5)

        self.link_repository = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, "GitHub", "https://github.com/voronsoft/Notebook-wxPython", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE)
        self.link_repository.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        sixer_center.Add(self.link_repository, 0, wx.ALL, 5)

        sizer_main.Add(sixer_center, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()

        self.Centre(wx.BOTH)
