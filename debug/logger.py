import tkinter as tk
from datetime import datetime


class DebugLogger(object):
    """
    Custom object that sends debug information to a DebugLog instance.
    """
    def __init__(self, widget, tag: str):
        """
        widget: widgets.debug.DebugLog instance
        """
        self.widget = widget
        self.tag = tag

    def write(self, string: str) -> None:
        self.widget.configure(state="normal")  # allow DebugLog object to be edited
        self.widget.insert(tk.END, f'{self.get_current_timestring()}: {string}\n', (self.tag,))  # insert log message
        self.widget.see(tk.END)  # force the target DebugLog object to scroll to the end when new text is added
        self.widget.configure(state="disabled")  # make DebugLog object read-only
    
    @staticmethod
    def get_current_timestring() -> str:
        return str(datetime.utcnow())