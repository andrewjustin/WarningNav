import tkinter as tk


class WindowsMenu(tk.Menu):
    """
    Menu that gives options for showing different windows.
    """
    def __init__(self, dashboard):
        """
        dashboard: main.AlertDashboard instance
        """
        super().__init__(master=dashboard, tearoff=False)
        self.add_command(label="Show Warnings Window")