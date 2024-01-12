import os
import wx
import wx.xrc

from instance.app_config import icons_folder_path


###########################################################################
# Class Export
###########################################################################

class ExportDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Экспорт", pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(600, 600))
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, "Экспортировать данные в файла", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)

        self.m_staticText6.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        sizer_top.Add(self.m_staticText6, 0, wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.ALIGN_CENTER, 5)

        self.line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.line, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, "(Если ничего не выбрано то экcпортируется всё в файл)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        sizer_main.Add(self.m_staticText9, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

        choice_moduleChoices = []
        self.choice_module = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_moduleChoices, 0)
        self.choice_module.SetSelection(0)
        self.choice_module.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        sizer_main.Add(self.choice_module, 0, wx.ALL | wx.EXPAND, 5)

        sizer_main.Add((0, 0), 1, wx.EXPAND, 5)

        self.apply_btn = wx.Button(self, wx.ID_ANY, "Применить", wx.DefaultPosition, wx.DefaultSize, 0)
        self.apply_btn.SetLabelMarkup("Применить")
        self.apply_btn.SetBitmap(wx.Bitmap(os.path.join(icons_folder_path, 'export24.png'), wx.BITMAP_TYPE_ANY))
        sizer_main.Add(self.apply_btn, 0, wx.ALL, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.apply_btn.Bind(wx.EVT_BUTTON, self.apply_btn_handler)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def apply_btn_handler(self, event):
        event.Skip()
