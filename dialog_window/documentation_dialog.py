import os
import wx
import wx.xrc
import wx.html
from instance.app_config import icons_folder_path, upd_db_folder_path
from db.creat_db_and_data import create_database, added_command_data_db
from utils.database_queries import clear_database


###########################################################################
# Class DocumentationDialog
###########################################################################

class DocumentationDialog(wx.Frame):
    """Документация"""

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Документация", pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.DEFAULT_DIALOG_STYLE)

        self.parent_dialog = self.GetParent()  # Родитель окна

        self.SetSizeHints(wx.Size(600, 600), wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(600, 600))
        # Сайзер TOP
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.text_label_top = wx.StaticText(self, wx.ID_ANY, "Документация:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_label_top.Wrap(-1)
        self.text_label_top.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top.Add(self.text_label_top, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.line_a = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_top.Add(self.line_a, 0, wx.EXPAND | wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)
        # Сайзер DATA
        sizer_data = wx.BoxSizer(wx.VERTICAL)

        self.html_wind = wx.html.HtmlWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO)
        self.html_wind.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_data.Add(self.html_wind, 0, wx.ALL | wx.EXPAND, 5)

        sizer_data.Add((0, 0), 1, wx.EXPAND, 5)

        self.line_b = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_data.Add(self.line_b, 0, wx.EXPAND | wx.ALL, 5)

        sizer_main.Add(sizer_data, 1, wx.EXPAND, 5)

        # Сайзер BOTTOM
        sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)

        self.upd_db_btn = wx.Button(self, wx.ID_ANY, "Восстановить БД", wx.DefaultPosition, wx.DefaultSize, 0)
        self.upd_db_btn.SetLabelMarkup("Восстановить БД")
        self.upd_db_btn.SetBitmap(wx.Bitmap(os.path.join(icons_folder_path, "upd_db24.png"), wx.BITMAP_TYPE_ANY))
        sizer_bottom.Add(self.upd_db_btn, 0, wx.ALL, 5)

        self.cls_db_btn = wx.Button(self, wx.ID_ANY, "Очистить БД", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cls_db_btn.SetLabelMarkup("Очистить БД")
        self.cls_db_btn.SetBitmap(wx.Bitmap(os.path.join(icons_folder_path, "del_db24.png"), wx.BITMAP_TYPE_ANY))
        sizer_bottom.Add(self.cls_db_btn, 0, wx.ALL, 5)

        sizer_main.Add(sizer_bottom, 0, wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # Подключение событий
        self.upd_db_btn.Bind(wx.EVT_BUTTON, self.update_database)
        self.cls_db_btn.Bind(wx.EVT_BUTTON, self.clear_database)

    # ---------------- Обработчики событий---------------
    def update_database(self, event):
        """Обновление БД (сброс)"""
        # Очищаем БД
        clear_database()

        # Создаем БД
        create_database()

        # Добавляем модули и команды в БД
        added_command_data_db(os.path.join(upd_db_folder_path, "list_data_add_db.txt"))  # list
        added_command_data_db(os.path.join(upd_db_folder_path, "string_data_add_db.txt"))  # string
        added_command_data_db(os.path.join(upd_db_folder_path, 'dict_data_add_db.txt'))  # dict
        added_command_data_db(os.path.join(upd_db_folder_path, 'tuple_data_add_db.txt'))  # tuple
        added_command_data_db(os.path.join(upd_db_folder_path, 'set_data_add_db.txt'))  # set
        added_command_data_db(os.path.join(upd_db_folder_path, 'python_func_data_add_db.txt'))  # function python
        added_command_data_db(os.path.join(upd_db_folder_path, 'class_magic_methods_data_add_db.txt'))  # class magic methods  python

        # Обновляем главное окно
        self.parent_dialog.update_main_window(None)
        # Выводим сообщение об восстановлении БД
        # Отображаем диалоговое окно с сообщением
        msg_upd_db = (f"Интерфейс обновлен."
                      f"БД в исходном состоянии")
        wx.MessageBox(msg_upd_db, "Оповещение", wx.OK | wx.ICON_INFORMATION)

        event.Skip()

    def clear_database(self, event):
        """Очистить БД"""
        clear_database()  # Очищаем БД
        self.parent_dialog.update_main_window(None)  # Обновляем главное окно
        # Отображаем диалоговое окно с сообщением
        msg_del_db = 'БД успешно очищена, интерфейс обновлен..'
        wx.MessageBox(msg_del_db, "Оповещение", wx.OK | wx.ICON_WARNING)

        event.Skip()
