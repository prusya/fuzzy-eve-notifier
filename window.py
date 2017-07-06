import sys

import wx
import wx.adv
import wx.lib.scrolledpanel

from watcher import Watcher


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(
            parent=None,
            title='Fuzzy Eve Notifier',
            size=(850, 300),
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        )

        self.init_ui()
        self.Centre()
        self.Show(True)
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        self.watcher = Watcher(self)
        self.watcher.run_monitor()

    def init_ui(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("feven.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
        self.tb_icon = wx.adv.TaskBarIcon()
        self.tb_icon.SetIcon(wx.Icon(wx.Bitmap("feven.ico")),
                             'Fuzzy Eve Notifier')
        self.tb_icon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

        menubar = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu_quit = file_menu.Append(
            wx.ID_EXIT, 'Quit', 'Quit application')

        # options_menu = wx.Menu()
        # options_load_preset = options_menu.Append(
        #     1, 'Load Preset', 'Load Preset')
        # options_save_preset = options_menu.Append(
        #     2, 'Save Preset', 'Save Preset')
        # options_edit_preset = options_menu.Append(
        #     3, 'Edit Preset', 'Edit Preset')

        help_menu = wx.Menu()
        help_about = help_menu.Append(
            wx.ID_ABOUT, 'About', 'About')

        menubar.Append(file_menu, '&File')
        # menubar.Append(options_menu, '&Options')
        menubar.Append(help_menu, '&Help')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.on_quit, file_menu_quit)
        self.Bind(wx.EVT_MENU, self.on_about, help_about)
        # self.Bind(wx.EVT_MENU, self.on_load_preset, options_load_preset)
        # self.Bind(wx.EVT_MENU, self.on_save_preset, options_save_preset)
        # self.Bind(wx.EVT_MENU, self.on_edit_preset, options_edit_preset)

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        # Row based layout.
        # 3 rows with 4 columns, 5xp border horizontally and vertially.
        # caption caption caption caption
        # button  button  button  button
        # input   input   input   input
        fgs = wx.FlexGridSizer(3, 4, 5, 5)

        font12 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        # First row.
        # Create text captions for columns and assign font.
        directory_caption = wx.StaticText(panel, label="Directory")
        filename_caption = wx.StaticText(panel, label="Filename")
        message_caption = wx.StaticText(panel, label="Keyword")
        ignore_caption = wx.StaticText(panel, label="Ignore Keyword")
        directory_caption.SetFont(font12)
        filename_caption.SetFont(font12)
        message_caption.SetFont(font12)
        ignore_caption.SetFont(font12)

        # Second row.
        # First column.
        panel_row0_col0 = wx.Panel(panel)
        sizer_row0_col0 = wx.BoxSizer(wx.HORIZONTAL)

        start_btn = wx.Button(panel_row0_col0, label="Start", size=(90, 28))
        stop_btn = wx.Button(panel_row0_col0, label="Stop", size=(90, 28))
        start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        stop_btn.Bind(wx.EVT_BUTTON, self.on_stop)
        start_btn.SetFont(font12)
        stop_btn.SetFont(font12)

        sizer_row0_col0.Add(start_btn, 0, wx.ALL, 3)
        sizer_row0_col0.Add(stop_btn, 0, wx.ALL, 3)
        panel_row0_col0.SetSizer(sizer_row0_col0)

        # Second column.
        panel_row0_col1 = wx.Panel(panel)
        sizer_row0_col1 = wx.BoxSizer(wx.HORIZONTAL)

        apply_btn = wx.Button(panel_row0_col1, label="Apply Changes",
                              size=(130, 28))
        apply_btn.Bind(wx.EVT_BUTTON, self.on_apply)
        apply_btn.SetFont(font12)

        sizer_row0_col1.Add(apply_btn, 1, wx.ALL, 3)
        panel_row0_col1.SetSizer(sizer_row0_col1)

        # Third column.
        panel_row0_col2 = wx.Panel(panel)
        sizer_row0_col2 = wx.BoxSizer(wx.HORIZONTAL)

        load_btn = wx.Button(panel_row0_col2, label="Load", size=(90, 28))
        save_btn = wx.Button(panel_row0_col2, label="Save", size=(90, 28))
        load_btn.Bind(wx.EVT_BUTTON, self.on_load)
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        load_btn.SetFont(font12)
        save_btn.SetFont(font12)

        sizer_row0_col2.Add(load_btn, 1, wx.ALL, 3)
        sizer_row0_col2.Add(save_btn, 1, wx.ALL, 3)
        panel_row0_col2.SetSizer(sizer_row0_col2)

        # Fourth column.
        panel_row0_col3 = wx.Panel(panel)
        sizer_row0_col3 = wx.BoxSizer(wx.HORIZONTAL)

        # play_sound_chk = wx.CheckBox(panel_row0_col3, label='Sound',
        #                              size=(65, 28))
        # delay_spin = wx.SpinCtrl(panel_row0_col3, value="5", size=(20, 28))
        # delay_label = wx.StaticText(panel_row0_col3, label='Time',
        #                             size=(20, 28))
        # play_sound_chk.Bind(wx.EVT_CHECKBOX, self.on_sound_chk)
        # delay_spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        # play_sound_chk.SetFont(font12)
        # delay_spin.SetFont(font12)
        # delay_label.SetFont(font12)
        #
        # sizer_row0_col3.Add(play_sound_chk, 1, wx.ALL, 3)
        # sizer_row0_col3.Add(delay_spin, 1, wx.ALL, 3)
        # sizer_row0_col3.Add(delay_label, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        panel_row0_col3.SetSizer(sizer_row0_col3)

        # Third row.
        # Create text inputs and assign font.
        self.directory_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.filename_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.message_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.ignore_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.directory_text.SetFont(font12)
        self.filename_text.SetFont(font12)
        self.message_text.SetFont(font12)
        self.ignore_text.SetFont(font12)

        # Add captions, buttons, text inputs into grid.
        fgs.AddMany([
            panel_row0_col0, panel_row0_col2, panel_row0_col1, panel_row0_col3,
            directory_caption, filename_caption, message_caption,
            ignore_caption,
            (self.directory_text, 1, wx.EXPAND),
            (self.filename_text, 1, wx.EXPAND),
            (self.message_text, 1, wx.EXPAND),
            (self.ignore_text, 1, wx.EXPAND)
        ])

        # Last row and all columns are growable to fill empty space.
        fgs.AddGrowableRow(2, 1)
        # fgs.AddGrowableCol(0, 1)
        # fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableCol(2, 1)
        fgs.AddGrowableCol(3, 1)
        hbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        panel.SetSizer(hbox)

    def on_exit(self, e):
        self.tb_icon.RemoveIcon()
        self.watcher.stop_monitor()
        # For unknown reasons MainThread does not stop and process does not
        # finish. Use explicit exit.
        sys.exit(0)

    def on_quit(self, e):
        self.Close()

    def on_left_down(self, e):
        self.Show(True)
        self.SetFocus()
        self.Raise()

    def on_about(self, e):
        print('on_about')
        print(e)

    def on_load(self, e):
        print('on_load')
        print(e)

    def on_save(self, e):
        print('on_save')
        print(e)

    def on_edit_preset(self, e):
        print('on_edit_preset')
        print(e)

    def on_apply(self, e):
        paths = self.directory_text.GetValue().strip().split('\n')
        if not paths:
            return
        filenames = self.filename_text.GetValue().strip().split('\n')
        if not filenames:
            return
        keywords = self.message_text.GetValue().strip().split('\n')
        ignore = self.ignore_text.GetValue().strip().split('\n')
        self.watcher.update(paths, filenames, keywords, ignore)

    def on_start(self, e):
        print('on_start')

        print(e)

    def on_stop(self, e):
        print('on_stop')
        print(e)

    def on_sound_chk(self, e):
        print('on_sound_chk')
        print(e)

    def on_spin(self, e):
        print('on_spin')
        print(e)
