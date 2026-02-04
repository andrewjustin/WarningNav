"""
Configuration settings window.
"""
import sys
import tkinter as tk
from tkinter import ttk
import pyautogui

class SettingsWidget(tk.Tk):

    def __init__(self, dashboard):
        """
        dashboard: main.AlertDashboard instance
        """
        sys.stdout.write('Opening settings widget...')

        super().__init__(master=dashboard)

        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        width = self.winfo_width()
        height = self.winfo_height()

        self.iconbitmap('warningnav.ico')
        self.title('Settings')
        self.attributes('-topmost', True)  # forces settings widget to stay on top
        self.resizable(False, False)  # keep window the same size

        tk.Button(sidebar, text='General')

        # Main content area
        main_area = tk.Frame(self, bg='white', relief='raised', borderwidth=1)
        main_area.pack(side='right', fill='both', expand=True)

        sys.stdout.write('Settings widget successfully loaded.')