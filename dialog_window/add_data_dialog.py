import wx
import wx.xrc
import wx.richtext


###########################################################################
# Class AddCommandModule
###########################################################################

class AddCommandOrModule(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Добавить данные", pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(600, 600))
        sizer_top = wx.GridSizer(0, 3, 0, 0)

        self.command_name_label = wx.StaticText(self, wx.ID_ANY, "Команда:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.command_name_label.Wrap(-1)
        sizer_top.Add(self.command_name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        self.module_name_label = wx.StaticText(self, wx.ID_ANY, "Модуль:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.module_name_label.Wrap(-1)
        sizer_top.Add(self.module_name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        self.modulr_list = wx.StaticText(self, wx.ID_ANY, "Список модулей:", wx.DefaultPosition, wx.Size(250, -1), wx.ALIGN_CENTER_HORIZONTAL)
        self.modulr_list.Wrap(-1)
        sizer_top.Add(self.modulr_list, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        self.cmd_data_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, -1), 0 | wx.BORDER_SIMPLE)
        self.cmd_data_name.SetMaxSize(wx.Size(300, -1))
        sizer_top.Add(self.cmd_data_name, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        self.mod_data_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, -1), 0 | wx.BORDER_SIMPLE)
        self.mod_data_name.SetMaxSize(wx.Size(300, -1))
        sizer_top.Add(self.mod_data_name, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        choice_moduleChoices = []
        self.choice_module = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(250, -1), choice_moduleChoices, 0 | wx.BORDER_SIMPLE)
        self.choice_module.SetSelection(0)
        self.choice_module.SetMaxSize(wx.Size(300, -1))
        sizer_top.Add(self.choice_module, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        sizer_main.Add(sizer_top, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        sizer_data = wx.BoxSizer(wx.VERTICAL)

        self.description_label = wx.StaticText(self, wx.ID_ANY, "Описание:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.description_label.Wrap(-1)
        sizer_data.Add(self.description_label, 0, wx.ALL, 5)

        self.description_data = wx.richtext.RichTextCtrl(self, wx.ID_ANY, "Текст описания", wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_SIMPLE | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        sizer_data.Add(self.description_data, 1, wx.EXPAND | wx.ALL, 5)

        self.example_label = wx.StaticText(self, wx.ID_ANY, "Пример:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.example_label.Wrap(-1)
        sizer_data.Add(self.example_label, 0, wx.ALL, 5)

        self.example_data = wx.richtext.RichTextCtrl(self, wx.ID_ANY, "Пример кода...", wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_SIMPLE | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        sizer_data.Add(self.example_data, 1, wx.EXPAND | wx.ALL, 5)

        sizer_main.Add(sizer_data, 1, wx.ALL | wx.EXPAND, 5)

        sizer_bottom = wx.StdDialogButtonSizer()
        self.sizer_bottomOK = wx.Button(self, wx.ID_OK)
        sizer_bottom.AddButton(self.sizer_bottomOK)
        self.sizer_bottomCancel = wx.Button(self, wx.ID_CANCEL)
        sizer_bottom.AddButton(self.sizer_bottomCancel)
        sizer_bottom.Realize()

        sizer_main.Add(sizer_bottom, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)
