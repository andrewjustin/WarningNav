"""
Real-time clock widget.

TODO
    * get the clock actually working
"""

from datetime import datetime
from zoneinfo import ZoneInfo
from threading import Thread
from typing import Literal
import tkinter as tk


class RealtimeClockWidget(tk.Label):
    
    def __init__(self,
                 frame: tk.Frame,
                 side: Literal['left', 'right'] = 'left',
                 fill: Literal['x', 'y'] = 'x',
                 **kwargs):
        """
        frame: tk.Frame object
            Parent frame for the clock.
        multithreading: bool (default = False)
            Run the clock on its own thread, independent of the application.
        """
        super().__init__(master=frame)
        self.timezone = ZoneInfo("America/Chicago")
        self.config(**kwargs)
        self.pack(side=side, fill=fill)
    
    def start(self, multithreading: bool = False):
        """
        Method that must be called to start the clock.
        
        multithreading: bool (default = False)
            Run the clock widget on its own thread.
        """
        if multithreading:
            thread = Thread(target=self._update_clock)
            thread.start()
        else:
            self._update_clock()

    def _update_clock(self, delay_ms=1000):
        """
        Internal method for updating the clock.

        delay_ms: int (default = 1000)
            Clock update frequency in milliseconds.
        """
        current_time = datetime.now(self.timezone).strftime("%Y/%m/%d %H:%M:%S %Z")
        self.config(text=current_time)
        self.after(delay_ms, self._update_clock)