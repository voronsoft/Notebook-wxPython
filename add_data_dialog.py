import wx
import wx.richtext


###########################################################################
# Class AddDataDialog
###########################################################################

class AddDataDialog(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='Добавить данные о команде', pos=wx.DefaultPosition, size=wx.Size(600, 600),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)

        # Задаем параметры шрифта по умолчанию
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(font)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer2.SetMinSize(wx.Size(-1, 70))
        bSizer2_a = wx.BoxSizer(wx.VERTICAL)
        self.add_command_label = wx.StaticText(self, wx.ID_ANY, "Команда:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_command_label.Wrap(-1)
        bSizer2_a.Add(self.add_command_label, 0, wx.ALL, 5)
        self.add_command_db_label = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_command_db_label.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.add_command_db_label.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет для красного

        bSizer2_a.Add(self.add_command_db_label, 0, wx.ALL | wx.EXPAND, 5)
        bSizer2.Add(bSizer2_a, 1, wx.EXPAND, 5)
        bSizer2_b = wx.BoxSizer(wx.VERTICAL)
        self.add_command_db_label = wx.StaticText(self, wx.ID_ANY, "Модуль родитель:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_command_db_label.Wrap(-1)
        bSizer2_b.Add(self.add_command_db_label, 0, wx.ALL, 5)
        self.add_modul_db_label = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_modul_db_label.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.add_modul_db_label.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет для красного

        bSizer2_b.Add(self.add_modul_db_label, 0, wx.ALL | wx.EXPAND, 5)
        bSizer2.Add(bSizer2_b, 1, wx.EXPAND, 5)
        bSizer1.Add(bSizer2, 0, wx.ALL | wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer3_a = wx.BoxSizer(wx.HORIZONTAL)
        bSizer3_a.SetMinSize(wx.Size(100, -1))  # Устанавливаем ширину
        self.add_description_label = wx.StaticText(self, wx.ID_ANY, "Описание", wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_description_label.Wrap(-1)
        bSizer3_a.Add(self.add_description_label, 0, wx.ALL, 5)
        bSizer3.Add(bSizer3_a, 0, wx.EXPAND, 5)
        bSizer3_b = wx.BoxSizer(wx.VERTICAL)
        self.add_description_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        bSizer3_b.Add(self.add_description_text, 1, wx.EXPAND | wx.ALL, 5)
        bSizer3.Add(bSizer3_b, 1, wx.EXPAND, 5)
        bSizer1.Add(bSizer3, 1, wx.ALL | wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer4_a = wx.BoxSizer(wx.VERTICAL)
        bSizer4_a.SetMinSize(wx.Size(100, -1))  # Устанавливаем ширину
        self.add_example_label = wx.StaticText(self, wx.ID_ANY, "Пример:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.add_example_label.Wrap(-1)
        bSizer4_a.Add(self.add_example_label, 1, wx.ALL, 5)
        bSizer4.Add(bSizer4_a, 0, wx.EXPAND, 5)
        bSizer14 = wx.BoxSizer(wx.VERTICAL)
        self.add_example_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)

        bSizer14.Add(self.add_example_text, 1, wx.EXPAND | wx.ALL, 5)
        bSizer4.Add(bSizer14, 1, wx.EXPAND, 5)
        bSizer1.Add(bSizer4, 1, wx.ALL | wx.EXPAND, 5)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, wx.ID_ANY, "Добавить", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.ok_button, 0, wx.ALL, 5)
        self.cancel_button2 = wx.Button(self, wx.ID_ANY, "Отмена", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.cancel_button2, 0, wx.ALL, 5)
        bSizer1.Add(bSizer5, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

# class AddDataDialog(wx.Dialog):
#     def __init__(self, parent, title):
#         wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='Добавить данные о команде', pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
# 
#         # Задаем параметры шрифта по умолчанию
#         self.default_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
# 
#         self.module_label = wx.StaticText(self, label="Модуль-родитель команды:")
#         self.module_label.SetFont(self.default_font)  
#         self.module_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
#         self.module_text.SetForegroundColour(wx.Colour(255, 0, 0))  # Устанавливаем красный цвет текста
#         self.module_text.SetMinSize((450, -1))  # Установите размер по вашему выбору
#         self.module_text.SetFont(self.default_font)  
# 
#         self.command_label = wx.StaticText(self, label="Команда:")
#         self.command_label.SetFont(self.default_font)  
#         self.command_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
#         self.command_text.SetFont(self.default_font)  
# 
#         self.description_label = wx.StaticText(self, label="Описание:")
#         self.description_label.SetFont(self.default_font)  
#         self.description_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
#         self.description_text.SetMinSize((-1, 150))  # Установите размер по вашему выбору
#         self.description_text.SetFont(self.default_font)  
# 
#         self.example_label = wx.StaticText(self, label="Пример:")
#         self.example_label.SetFont(self.default_font)  
#         self.example_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
#         self.example_text.SetMinSize((-1, 150))  # Установите размер по вашему выбору
#         self.example_text.SetFont(self.default_font)  
# 
#         # кнопки формы
#         self.ok_button = wx.Button(self, label="Добавить")
#         self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
#         # Устанавливаем больший размер шрифта
#         font_size1 = self.ok_button.GetFont()
#         font_size1.SetPointSize(12)  # Размер шрифта 12
#         self.ok_button.SetFont(font_size1)
# 
#         self.cancel_button = wx.Button(self, label="Отмена")
#         self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
#         # Устанавливаем больший размер шрифта
#         font_size2 = self.cancel_button.GetFont()
#         font_size2.SetPointSize(12)  # Размер шрифта 12
#         self.cancel_button.SetFont(font_size1)
# 
#         # Создаем сетку для размещения элементов формы
#         self.grid = wx.FlexGridSizer(5, 2, 10, 10)
#         self.grid.AddMany([
#             self.module_label,
#             (self.module_text, 1, wx.EXPAND),
#             self.command_label,
#             (self.command_text, 1, wx.EXPAND),
#             self.description_label,
#             (self.description_text, 1, wx.EXPAND),
#             self.example_label,
#             (self.example_text, 1, wx.EXPAND),
#             self.ok_button,
#             self.cancel_button,
#         ])
# 
#         # Создаем главный сизер и добавляем в него сетку
#         self.main_sizer = wx.BoxSizer(wx.VERTICAL)
#         self.main_sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 10)
# 
#         # Устанавливаем главный сизер для диалога
#         self.SetSizer(self.main_sizer)
# 
#         # Устанавливаем минимальный размер после добавления всех элементов
#         self.SetMinSize(self.GetSize())
# 
#         # Вызываем Fit и Layout для правильного распределения элементов
#         self.Fit()
#         self.Layout()
#         # Центрируем окно на экране
#         self.CentreOnScreen(wx.BOTH)
# 
#     def on_ok(self, event):
#         module_name = self.module_text.GetValue()
#         command_name = self.command_text.GetValue()
#         description = self.description_text.GetValue()
#         example = self.example_text.GetValue()
# 
#         if module_name and command_name:
#             # Тут ты можешь использовать полученные значения
#             # Например, добавить запись в базу данных или выполнить другие действия
#             print(f"Название модуля: {module_name}")
#             print(f"Команда: {command_name}")
#             print(f"Описание: {description}")
#             print(f"Пример: {example}")
# 
#             self.EndModal(wx.ID_OK)
#             self.Fit()
#             self.Layout()
# 
#     def on_cancel(self, event):
#         self.EndModal(wx.ID_CANCEL)
#         self.Fit()
#         self.Layout()
