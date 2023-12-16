import wx
import wx.xrc
import wx.richtext


###########################################################################
# Class EditCommandOrModule
###########################################################################
class EditCommandOrModule(wx.Dialog):
    """Главное окно изменить: Команду или Модуль"""

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Изменить данные", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        # Главный сайзер окна
        sizer_main_dialog = wx.BoxSizer(wx.VERTICAL)
        sizer_main_dialog.SetMinSize(wx.Size(600, 600))

        # Сайзер радио-кнопок
        sizer_radio_button = wx.BoxSizer(wx.HORIZONTAL)
        # КНОПКА - "Изменить МОДУЛЬ"
        self.radio_edit_module = wx.RadioButton(self, wx.ID_ANY, "Изменить МОДУЛЬ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.radio_edit_module.SetValue(True)
        sizer_radio_button.Add(self.radio_edit_module, 0, wx.ALL | wx.EXPAND, 5)
        # Заполнитель
        self.static_text_empty = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        sizer_radio_button.Add(self.static_text_empty, 0, wx.ALL, 5)
        # КНОПКА - "Изменить КОМАНДУ"
        self.radio_edit_command = wx.RadioButton(self, wx.ID_ANY, "Изменить КОМАНДУ", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_radio_button.Add(self.radio_edit_command, 0, wx.ALL | wx.EXPAND, 5)
        sizer_main_dialog.Add(sizer_radio_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        # Сайзер разделительной линии
        sizer_line = wx.BoxSizer(wx.VERTICAL)
        self.static_line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_line.Add(self.static_line, 0, wx.EXPAND | wx.ALL, 5)
        sizer_main_dialog.Add(sizer_line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        # ------------------- Динамический сайзер для активации нужного класса ------------
        # При выборе активной радио-кнопки сайзер будет подключать соответствующий класс диалога
        # или изменить модуль - Class PanelDelModule
        # или изменить команду - Class PanelDelCommand
        self.sizer_DYNAMIC_edit = wx.BoxSizer(wx.VERTICAL)
        sizer_main_dialog.Add(self.sizer_DYNAMIC_edit, 1, wx.EXPAND, 5)
        # --------------------------------- END ----------------------------

        # Искусственно генерируем событие выбора активной радио-кнопки
        self.on_radio_change(event=self.radio_edit_module)
        # Привязываем обработчик on_radio_change к событию изменения радио кнопок
        self.radio_edit_module.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
        self.radio_edit_command.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
        # Привязываем событие при закрытии окна
        self.Bind(wx.EVT_CLOSE, self.on_close_dialog)

        self.SetSizer(sizer_main_dialog)
        self.Layout()
        sizer_main_dialog.Fit(self)
        self.Centre(wx.BOTH)

    # -------------------------- Обработчики ------------------------------
    # Обработчик поведения на выбор активной радиокнопки
    def on_radio_change(self, event):
        """Обработчик поведения на выбор активной радиокнопки"""
        # Удаляем все дочерние элементы из self.sizer_DYNAMIC_edit
        for child in self.sizer_DYNAMIC_edit.GetChildren():
            child.GetWindow().Destroy()

        if self.radio_edit_command.GetValue():
            command_connect = PanelEditCommand(self)  # Создаем экземпляр класса
            self.sizer_DYNAMIC_edit.Add(command_connect, 1, wx.EXPAND | wx.ALL, 5)

        elif self.radio_edit_module.GetValue():
            module_connect = PanelEditModule(self)  # Создаем экземпляр класса
            self.sizer_DYNAMIC_edit.Add(module_connect, 1, wx.EXPAND | wx.ALL, 5)

        # Перераспределяем элементы и подгоняем размер
        self.Layout()
        self.sizer_DYNAMIC_edit.Fit(self)

    # Обработчик события закрытия окна
    def on_close_dialog(self, event):
        """Закрытие диалогового окна"""
        self.Destroy()


###########################################################################
# Class PanelEditModule
###########################################################################
class PanelEditModule(wx.Panel):
    """Изменить модуль"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=0, name="Удалить МОДУЛЬ"):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        # Главный сайзер
        sizer_main_panel_edit_mod = wx.BoxSizer(wx.VERTICAL)

        sizer_main_panel_edit_mod.SetMinSize(wx.Size(600, 600))
        sizer_data = wx.BoxSizer(wx.VERTICAL)

        self.choice_mod_label = wx.StaticText(self, wx.ID_ANY, "Выберите модуль:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.choice_mod_label.Wrap(-1)

        sizer_data.Add(self.choice_mod_label, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)

        choice_modChoices = []
        self.choice_mod = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_modChoices, 0)
        self.choice_mod.SetSelection(0)
        self.choice_mod.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))

        sizer_data.Add(self.choice_mod, 0, wx.ALL | wx.EXPAND, 5)

        self.name_mod_label = wx.StaticText(self, wx.ID_ANY, "Название:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.name_mod_label.Wrap(-1)

        sizer_data.Add(self.name_mod_label, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)

        self.name_mod_text = wx.TextCtrl(self, wx.ID_ANY, "Модуль тест", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_data.Add(self.name_mod_text, 0, wx.EXPAND | wx.ALL, 5)

        self.descr_mod_label = wx.StaticText(self, wx.ID_ANY, "Описание:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.descr_mod_label.Wrap(-1)

        sizer_data.Add(self.descr_mod_label, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)

        self.descr_mod_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, "Описание модуля", wx.DefaultPosition, wx.DefaultSize, 0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        sizer_data.Add(self.descr_mod_text, 1, wx.EXPAND | wx.ALL, 5)

        sizer_main_panel_edit_mod.Add(sizer_data, 1, wx.EXPAND, 5)

        sizer_bottom = wx.BoxSizer(wx.VERTICAL)

        self.button_apply = wx.Button(self, wx.ID_ANY, "Применить", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_bottom.Add(self.button_apply, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        sizer_main_panel_edit_mod.Add(sizer_bottom, 0, wx.EXPAND, 5)

        self.SetSizer(sizer_main_panel_edit_mod)
        self.Layout()
        sizer_main_panel_edit_mod.Fit(self)


###########################################################################
# Class PanelEditCommand
###########################################################################
class PanelEditCommand(wx.Panel):
    """Изменить команду"""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        # Главный сайзер
        sizer_main_panel_edit_cmd = wx.BoxSizer(wx.VERTICAL)

        sizer_main_panel_edit_cmd.SetMinSize(wx.Size(600, 600))
        sizer_data = wx.BoxSizer(wx.VERTICAL)

        self.choice_mod_label = wx.StaticText(self, wx.ID_ANY, "Выберите модуль:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.choice_mod_label.Wrap(-1)

        sizer_data.Add(self.choice_mod_label, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)

        choice_modChoices = []
        self.choice_mod = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_modChoices, 0)
        self.choice_mod.SetSelection(0)
        sizer_data.Add(self.choice_mod, 0, wx.ALL | wx.EXPAND, 5)

        self.choice_cmd_label = wx.StaticText(self, wx.ID_ANY, "Выберите команду:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.choice_cmd_label.Wrap(-1)

        sizer_data.Add(self.choice_cmd_label, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)

        choice_cmdChoices = []
        self.choice_cmd = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_cmdChoices, 0)
        self.choice_cmd.SetSelection(0)
        sizer_data.Add(self.choice_cmd, 0, wx.ALL | wx.EXPAND, 5)

        self.name_label = wx.StaticText(self, wx.ID_ANY, "Название:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.name_label.Wrap(-1)

        sizer_data.Add(self.name_label, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)

        self.name_inp_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_data.Add(self.name_inp_text, 0, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        self.descr_label = wx.StaticText(self, wx.ID_ANY, "Описание:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.descr_label.Wrap(-1)

        sizer_data.Add(self.descr_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)

        self.descr_inp_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, "Описание модуля", wx.DefaultPosition, wx.Size(-1, 200), 0 | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        self.descr_inp_text.SetMinSize(wx.Size(-1, 200))

        sizer_data.Add(self.descr_inp_text, 2, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        self.exampl_label = wx.StaticText(self, wx.ID_ANY, "Пример:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.exampl_label.Wrap(-1)

        sizer_data.Add(self.exampl_label, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)

        self.exampl_inp_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, "Пример описания", wx.DefaultPosition, wx.Size(-1, 200), 0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        self.exampl_inp_text.SetMinSize(wx.Size(-1, 100))

        sizer_data.Add(self.exampl_inp_text, 1, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        sizer_main_panel_edit_cmd.Add(sizer_data, 1, wx.EXPAND, 5)

        sizer_bottom = wx.BoxSizer(wx.VERTICAL)

        self.button_apply = wx.Button(self, wx.ID_ANY, "Применить", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_bottom.Add(self.button_apply, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        sizer_main_panel_edit_cmd.Add(sizer_bottom, 0, wx.EXPAND, 5)

        self.SetSizer(sizer_main_panel_edit_cmd)
        self.Layout()
        sizer_main_panel_edit_cmd.Fit(self)


if __name__ == '__main__':
    app = wx.App(False)
    frame = EditCommandOrModule(None)
    frame.Show(True)
    app.MainLoop()