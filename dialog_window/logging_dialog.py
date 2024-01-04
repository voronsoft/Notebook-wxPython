import os
import wx
import wx.xrc
import wx.richtext
from utils.logs_files import logs_files
from logs.app_logger import logger_debug
from instance.app_config import icons_folder_path, path_to_log


###########################################################################
# Class LoggingDialog
###########################################################################
class LoggingDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Logging (логи)", pos=wx.DefaultPosition, size=wx.Size(600, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.parent_dialog = self.GetParent()  # Родитель окна

        # Устанавливаем иконку для окна
        icon = wx.Icon(f'{os.path.join(icons_folder_path, "notebook.ico")}', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # Главный сайзер MAIN
        sizer_main_log = wx.BoxSizer(wx.VERTICAL)
        # Сайзер TOP
        sizer_top = wx.BoxSizer(wx.HORIZONTAL)
        # Поле выбора файла лога
        choice_logChoices = logs_files()  # Список файлов логирования
        self.choice_log = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_logChoices, 0)
        self.choice_log.SetSelection(-1)
        self.choice_log.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top.Add(self.choice_log, 1, wx.ALL, 5)
        # Кнопка очистки файла лога
        self.clear_btn_choice_log = wx.Button(self, wx.ID_ANY, "Очистить файл логов", wx.DefaultPosition, wx.DefaultSize, 0)
        self.clear_btn_choice_log.SetLabelMarkup("Очистить раздел логов")
        self.clear_btn_choice_log.SetBitmap(wx.Bitmap(os.path.join(icons_folder_path, "del16.png"), wx.BITMAP_TYPE_ANY))
        self.clear_btn_choice_log.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top.Add(self.clear_btn_choice_log, 1, wx.ALL, 5)

        sizer_main_log.Add(sizer_top, 0, wx.EXPAND, 5)

        # Сайзер DATA
        sizer_data_log = wx.BoxSizer(wx.VERTICAL)
        # Поле Данных из выбранного лог файла
        self.data_rich_text = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_SIMPLE | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        self.data_rich_text.SetEditable(False)  # Делаем текст только для чтения
        self.data_rich_text.SetMinSize(wx.Size(600, 400))
        sizer_data_log.Add(self.data_rich_text, 1, wx.EXPAND | wx.ALL, 5)

        sizer_main_log.Add(sizer_data_log, 1, wx.EXPAND, 5)

        self.SetSizer(sizer_main_log)
        self.Layout()

        self.Centre(wx.BOTH)

        # Привязываем событие к кнопке удаления данных в файле
        self.clear_btn_choice_log.Bind(wx.EVT_BUTTON, self.clear_log)
        # Привязываем событие к выбору модуля
        self.choice_log.Bind(wx.EVT_CHOICE, self.on_file_select)

    # -------------------------- Обработчики ------------------------------
    def on_file_select(self, event):
        """Обработчик события выбора файла лога"""
        # Получаем название выбранного файла
        selected_file_name = self.choice_log.GetStringSelection()  # Получаем имя выбранного файла логов

        # Составляем полный путь к выбранному файлу
        selected_file_path = os.path.join(path_to_log, selected_file_name)

        try:
            # Открываем файл для чтения
            with open(selected_file_path, 'r', encoding='utf-8') as file:
                # Читаем данные из файла в переменную data
                data_log = file.read()
                # Очищаем текущий контент RichTextCtrl
                self.data_rich_text.Clear()
                # Добавляем данные в RichTextCtrl
                self.data_rich_text.WriteText(data_log)
                logger_debug.debug(f'Данные из {selected_file_name} файла прочитаны')

        except Exception as e:
            logger_debug.exception(f'Ошибка при чтении файла {selected_file_name}:\n', str(e))

    def clear_log(self, event):
        """Очистка файла логов"""
        # Отображаем сообщение
        message = f"Данные в файле будут очищены !"
        wx.MessageBox(message, "Оповещение", wx.OK | wx.ICON_WARNING)

        # Получаем название выбранного файла
        selected_file_name = self.choice_log.GetStringSelection()  # Получаем имя выбранного файла логов
        # Составляем полный путь к выбранному файлу
        selected_file_path = os.path.join(path_to_log, selected_file_name)

        try:
            # Открываем файл для записи
            with open(selected_file_path, 'w') as file:
                # Очищаем текущий контент RichTextCtrl
                self.data_rich_text.Clear()
                # Очищаем поле с данными в окне

            logger_debug.debug(f'Данные из {selected_file_name} файла ОЧИЩЕНЫ')
        except Exception as e:
            logger_debug.exception(f"Ошибка при очистке файла {selected_file_name}:\n", str(e))
