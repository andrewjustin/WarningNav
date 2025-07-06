import tkinter as tk
from debug.menu import DebugFileMenu


class DebugLogWindow(tk.Toplevel):
    
    def __init__(self, widget):
        """
        widget: main.AlertDashboard instance
        """
        super().__init__(master=widget)
        self.withdraw()
        self.iconbitmap('warningnav.ico')  # app icon
        self.title('Debug Log')
        self.attributes('-topmost', True)  # forces debug window to stay on top
        self._add_menubar()
    
    def _add_menubar(self) -> None:
        """
        Internal method that creates a menubar.
        """
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        menubar.add_cascade(label="File", menu=DebugFileMenu(self))

    def destroy(self) -> None:
        """
        When closing the window, prevent the instance from being 'destroyed'.
        """
        self.withdraw()


class DebugLog(tk.Text):
    
    def __init__(self, widget):
        """
        widget: main.AlertDashboard instance
        """
        super().__init__(master=DebugLogWindow(widget))
        self.pack(side="top", fill="both", expand=True)
        self.tag_configure("stdout", foreground="#000000")  # black text for standard info
        self.tag_configure("stderr", foreground="#ff0000")  # red text for error info