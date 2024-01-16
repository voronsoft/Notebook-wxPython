import os
import wx
import json
import codecs
import wx.xrc
import wx.stc
from logs.app_logger import logger_debug
from instance.app_config import icons_folder_path
from utils.database_queries import import_data_json_from_db


###########################################################################
# Class Import
###########################################################################

class ImportDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Импорт", pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_FRAME_STYLE)

        self.parent_dialog = self.GetParent()  # Родитель окна

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        # Устанавливаем иконку для окна
        icon = wx.Icon(f'{os.path.join(icons_folder_path, "notebook.ico")}', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Главный сайзер
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(600, 600))

        #  Сайзер TOP
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.import_static_text = wx.StaticText(self, wx.ID_ANY, "Импорт данных в программу из файла JSON", wx.DefaultPosition, wx.DefaultSize, 0)
        self.import_static_text.Wrap(-1)
        self.import_static_text.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top.Add(self.import_static_text, 0, wx.ALL, 5)

        self.import_static_text_2 = wx.StaticText(self, wx.ID_ANY, "Пояснение смотреть: HELP -> Документация", wx.DefaultPosition, wx.DefaultSize, 0)
        self.import_static_text_2.SetForegroundColour(wx.Colour(255, 0, 0))  # RGB цвет красный
        self.import_static_text_2.Wrap(-1)
        self.import_static_text_2.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top.Add(self.import_static_text_2, 0, wx.ALIGN_CENTER, 5)

        sizer_main.Add(sizer_top, 0, wx.ALIGN_CENTER, 5)

        #  Поле выбора файла для импорта
        self.choice_file = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, "Select a file", "*.json*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        sizer_main.Add(self.choice_file, 0, wx.ALL | wx.EXPAND, 5)
        #  Разделитель
        self.line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.line, 0, wx.EXPAND | wx.ALL, 5)

        # Поле статус бара
        self.gauge = wx.Gauge(self, wx.ID_ANY, 1, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.gauge.SetValue(0)  # Задаём начальное значение строке статус бара
        sizer_main.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 5)

        # Поле вывода импортируемых данных
        self.scintilla = wx.stc.StyledTextCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(600, 600), wx.BORDER_SIMPLE)
        self.scintilla.SetLexer(wx.stc.STC_LEX_JSON)  # Устанавливаем лексер для JSON
        # Стили для различных элементов синтаксиса JSON
        self.scintilla.StyleSetSpec(wx.stc.STC_JSON_DEFAULT, "fore:#000000,face:%(mono)s")
        self.scintilla.StyleSetSpec(wx.stc.STC_JSON_NUMBER, "fore:#007F00,face:%(mono)s")
        self.scintilla.StyleSetSpec(wx.stc.STC_JSON_STRING, "fore:#7F007F,face:%(mono)s")
        self.scintilla.StyleSetSpec(wx.stc.STC_JSON_STRINGEOL, "fore:#7F007F,face:%(mono)s")
        self.scintilla.StyleSetSpec(wx.stc.STC_JSON_PROPERTYNAME, "fore:#FF0000,face:%(mono)s")  # Красный цвет для ключей
        self.scintilla.StyleSetSpec(wx.stc.STC_JSON_ESCAPESEQUENCE, "fore:#FF0000,face:%(mono)s")
        self.scintilla.StyleSetSpec(wx.stc.STC_JSON_BLOCKCOMMENT, "fore:#007F00,face:%(mono)s")
        # END стили
        sizer_main.Add(self.scintilla, 1, wx.EXPAND | wx.ALL, 5)

        # Кнопка - "Импортировать"
        self.apply_btn = wx.Button(self, wx.ID_ANY, "Импортировать", wx.DefaultPosition, wx.DefaultSize, 0)
        self.apply_btn.SetLabelMarkup("Импортировать")
        self.apply_btn.SetBitmap(wx.Bitmap(os.path.join(icons_folder_path, 'import24.png'), wx.BITMAP_TYPE_ANY))
        sizer_main.Add(self.apply_btn, 0, wx.ALL, 5)
        # Поведение кнопки активна\неактивна
        if not self.choice_file.GetPath():
            self.apply_btn.Disable()
        else:
            self.apply_btn.Enable()

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # ------------ События --------------
        self.choice_file.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_selected)  # Событие выбора файла
        self.apply_btn.Bind(wx.EVT_BUTTON, self.apply_btn_handler_import_data)  # Событие для кнопки - Импортировать

    # ---------------- Обработчики событий---------------
    def on_file_selected(self, event):
        """Обработчик события выбора файла."""
        # Получаем путь к выбранному файлу
        selected_file_path = self.choice_file.GetPath()
        if selected_file_path and os.path.exists(selected_file_path):
            self.apply_btn.Enable()  # Делаем кнопку ИМПОРТИРОВАТЬ активной
            try:
                with open(selected_file_path, 'r', encoding='utf-8') as file_data:
                    data = json.load(file_data)
                    # Преобразуем данные в формат JSON
                    json_data = json.dumps(data, indent=4)
                    # Декодируем строки Unicode в удобочитаемый формат
                    pretty_data_decoded = codecs.decode(json_data, 'unicode_escape')
                    # Добавляем в окно программы полученные данные для просмотра (визуализации)
                    self.scintilla.ClearAll()  # Очищаем поле от данных
                    self.scintilla.SetText(pretty_data_decoded)  # Добавляем данные в поле
                    self.scintilla.SetReadOnly(True)  # Делаем текст только для чтения
            except Exception as e:
                logger_debug.exception(f'Ошибка при считывании и обработке данных из файла JSON: {e}')

    def apply_btn_handler_import_data(self, event):
        """Импорт данных"""
        # Получаем путь к выбранному файлу
        path_file_json_data = self.choice_file.GetPath()

        # Выводим сообщение о ходе процесса импорта данных из файла json  в БД
        info_add = wx.BusyInfo("Ожидайте, идет процес ИМПОРТА данных...")
        # Вызовите функцию импорта
        result = import_data_json_from_db(path_file_json_data, self.gauge)
        del info_add  # Отключаем оповещение о ходе процесса импорта

        if result:
            message = f"Данные были импортированы успешно.\nПосле закрытия окна основной интерфейс будет обновлен\nс учетом добавленных данных."
            wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_INFORMATION)
            # Очищаем данные в окне
            self.gauge.SetValue(0)  # Сбрасываем прогрес бар
            self.scintilla.SetReadOnly(False)  # Снимаем ограничение с поля данных для очистки (если не снять поле не очищается!)
            self.scintilla.SetSelection(0, self.scintilla.GetTextLength())
            self.scintilla.Clear()  # Очищаем данные визуализации (загружаемые команды)
            self.choice_file.SetPath("")  # Очищаем поле от данных
            self.apply_btn.Disable()  # Делаем кнопку ИМПОРТИРОВАТЬ не активной
            # Отображаем диалоговое окно с сообщением
            # Обновляем основной интерфейс программы
            self.parent_dialog.update_main_window(self)
        else:
            # Оповещение
            message = f"Ошибка ИМПОТРА из файла JSON в БД.\nВозможно в файле ошибка!\nПроверьте данные и повторите попытку."
            wx.MessageBox(message, "Ошибка", wx.OK | wx.ICON_ERROR)

        event.Skip()
