import os
import wx

from instance.app_config import icons_folder_path


# class BooksDialog(wx.Dialog):
#     """"""
# 
#     def __init__(self, parent):
#         wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Полезное", pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.DEFAULT_DIALOG_STYLE)
# 
#         self.parent_dialog = self.GetParent()  # Родитель окна
# 
#         # Устанавливаем иконку для окна
#         icon = wx.Icon(f'{os.path.join(icons_folder_path, "notebook.ico")}', wx.BITMAP_TYPE_ICO)
#         self.SetIcon(icon)
# 
#         self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
#         self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
# 
#         # Главный сайзер окна
#         self.sizer_main = wx.BoxSizer(wx.VERTICAL)
#         self.sizer_main.SetMinSize(wx.Size(600, 600))
# 
#         # Сайзер TOP
#         self.sizer_top = wx.BoxSizer(wx.HORIZONTAL)
# 
#         # Кнопка "Свернуть все"
#         self.collapse_button = wx.Button(self, wx.ID_ANY, "Свернуть все")
#         self.collapse_button.Bind(wx.EVT_BUTTON, self.on_collapse_all)
#         self.sizer_top.Add(self.collapse_button, 0, wx.ALL, 5)
# 
#         # Кнопка "Развернуть все"
#         self.expand_button = wx.Button(self, wx.ID_ANY, "Развернуть все")
#         self.expand_button.Bind(wx.EVT_BUTTON, self.on_expand_all)
#         self.sizer_top.Add(self.expand_button, 0, wx.ALL, 5)
# 
#         self.sizer_main.Add(self.sizer_top, 0, wx.EXPAND | wx.ALL, 5)
# 
#         # Окно дерева файлов pdf
#         self.tree_ctrl = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE | wx.TR_SINGLE)
#         self.sizer_main.Add(self.tree_ctrl, 1, wx.EXPAND | wx.ALL, 5)
# 
#         # Привязываем событие выбора файла из дерева
#         self.tree_ctrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_tree_item_activated)
# 
#         self.SetSizer(self.sizer_main)
#         self.Layout()
#         self.sizer_main.Fit(self)
#         self.Centre(wx.BOTH)
#         # ----------------------- Логика ----------------------
#         self.root = self.tree_ctrl.AddRoot("Список PDF файлов в Documents->Notebook-pdf")
#         # Путь к папке с файлами PDF для сканирования
#         # Определяем путь для сохранения файла по пути в операционной системе - C:\Users\user\Documents\Notebook-pdf
#         self.root_path_pdf_files = os.path.join(os.path.expanduser('~'), 'Documents', 'Notebook-pdf')
#         # Проверяем и создаем директорию, если она не существует
#         os.makedirs(self.root_path_pdf_files, exist_ok=True)
#         self.scan_directory(self.root_path_pdf_files, self.root)
#         self.tree_ctrl.ExpandAll()  # Разворачиваем все элементы дерева
# 
#     # ---------------- Обработчики событий ----------------
#     def on_tree_item_activated(self, event):
#         selected_item = event.GetItem()
#         if selected_item.IsOk() and not self.tree_ctrl.ItemHasChildren(selected_item):
#             # Получаем полный путь к выбранному PDF-файлу
#             pdf_path = self.get_tree_path(selected_item)
# 
#             # Открываем PDF с помощью программы по умолчанию в Windows
#             try:
#                 os.startfile(pdf_path)
#             except Exception as e:
#                 wx.MessageBox(f"Ошибка при открытии PDF: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)
# 
#     def scan_directory(self, path, parent_item):
#         # Сканирование папки и добавление элементов в дерево
#         for item in os.listdir(path):
#             item_path = os.path.join(path, item)
#             if os.path.isdir(item_path):
#                 # Добавляем папку в дерево
#                 folder_item = self.tree_ctrl.AppendItem(parent_item, item)
#                 self.scan_directory(item_path, folder_item)
#             elif item.lower().endswith(".pdf"):
#                 # Добавляем PDF-файл в дерево
#                 self.tree_ctrl.AppendItem(parent_item, item)
# 
#     def get_tree_path(self, item):
#         # Получаем полный путь к элементу дерева
#         path = []
#         while item.IsOk() and self.tree_ctrl.GetItemText(item):  # Используем GetItemText
#             path.insert(0, self.tree_ctrl.GetItemText(item))
#             item = self.tree_ctrl.GetItemParent(item)
# 
#         # Убираем "PDF Files\" из пути
#         path = path[1:]  # Игнорируем первый элемент, который является "PDF Files\"
#         return os.path.join(self.root_path_pdf_files, *path)
# 
#     def on_collapse_all(self, event):
#         """Свернуть всё"""
#         self.tree_ctrl.CollapseAll()
# 
#     def on_expand_all(self, event):
#         """Развернуть всё"""
#         self.tree_ctrl.ExpandAll()


class BooksDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Полезное", pos=wx.DefaultPosition, size=wx.Size(600, 600), style=wx.DEFAULT_DIALOG_STYLE)

        self.parent_dialog = self.GetParent()  # Родитель окна

        # Устанавливаем иконку для окна
        icon = wx.Icon(f'{os.path.join(icons_folder_path, "notebook.ico")}', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        # Главный сайзер окна
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(600, 600))

        # Сайзер TOP
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.title = wx.StaticText(self, wx.ID_ANY, "Полезное:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.title.Wrap(-1)

        self.title.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))

        sizer_top.Add(self.title, 0, wx.ALIGN_CENTER | wx.TOP | wx.RIGHT | wx.LEFT, 5)
        self.static_text = wx.StaticText(self, wx.ID_ANY, "(Вы можете добавлять PDF в Documents/Notebook-pdf/ваш_файл.pdf)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text.Wrap(-1)

        self.static_text.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        sizer_top.Add(self.static_text, 0, wx.ALIGN_CENTER | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)
        # Кнопка "Свернуть все"
        self.collapse_button = wx.Button(self, wx.ID_ANY, "Свернуть", wx.DefaultPosition, wx.DefaultSize, 0)
        self.collapse_button.SetBitmap(wx.Bitmap(os.path.join(icons_folder_path, "collapse24.png"), wx.BITMAP_TYPE_ANY))
        self.collapse_button.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_btn.Add(self.collapse_button, 0, wx.ALL, 5)
        # Кнопка "Развернуть все"
        self.expand_button = wx.Button(self, wx.ID_ANY, "Развернуть", wx.DefaultPosition, wx.DefaultSize, 0)
        self.expand_button.SetBitmap(wx.Bitmap(os.path.join(icons_folder_path, "expand24.png"), wx.BITMAP_TYPE_ANY))
        self.expand_button.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_btn.Add(self.expand_button, 0, wx.ALL, 5)

        sizer_top.Add(sizer_btn, 1, wx.ALIGN_CENTER, 5)
        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)

        self.scroll_window = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.ALWAYS_SHOW_SB | wx.HSCROLL | wx.VSCROLL)
        self.scroll_window.SetScrollRate(5, 5)

        sizer_data = wx.BoxSizer(wx.HORIZONTAL)
        sizer_data.SetMinSize(wx.Size(600, 600))
        # Окно дерева файлов pdf
        self.tree_ctrl = wx.TreeCtrl(self.scroll_window, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE | wx.TR_SINGLE)
        self.tree_ctrl.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))

        sizer_data.Add(self.tree_ctrl, 1, wx.EXPAND, 5)

        self.scroll_window.SetSizer(sizer_data)
        self.scroll_window.Layout()
        sizer_data.Fit(self.scroll_window)
        sizer_main.Add(self.scroll_window, 1, wx.EXPAND | wx.ALL, 5)

        # Привязываем событие выбора файла из дерева
        self.tree_ctrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_tree_item_activated)
        self.collapse_button.Bind(wx.EVT_BUTTON, self.on_collapse_all)
        self.expand_button.Bind(wx.EVT_BUTTON, self.on_expand_all)

        self.SetSizer(sizer_main)
        self.Layout()
        self.Centre(wx.BOTH)

        # ----------------------- Логика ----------------------
        self.root = self.tree_ctrl.AddRoot("Список PDF в Documents/Notebook-pdf")
        # Путь к папке с файлами PDF для сканирования
        # Определяем путь для сохранения файла по пути в операционной системе - C:\Users\user\Documents\Notebook-pdf
        self.root_path_pdf_files = os.path.join(os.path.expanduser('~'), 'Documents', 'Notebook-pdf')
        # Проверяем и создаем директорию, если она не существует
        os.makedirs(self.root_path_pdf_files, exist_ok=True)
        self.scan_directory(self.root_path_pdf_files, self.root)
        self.tree_ctrl.ExpandAll()  # Разворачиваем все элементы дерева

    # ---------------- Обработчики событий ----------------
    def on_tree_item_activated(self, event):
        selected_item = event.GetItem()
        if selected_item.IsOk() and not self.tree_ctrl.ItemHasChildren(selected_item):
            # Получаем полный путь к выбранному PDF-файлу
            pdf_path = self.get_tree_path(selected_item)

            # Открываем PDF с помощью программы по умолчанию в Windows
            try:
                os.startfile(pdf_path)
            except Exception as e:
                wx.MessageBox(f"Ошибка при открытии PDF: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)

    def scan_directory(self, path, parent_item):
        # Сканирование папки и добавление элементов в дерево
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                # Добавляем папку в дерево
                folder_item = self.tree_ctrl.AppendItem(parent_item, item)
                self.scan_directory(item_path, folder_item)
            elif item.lower().endswith(".pdf"):
                # Добавляем PDF-файл в дерево
                self.tree_ctrl.AppendItem(parent_item, item)

    def get_tree_path(self, item):
        # Получаем полный путь к элементу дерева
        path = []
        while item.IsOk() and self.tree_ctrl.GetItemText(item):  # Используем GetItemText
            path.insert(0, self.tree_ctrl.GetItemText(item))
            item = self.tree_ctrl.GetItemParent(item)

        # Убираем "PDF Files\" из пути
        path = path[1:]  # Игнорируем первый элемент, который является "PDF Files\"
        return os.path.join(self.root_path_pdf_files, *path)

    def on_collapse_all(self, event):
        """Свернуть всё"""
        self.tree_ctrl.CollapseAll()

    def on_expand_all(self, event):
        """Развернуть всё"""
        self.tree_ctrl.ExpandAll()
