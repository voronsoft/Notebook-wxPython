import os
import wx
import wx.xrc
import wx.html
import wx.richtext
from instance.app_config import icons_folder_path, img_folder_path


###########################################################################
# Class DocumentationDialog
###########################################################################

class DocumentationDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Документация", pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER)

        self.parent_dialog = self.GetParent()  # Родитель окна
        # Устанавливаем иконку для окна
        icon = wx.Icon(f'{os.path.join(icons_folder_path, "notebook.ico")}', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.SetSizeHints(wx.Size(-1, -1), wx.DefaultSize)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(650, 600))
        sizer_data = wx.BoxSizer(wx.VERTICAL)

        self.m_scrolledWindow1 = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), wx.HSCROLL | wx.VSCROLL)
        self.m_scrolledWindow1.SetScrollRate(15, 15)
        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_bitmap0 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(icons_folder_path, "notebook.ico"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap0, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticText2 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "Добро пожаловать в программу - \"Блокнот программ\".\nДля чего она служит ?\nСоздана она по типу блокнот с заметками.\nВид интерфейса:\n", wx.DefaultPosition,
                                           wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText2.SetLabelMarkup("Добро пожаловать в программу - \"Блокнот программ\".\nДля чего она служит ?\nСоздана она по типу блокнот с заметками.\nВид интерфейса:\n")
        self.m_staticText2.Wrap(-1)

        self.m_staticText2.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap1 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "2.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticline2 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline2, 0, wx.ALL | wx.EXPAND, 20)

        self.m_staticText21 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "Как видите есть центральная часть окна, в которой вы видите вкладки и записи.\n", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText21.Wrap(-1)

        self.m_staticText21.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText21, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap2 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "3.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticline3 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline3, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText6 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "Запись(и)в вкладке", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)

        self.m_staticText6.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText6, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap3 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "4.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap3, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticline4 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline4, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText7 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "Теперь взглянем на основную панель управления.\nДумаю по описанию вам вполне понятно для каких\nцелей предназначены кнопки управления", wx.DefaultPosition,
                                           wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText7.Wrap(-1)

        self.m_staticText7.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText7, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap4 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "5.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap4, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticline5 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline5, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText8 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "- ДОБАВИТЬ - \nДобавит запись к существующей вкладке.\nИли добавит новую вкладку.", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText8.Wrap(-1)

        self.m_staticText8.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText8, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_bitmap5 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "6.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.m_bitmap5, 0, wx.ALL, 5)

        self.m_bitmap6 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "6-1.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.m_bitmap6, 0, wx.ALL, 5)

        bSizer4.Add(bSizer5, 0, wx.ALIGN_CENTER, 5)

        self.m_staticline6 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline6, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText81 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "- ИЗМЕНИТЬ -\nИзменит название и описание для:\nвкладки или конкретной записи.", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText81.Wrap(-1)

        self.m_staticText81.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText81, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_bitmap7 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "7.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.m_bitmap7, 0, wx.ALL, 5)

        self.m_bitmap8 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "7-1.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.m_bitmap8, 0, wx.ALL, 5)

        bSizer4.Add(bSizer6, 0, wx.ALIGN_CENTER, 5)

        self.m_staticline7 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline7, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText811 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "- УДАЛИТЬ -\nУдалит вкладку с всеми записями для вкладки.\nУдалит отдельно выбранную команду", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText811.Wrap(-1)

        self.m_staticText811.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText811, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_bitmap9 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "8.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer7.Add(self.m_bitmap9, 0, wx.ALL, 5)

        self.m_bitmap10 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "8-1.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer7.Add(self.m_bitmap10, 0, wx.ALL, 5)

        bSizer4.Add(bSizer7, 0, wx.ALIGN_CENTER, 5)

        self.m_staticline8 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline8, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText812 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "- ПОИСК -\nПоиск по точному совпадению названия вкладки.\n(поиск реализован просто как пример)", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText812.Wrap(-1)

        self.m_staticText812.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText812, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_bitmap11 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "9.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_bitmap11, 0, wx.ALL, 5)

        bSizer4.Add(bSizer8, 0, wx.ALIGN_CENTER, 5)

        self.m_staticline10 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline10, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText18 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "Взглянем на меню бар:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText18.Wrap(-1)

        self.m_staticText18.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText18, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap13 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "10.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap13, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticline11 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline11, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText19 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "-ФАЙЛ-\nЗагрузить БД Python - Будет загружена дефолтная база данных.\nОчистить БД - База данных будет полностью стерта !!\nВыход - Программа будет закрыта.",
                                            wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText19.Wrap(-1)

        self.m_staticText19.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText19, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap14 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "10-1.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap14, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticline12 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline12, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText192 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "-СТАТИСТИКА-\nСодержит данные о вкладке и количестве записей в ней.", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText192.Wrap(-1)

        self.m_staticText192.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText192, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap15 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "10-2.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap15, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap16 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "10-2-1.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap16, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticline13 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline13, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText1921 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "HELP\nНемного остановимся на пункте ЛОГИ программы.", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText1921.Wrap(-1)

        self.m_staticText1921.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText1921, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap17 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "10-3.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap17, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticText28 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY,
                                            "В окне логи программы содержатся данные о работе программы.\nНеобходимо для разработчиков.\nМожно увидеть три типа логов(оповещений)\n- Информация\n- Предупреждения\n- Ошибки\n\nТак же можно очистить данные от логов.",
                                            wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText28.Wrap(-1)

        self.m_staticText28.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText28, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap18 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "10-3-3.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap18, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticline14 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline14, 0, wx.EXPAND | wx.ALL, 20)

        self.m_staticText29 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "Импорт-Экспорт\n- Импортировать можно только файлы в формате JSON\nНазвание полей важно учитывать для понимания структуры.", wx.DefaultPosition, wx.DefaultSize,
                                            wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText29.Wrap(-1)

        self.m_staticText29.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText29, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap19 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "10-4.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap19, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticText32 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "ВАЖНО !!!", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText32.Wrap(-1)

        self.m_staticText32.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText32, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticText31 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY,
                                            "Название ключей не менять. \n\"module_name\" - это поле является по факту Вкладкой, которая будет создана.\n\"command_name\" - это поле название записи.\n\"command_description\" - описание записи.\n\"command_example\" - дополнительное поле.\n\n[\n    {\n        \"module_name\": \"Вкладка1 (название будущей или существующей вкладки)\",\n        \"command_name\": \"Название записи\",\n        \"command_description\": \"Описание записи \",\n        \"command_example\": \"Будет добавлена в вкладку Вкладка1.\"\n    },\n     {\n        \"module_name\": \"Вкладка2\",\n        \"command_name\": \"Название записи 2\",\n        \"command_description\": \"Описание записи 2\",\n        \"command_example\": \"Будет добавлена в вкладку Вкладка2\"\n    }\n]",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText31.Wrap(-1)

        self.m_staticText31.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText31, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap21 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "13.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap21, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticText33 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY,
                                            "То есть вы создаете файл JSON для импорта данных в программу.\nВыбираете файл.\nВ центральной части вы увидите как выглядят ваши импортируемые данные.\nВизуализация для проверки.\nДалее вы можете приступить к импорту данных.\nЕсли в файле JSON будет ошибка в структуре,\nбудет выведенно предупреждение.\n\nPS.\nЕсли вы запутались и не знаете как создать файл для импорта,\nМожно сначала загрузить тестовую БД из системного меню.\nФайл-> Загрузить БД python\nА далее экспортировать данные в файл.\nImport/Export -> Export\nФайл будет сохранет в папке - Документы",
                                            wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText33.Wrap(-1)

        self.m_staticText33.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText33, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticline15 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline15, 0, wx.ALL | wx.EXPAND, 20)

        self.m_staticText30 = wx.StaticText(self.m_scrolledWindow1, wx.ID_ANY, "Экспорт", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText30.Wrap(-1)

        self.m_staticText30.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        bSizer4.Add(self.m_staticText30, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_bitmap23 = wx.StaticBitmap(self.m_scrolledWindow1, wx.ID_ANY, wx.Bitmap(os.path.join(img_folder_path, "14.png"), wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_bitmap23, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticline18 = wx.StaticLine(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer4.Add(self.m_staticline18, 0, wx.EXPAND | wx.ALL, 20)

        self.m_scrolledWindow1.SetSizer(bSizer4)
        self.m_scrolledWindow1.Layout()
        bSizer4.Fit(self.m_scrolledWindow1)
        sizer_data.Add(self.m_scrolledWindow1, 1, wx.EXPAND | wx.ALL, 5)

        sizer_main.Add(sizer_data, 1, wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)
