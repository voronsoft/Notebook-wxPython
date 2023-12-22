import wx
import wx.xrc
from utils import database_queries


# class StatisticDialog(wx.Dialog):
#
#     def __init__(self, parent):
#         wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Статистика", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
#
#         self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
#         #
#         sizer_maim = wx.BoxSizer(wx.VERTICAL)
#         sizer_maim.SetMinSize(wx.Size(600, 600))
#         #
#         sizer_top = wx.BoxSizer(wx.VERTICAL)
#
#         self.top_txt = wx.StaticText(self, wx.ID_ANY, "Статистика:", wx.DefaultPosition, wx.DefaultSize, 0)
#         self.top_txt.Wrap(-1)
#         self.top_txt.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
#         sizer_top.Add(self.top_txt, 0, wx.ALIGN_CENTER | wx.ALL, 5)
#         sizer_maim.Add(sizer_top, 0, wx.ALL | wx.EXPAND, 5)
#         #
#         sizer_stat = wx.BoxSizer(wx.VERTICAL)
#
#         mod, cmd = self.stat_data()  #
#         print('====mod', mod)
#         print('====cmd', cmd)
#
#         for i in range(len(mod)):
#             self.static_txt = wx.StaticText(self, wx.ID_ANY, f"{mod[i]['module_name']} : {cmd[i]} (записей)", wx.DefaultPosition, wx.DefaultSize, 0)
#             self.static_txt.Wrap(-1)
#             self.static_txt.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
#             sizer_stat.Add(self.static_txt, 0, wx.ALL, 5)
#
#             self.line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
#             sizer_stat.Add(self.line, 0, wx.EXPAND | wx.ALL, 5)
#
#         #
#         sizer_maim.Add(sizer_stat, 1, wx.ALL | wx.EXPAND, 5)
#
#         self.SetSizer(sizer_maim)
#         self.Layout()
#         sizer_maim.Fit(self)
#
#         self.Centre(wx.BOTH)
#
#     def stat_data(self):
#         # Получаем модули
#         modules = database_queries.request_to_get_all_modules()
#         # Получаем количество команд для каждого модуля
#         commands_count = [database_queries.count_commands_in_module(module['module_name']) for module in modules]
#         return modules, commands_count
###########################################################################
# Class StatisticDialog
###########################################################################
class StatisticDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Статистика", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        sizer_maim = wx.BoxSizer(wx.VERTICAL)
        sizer_maim.SetMinSize(wx.Size(600, 600))

        # Сайзер TOP
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.top_txt = wx.StaticText(self, wx.ID_ANY, "Статистика:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.top_txt.Wrap(-1)
        self.top_txt.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer_top.Add(self.top_txt, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer_maim.Add(sizer_top, 0, wx.ALL | wx.EXPAND, 5)

        # Скролл
        self.scrol_wind = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.scrol_wind.SetScrollRate(5, 5)
        self.scrol_wind.SetMinSize(wx.Size(-1, 300))

        # Сайзер данных =================
        sizer_stat_data = wx.BoxSizer(wx.VERTICAL)

        mod, cmd = self.stat_data()  # Получаем данные о модулях и количестве команд

        # Формируем поля
        for i in range(len(mod)):
            self.static_txt = wx.StaticText(self.scrol_wind, wx.ID_ANY, f"'{mod[i]['module_name']}' : {cmd[i]} (записей)", wx.DefaultPosition, wx.DefaultSize, 0)
            self.static_txt.Wrap(-1)
            self.static_txt.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
            sizer_stat_data.Add(self.static_txt, 0, wx.ALL, 5)

            self.line = wx.StaticLine(self.scrol_wind, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
            sizer_stat_data.Add(self.line, 0, wx.EXPAND | wx.ALL, 5)
        # END Сайзер данных =================

        self.scrol_wind.SetSizer(sizer_stat_data)
        self.scrol_wind.Layout()
        sizer_stat_data.Fit(self.scrol_wind)
        sizer_maim.Add(self.scrol_wind, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer_maim)
        self.Layout()
        sizer_maim.Fit(self)

        self.Centre(wx.BOTH)

    # ------- Функции --------
    def stat_data(self):
        # Получаем модули
        modules = database_queries.request_to_get_all_modules()
        # Получаем количество команд для каждого модуля
        commands_count = [database_queries.count_commands_in_module(module['module_name']) for module in modules]
        return modules, commands_count


if __name__ == '__main__':
    app = wx.App(False)
    frame = StatisticDialog(None)
    frame.Show(True)
    app.MainLoop()
