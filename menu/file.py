import tkinter as tk


class FileMenu(tk.Menu):
    """
    File menu on the main dashboard's menubar.
    """
    def __init__(self, widget):
        """
        widget: main.AlertDashboard instance
        """
        super().__init__(master=widget, tearoff=False)
        self.widget = widget
        self.add_command(label="Exit", command=lambda: self.widget.destroy())