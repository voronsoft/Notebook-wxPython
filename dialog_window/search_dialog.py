import wx
import wx.xrc
import wx.richtext
from utils.database_queries import request_to_get_all_modules, request_get_commands


###########################################################################
# Class SearchDialog
###########################################################################

class SearchDialog(wx.Dialog):
    """Поиск"""

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Поиск", pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        # Главный сайзер окна
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(600, 600))

        # Сайзер TOP
        sizer_top = wx.BoxSizer(wx.HORIZONTAL)
        # Поле поиска
        # TODO доделать поиск по совпадению части слова
        self.searchCtrl = wx.SearchCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(212, -1), wx.TE_LEFT)
        self.searchCtrl.ShowSearchButton(True)
        self.searchCtrl.ShowCancelButton(False)
        self.searchCtrl.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.searchCtrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        # Кнопка поиска
        self.search_button = wx.Button(self, wx.ID_ANY, "Поиск", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_top.Add(self.searchCtrl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 5)
        sizer_top.Add(self.search_button, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 4)
        # Привязываем обработчик события
        self.search_button.Bind(wx.EVT_BUTTON, self.on__click)
        self.searchCtrl.Bind(wx.EVT_SEARCH, self.on__click)

        sizer_main.Add(sizer_top, 0, wx.ALL | wx.EXPAND, 5)

        # Сайзер выбора (команды и модули)
        sizer_choice = wx.GridSizer(0, 2, 0, 0)

        self.module_label = wx.StaticText(self, wx.ID_ANY, "Модуль", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL | wx.BORDER_THEME)
        self.module_label.Wrap(-1)
        self.module_label.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_choice.Add(self.module_label, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 5)

        self.command_label = wx.StaticText(self, wx.ID_ANY, "Команда", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL | wx.BORDER_THEME)
        self.command_label.Wrap(-1)
        self.command_label.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_choice.Add(self.command_label, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 5)

        modules_choiceChoices = [mod_item['module_name'] for mod_item in request_to_get_all_modules()]  # Получаем список модулей
        self.modules_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, modules_choiceChoices, 0 | wx.BORDER_SIMPLE)
        # Привязываем обработчик события к выбору модуля
        self.modules_choice.Bind(wx.EVT_CHOICE, self.on_module_select)

        self.modules_choice.SetSelection(0)
        self.modules_choice.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_choice.Add(self.modules_choice, 1, wx.ALL | wx.EXPAND, 5)
        sizer_main.Add(sizer_choice, 0, wx.ALL | wx.EXPAND, 5)

        commands_choiceChoices = [item['commands_name'] for item in request_get_commands(modules_choiceChoices[0])]
        self.commands_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, commands_choiceChoices, 0 | wx.BORDER_SIMPLE)
        # Привязываем обработчик события к выбору команды
        self.commands_choice.Bind(wx.EVT_CHOICE, self.on_command_select)

        self.commands_choice.SetSelection(0)
        self.commands_choice.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_choice.Add(self.commands_choice, 1, wx.ALL | wx.EXPAND, 5)

        # Сайзер вывода основных данных
        sizer_data = wx.BoxSizer(wx.VERTICAL)

        self.description_label = wx.StaticText(self, wx.ID_ANY, "Описание:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.description_label.Wrap(-1)
        self.description_label.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        sizer_data.Add(self.description_label, 0, wx.ALL, 5)

        # Поле вывода данных
        self.description_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_THEME | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        self.description_text.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.description_text.SetEditable(False)  # Делаем текст только для чтения

        sizer_data.Add(self.description_text, 1, wx.EXPAND | wx.ALL, 5)

        sizer_main.Add(sizer_data, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        self.Layout()
        self.Centre(wx.BOTH)

    # Обработчики
    def on__click(self, event):
        """Функция поиска"""
        self.description_text.Clear()  # Очистка поля описания команды
        input_text_search = self.searchCtrl.GetValue()  # Получаем текст в строке поиска
        self.searchCtrl.Clear()  # Очистка поля после нажатия кнопки запуска поиска
        result = f'Вы искали: {input_text_search}\n'
        self.description_text.SetValue(result)

    def on_module_select(self, event):
        """Обработчик события выбора модуля"""
        selected_module = self.modules_choice.GetStringSelection()  # Получаем выбранный модуль
        commands = request_get_commands(selected_module)  # Запрашиваем команды для выбранного модуля
        # Обновляем список команд в self.commands_choice
        self.commands_choice.SetItems([command['commands_name'] for command in commands])
        self.commands_choice.SetSelection(0)  # Выбираем первую команду по умолчанию
        self.description_text.Clear()  # Очистка поля описания команды если был выбран другой модуль

    def on_command_select(self, event):
        """Обработчик события выбора команды"""
        selected_module = self.modules_choice.GetStringSelection()  # Получаем выбранный модуль
        selected_command = self.commands_choice.GetStringSelection()  # Получаем выбранную команду
        commands = request_get_commands(selected_module)  # Запрашиваем команды для выбранного модуля
        command_info = [command for command in commands if command['commands_name'] == selected_command]
        if command_info:
            description_text = (f"Описание команды:\n{command_info[0]['description_command']}\n\n"
                                f"Пример использования:\n{command_info[0]['command_example:']}")
            self.description_text.SetValue(description_text)
