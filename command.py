import wx
import wx.html
import wx.richtext


###########################################################################
# Class ViewCommand
###########################################################################

class ViewCommand(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='Данные о команде', pos=wx.DefaultPosition, size=wx.Size(600, 600),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)

        # Задаем параметры шрифта по умолчанию
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(font)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer2.SetMinSize(wx.Size(-1, 70))
        bSizer2_a = wx.BoxSizer(wx.VERTICAL)
        self.command_label = wx.StaticText(self, wx.ID_ANY, "Команда:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.command_label.Wrap(-1)
        bSizer2_a.Add(self.command_label, 0, wx.ALL, 5)
        self.command_db_label = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.command_db_label.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.command_db_label.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет для красного
        self.command_db_label.Wrap(-1)
        # ----
        # Переменная с данными
        command_data = "Текст из переменной"
        # Вставляем данные из переменной в StaticText для поля command_db_label
        self.command_db_label.SetLabel(command_data)
        # ----
        bSizer2_a.Add(self.command_db_label, 0, wx.ALL, 5)
        bSizer2.Add(bSizer2_a, 1, wx.EXPAND, 5)
        bSizer2_b = wx.BoxSizer(wx.VERTICAL)
        self.modul_label = wx.StaticText(self, wx.ID_ANY, "Модуль родитель:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.modul_label.Wrap(-1)
        bSizer2_b.Add(self.modul_label, 0, wx.ALL, 5)
        self.modul_db_label = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.modul_db_label.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.modul_db_label.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет для красного
        self.modul_db_label.Wrap(-1)
        # ----
        # Переменная с данными
        modul_data = "Текст из переменной"
        # Вставляем данные из переменной в StaticText для поля command_db_label
        self.modul_db_label.SetLabel(modul_data)
        # ----
        bSizer2_b.Add(self.modul_db_label, 0, wx.ALL, 5)
        bSizer2.Add(bSizer2_b, 1, wx.EXPAND, 5)
        bSizer1.Add(bSizer2, 0, wx.ALL | wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer3_a = wx.BoxSizer(wx.HORIZONTAL)
        bSizer3_a.SetMinSize(wx.Size(100, -1))  # Устанавливаем ширину
        self.description_label = wx.StaticText(self, wx.ID_ANY, "Описание:", wx.DefaultPosition, wx.DefaultSize, 0)
        wx.Font.SetWeight(font, wx.FONTWEIGHT_NORMAL)
        self.description_label.Wrap(-1)
        bSizer3_a.Add(self.description_label, 0, wx.ALL, 5)
        bSizer3.Add(bSizer3_a, 0, wx.EXPAND, 5)
        bSizer3_b = wx.BoxSizer(wx.VERTICAL)
        self.description_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        self.description_text.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.description_text.SetEditable(False)  # Делаем текст только для чтения
        db_content_description = "Ваш текст здесь.\nВторая строка"  # Переменная с данными
        self.description_text.WriteText(db_content_description)  # Добавляем текст из переменной в RichTextCtrl

        bSizer3_b.Add(self.description_text, 1, wx.EXPAND | wx.ALL, 5)
        bSizer3.Add(bSizer3_b, 1, wx.EXPAND, 5)
        bSizer1.Add(bSizer3, 1, wx.ALL | wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer4_a = wx.BoxSizer(wx.VERTICAL)
        bSizer4_a.SetMinSize(wx.Size(100, -1))  # Устанавливаем ширину
        self.example_label = wx.StaticText(self, wx.ID_ANY, "Пример:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.example_label.Wrap(-1)
        bSizer4_a.Add(self.example_label, 1, wx.ALL, 5)
        bSizer4.Add(bSizer4_a, 0, wx.EXPAND, 5)
        bSizer4_b = wx.BoxSizer(wx.VERTICAL)
        # self.example_text = wx.html.HtmlWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO)
        self.example_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        self.example_text.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.example_text.SetEditable(False)  # Делаем текст только для чтения
        db_content_example = "Ваш текст здесь.\nВторая строка\nТретья строка."  # Переменная с данными
        self.example_text.WriteText(db_content_example)  # Добавляем текст из переменной в RichTextCtrl

        bSizer4_b.Add(self.example_text, 1, wx.EXPAND | wx.ALL, 5)
        bSizer4.Add(bSizer4_b, 1, wx.EXPAND, 5)
        bSizer1.Add(bSizer4, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

# import wx
#
#
# class ViewCommand(wx.Dialog):
#     def __init__(self, parent, title):
#         super(ViewCommand, self).__init__(parent, title=title)
#
#         # Задаем параметры шрифта по умолчанию
#         self.default_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
#         # Устанавливаем размер окна
#         self.SetSize(wx.Size(600, 600))
#         # Центрируем окно на экране
#         self.CentreOnScreen(wx.BOTH)
#         # -----------------------------
#
#         # создаем панель
#         panel = wx.Panel(self)
#
#         # 1 Создаем горизонтальный сизер - команды
#         command_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
#         # Добавляем элементы в горизонтальный сизер
#         command = wx.StaticText(panel, label="Команда:")
#         command.SetFont(self.default_font)
#         command_text = wx.StaticText(panel, label="вставить код из БД")
#         command_text.SetFont(self.default_font)
#         command_horizontal_sizer.Add(command, 0, wx.ALL, 5)
#         command_horizontal_sizer.Add(command_text, 0, wx.ALL, 5)
#
#         # 2 Создаем горизонтальный сизер - описания
#         description_horizontal_sizer = wx.BoxSizer(wx.VERTICAL)
#         # Добавляем элементы в горизонтальный сизер
#         description = wx.StaticText(panel, label="Описание:")
#         description.SetFont(self.default_font)
#         description_text = wx.TextCtrl(panel, value="вставить код из БД", style=wx.TE_MULTILINE)
#         description_text.SetMinSize((600, 250))
#         description_text.SetFont(self.default_font)
#         description_horizontal_sizer.Add(description, 0, wx.ALL, 5)
#         description_horizontal_sizer.Add(description_text, 0, wx.ALL, 5)
#
#         # 3 Создаем горизонтальный сизер - пример
#         example_horizontal_sizer = wx.BoxSizer(wx.VERTICAL)
#         # Добавляем элементы в горизонтальный сизер
#         example = wx.StaticText(panel, label="Пример:")
#         example.SetFont(self.default_font)
#         example_text = wx.TextCtrl(panel, value="вставить код из БД", style=wx.TE_MULTILINE)
#         example_text.SetMinSize((600, 250))
#         example_text.SetFont(self.default_font)
#         example_horizontal_sizer.Add(example, 0, wx.ALL, 5)
#         example_horizontal_sizer.Add(example_text, 0, wx.ALL, 5)
#
#         # Создаем вертикальный сизер
#         vertical_sizer = wx.BoxSizer(wx.VERTICAL)
#
#         # Добавляем горизонтальные сизеры в вертикальный
#         vertical_sizer.Add(command_horizontal_sizer, 0, wx.ALL, 5)
#         vertical_sizer.Add(description_horizontal_sizer, 0, wx.ALL, 5)
#         vertical_sizer.Add(example_horizontal_sizer, 0, wx.ALL, 5)
#
#         # Устанавливаем вертикальный сизер для окна
#         panel.SetSizer(vertical_sizer)
