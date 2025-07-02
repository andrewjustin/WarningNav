import tkinter as tk


class WindowsMenu(tk.Menu):
    
    def __init__(self):
        """
        menubar: Parent menubar.
        """
        super().__init__()
        
        self.config(tearoff=False)
        self.add_command(label="Show Warnings Window")