import tkinter as tk
from datetime import datetime


class DebugLogger(object):
    """
    Custom object that sends debug information to a DebugLog instance.
    """
    def __init__(self, debug_log, tag: str):
        """
        debug_log: widgets.debug.DebugLog instance
        tag: text identifier
        """
        self.debug_log = debug_log
        self.tag = tag

    def write(self, string: str) -> None:
        self.debug_log.configure(state="normal")  # allow DebugLog object to be edited
        self.debug_log.insert(tk.END, f'{self._get_current_timestring()}: {string}\n', (self.tag,))  # insert log message
        self.debug_log.see(tk.END)  # force the target DebugLog object to scroll to the end when new text is added
        self.debug_log.configure(state="disabled")  # make DebugLog object read-only

    @staticmethod
    def _get_current_timestring() -> str:
        return str(datetime.utcnow())