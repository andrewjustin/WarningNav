import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class DebugLogWindow(tk.Toplevel):
    
    def __init__(self, widget):
        """
        widget: Parent tkinter widget.
        """
        super().__init__(widget)
        self.withdraw()
        self.title('Debug Log')
        self.attributes('-topmost', True)  # forces debug window to stay on top
    
    def add_menubar(self):
        """
        Adds an option to clear the debug log
        """
        menubar = tk.Menu(self)
        menubar.add()
        
    def show(self):
        self.deiconify()
    
    # redefine destroy method so the window will be hidden rather than destroyed
    def destroy(self):
        self.withdraw()


class DebugLog(tk.Text):
    
    def __init__(self, widget):
        """
        widget: Parent tkinter widget.
        """
        super().__init__(master=DebugLogWindow(widget))
        self.pack(side="top", fill="both", expand=True)
        self.tag_configure("stdout", foreground="#000000")  # black text for standard info
        self.tag_configure("stderr", foreground="#ff0000")  # red text for error info