import tkinter as tk
from widgets.settings import SettingsWidget


class FileMenu(tk.Menu):
    """
    File menu on the main dashboard's menubar.
    """
    def __init__(self, dashboard):
        """
        dashboard: main.AlertDashboard instance
        """
        super().__init__(master=dashboard, tearoff=False)
        self.dashboard = dashboard
        self.add_command(label="Exit", command=lambda: self.dashboard.destroy())
        self.add_command(label="Settings", command=lambda: SettingsWidget(self.dashboard))