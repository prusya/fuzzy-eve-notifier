import wx
import wx.html2


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(
            parent=None,
            title='Fuzzy Eve Notifier',
            size=(800, 300),
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        )

        self.init_ui()
        self.Centre()
        self.Show(True)

    def init_ui(self):
        menubar = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu_quit = file_menu.Append(
            wx.ID_EXIT, 'Quit', 'Quit application')

        options_menu = wx.Menu()
        options_load_preset = options_menu.Append(
            1, 'Load Preset', 'Load Preset')
        options_save_preset = options_menu.Append(
            2, 'Save Preset', 'Save Preset')
        options_edit_preset = options_menu.Append(
            3, 'Edit Preset', 'Edit Preset')

        help_menu = wx.Menu()
        help_about = help_menu.Append(
            wx.ID_ABOUT, 'About', 'About')

        menubar.Append(file_menu, '&File')
        menubar.Append(options_menu, '&Options')
        menubar.Append(help_menu, '&Help')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.on_quit, file_menu_quit)
        self.Bind(wx.EVT_MENU, self.on_about, help_about)
        self.Bind(wx.EVT_MENU, self.on_load_preset, options_load_preset)
        self.Bind(wx.EVT_MENU, self.on_save_preset, options_save_preset)
        self.Bind(wx.EVT_MENU, self.on_edit_preset, options_edit_preset)

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        # 3 rows with 4 columns, 5xp border horizontally and vertially.
        # caption caption caption caption
        # button  button  button  button
        # input   input   input   input
        fgs = wx.FlexGridSizer(3, 4, 5, 5)

        font12 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        # Create text captions for columns and assign font.
        directory_caption = wx.StaticText(panel, label="Directory")
        filename_caption = wx.StaticText(panel, label="Filename")
        message_caption = wx.StaticText(panel, label="Keyword")
        ignore_caption = wx.StaticText(panel, label="Ignore Keyword")
        directory_caption.SetFont(font12)
        filename_caption.SetFont(font12)
        message_caption.SetFont(font12)
        ignore_caption.SetFont(font12)

        # Create apply buttons for columns and assign event handler and font.
        directory_apply = wx.Button(panel, label="Apply", size=(90, 28))
        filename_apply = wx.Button(panel, label="Apply", size=(90, 28))
        message_apply = wx.Button(panel, label="Apply", size=(90, 28))
        ignore_apply = wx.Button(panel, label="Apply", size=(90, 28))
        directory_apply.Bind(wx.EVT_BUTTON, self.on_directory_apply)
        filename_apply.Bind(wx.EVT_BUTTON, self.on_filename_apply)
        message_apply.Bind(wx.EVT_BUTTON, self.on_message_apply)
        ignore_apply.Bind(wx.EVT_BUTTON, self.on_ignore_apply)
        directory_apply.SetFont(font12)
        filename_apply.SetFont(font12)
        message_apply.SetFont(font12)
        ignore_apply.SetFont(font12)

        # Create text inputs and assign font.
        directory_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        filename_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        message_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        ignore_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        directory_text.SetFont(font12)
        filename_text.SetFont(font12)
        message_text.SetFont(font12)
        ignore_text.SetFont(font12)

        # Add captions, buttons, text inputs into grid.
        fgs.AddMany([
            directory_caption, filename_caption, message_caption,
            ignore_caption,
            directory_apply, filename_apply, message_apply, ignore_apply,
            (directory_text, 1, wx.EXPAND),
            (filename_text, 1, wx.EXPAND),
            (message_text, 1, wx.EXPAND),
            (ignore_text, 1, wx.EXPAND),
        ])

        # Last row and all columns are growable to fill empty space.
        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(0, 1)
        fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableCol(2, 1)
        fgs.AddGrowableCol(3, 1)
        hbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        panel.SetSizer(hbox)

    def on_quit(self, e):
        self.Close()

    def on_about(self, e):
        print('on_about')
        print(e)

    def on_load_preset(self, e):
        print('on_load_preset')
        print(e)

    def on_save_preset(self, e):
        print('on_save_preset')
        print(e)

    def on_edit_preset(self, e):
        print('on_edit_preset')
        print(e)

    def on_directory_apply(self, e):
        print('on_directory_apply')
        print(e)

    def on_filename_apply(self, e):
        print('on_filename_apply')
        print(e)

    def on_message_apply(self, e):
        print('on_message_apply')
        print(e)

    def on_ignore_apply(self, e):
        print('on_ignore_apply')
        print(e)
