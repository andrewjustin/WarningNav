import tkinter as tk


class HelpMenu(tk.Menu):
    
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.config(tearoff=False)
        self.add_command(label="Show Debug Log", command=lambda: self._show_debug_log())
    
    def _show_debug_log(self):
        """
        Displays a debug log.
        """
        self.root.debug_log.master.show()