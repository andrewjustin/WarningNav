import tkinter as tk


class HelpMenu(tk.Menu):
    """
    Help menu on the main dashboard's menubar.
    """
    def __init__(self, widget):
        """
        widget: main.AlertDashboard instance
        """
        super().__init__(master=widget, tearoff=False)
        self.widget = widget
        self.add_command(label="Show Debug Log", command=lambda: self.widget.debug_log.master.deiconify())