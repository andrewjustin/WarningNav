import tkinter as tk


class WindowsMenu(tk.Menu):
    """
    Menu that gives options for showing different windows.
    """
    def __init__(self, widget):
        """
        widget: main.AlertDashboard instance
        """
        super().__init__(master=widget, tearoff=False)
        self.add_command(label="Show Warnings Window")