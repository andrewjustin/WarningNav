import tkinter as tk
from datetime import datetime


class DebugLogger(object):
    """
    Custom object that sends debug information to a DebugLog instance.
    """
    def __init__(self, widget, tag: str):
        self.widget = widget
        self.tag = tag

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, f'{self.get_current_timestring()}: {string}\n', (self.tag,))
        self.widget.configure(state="disabled")
    
    @staticmethod
    def get_current_timestring():
        return str(datetime.utcnow())