import os
import wx
import wx.xrc
from instance.app_config import icons_folder_path
from utils.database_queries import request_to_get_all_modules, export_data_db_to_json_file


###########################################################################
# Class Export
###########################################################################

class ExportDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Экспорт", pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        # Устанавливаем иконку для окна
        icon = wx.Icon(f'{os.path.join(icons_folder_path, "notebook.ico")}', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        # Главный сайзер
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(600, 600))

        # Сайзер TOP
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.static_text_6 = wx.StaticText(self, wx.ID_ANY, "Экспортировать данные в файл", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text_6.Wrap(-1)
        self.static_text_6.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top.Add(self.static_text_6, 0, wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.ALIGN_CENTER, 5)

        self.line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.line, 0, wx.EXPAND | wx.ALL, 5)

        # Поле подсказки
        self.static_text_9 = wx.StaticText(self, wx.ID_ANY, "(Если ничего не выбрано то экcпортируется всё в файл.\nПуть к файлу папка: Документы.)", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.static_text_9.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет красный
        self.static_text_9.Wrap(-1)
        sizer_main.Add(self.static_text_9, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

        # Поле выбора вкладки (список)
        choice_module_choices = [mod_item['module_name'] for mod_item in request_to_get_all_modules()]
        self.choice_module = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_module_choices, 0)
        self.choice_module.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет красный
        self.choice_module.SetSelection(-1)
        self.choice_module.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_main.Add(self.choice_module, 0, wx.ALL | wx.EXPAND, 5)

        # Поле статус бара
        self.gauge = wx.Gauge(self, wx.ID_ANY, 1, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.gauge.SetValue(0)  # Задаём начальное значение строке статус бара
        sizer_main.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 5)

        # Заполнитель
        sizer_main.Add((0, 0), 1, wx.EXPAND, 5)

        # Кнопка - "Экспортировать"
        self.apply_btn = wx.Button(self, wx.ID_ANY, "Экспортировать", wx.DefaultPosition, wx.DefaultSize, 0)
        self.apply_btn.SetLabelMarkup("Экспортировать")
        self.apply_btn.SetBitmap(wx.Bitmap(os.path.join(icons_folder_path, 'export24.png'), wx.BITMAP_TYPE_ANY))
        sizer_main.Add(self.apply_btn, 0, wx.ALL, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # ------------ События --------------
        self.apply_btn.Bind(wx.EVT_BUTTON, self.apply_btn_handler)  # Событие для кнопки - Импортировать

    # ---------------- Обработчики событий--------------
    def apply_btn_handler(self, event):
        """Обработчик для кнопки Экспорт"""
        # Если выбран какой либо модуль из списка
        if self.choice_module.GetSelection() >= 0:
            # Получение значения индекса выбранного модуля
            selection_index_choice = self.choice_module.GetSelection()
            # Получаем текстовое значение поля выбора
            name_text_module = self.choice_module.GetString(selection_index_choice)
            # Экспортируем данные модуля в файл, передав в функцию имя модуля для экспорта списка записей
            export_data_db_to_json_file(name_text_module, gauge=self.gauge)
            # Очищаем значение выбранного модуля
            self.choice_module.SetSelection(-1)

        # Если не выбран ни один модуль, импортируем всю бд в файл
        # В папку системы - ДОКУМЕНТЫ
        elif self.choice_module.GetSelection() == -1:
            export_data_db_to_json_file(gauge=self.gauge)

        event.Skip()
