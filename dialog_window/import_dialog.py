import os

import wx
import wx.xrc
import wx.richtext

import wx
import wx.xrc
import wx.richtext

from instance.app_config import icons_folder_path


###########################################################################
# Class Import
###########################################################################

class ImportDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Импорт", pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(600, 600))
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.import_static_text = wx.StaticText(self, wx.ID_ANY, "Импортировать данные в программу", wx.DefaultPosition, wx.DefaultSize, 0)
        self.import_static_text.Wrap(-1)

        self.import_static_text.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        sizer_top.Add(self.import_static_text, 0, wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.ALIGN_CENTER, 5)

        self.choice_file = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, "Select a file", "*.json*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        sizer_main.Add(self.choice_file, 0, wx.ALL | wx.EXPAND, 5)

        self.line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.line, 0, wx.EXPAND | wx.ALL, 5)

        self.rich_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_SIMPLE | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        self.rich_text.SetEditable(False)  # Делаем текст только для чтения
        sizer_main.Add(self.rich_text, 1, wx.EXPAND | wx.ALL, 5)

        self.apply_btn = wx.Button(self, wx.ID_ANY, "Применить", wx.DefaultPosition, wx.DefaultSize, 0)
        self.apply_btn.SetLabelMarkup("Применить")
        self.apply_btn.SetBitmap(wx.Bitmap(os.path.join(icons_folder_path, 'import24.png'), wx.BITMAP_TYPE_ANY))
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
