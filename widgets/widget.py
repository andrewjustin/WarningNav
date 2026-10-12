import tkinter as tk


class Widget(tk.Toplevel):

    def __init__(self, dashboard) -> None:
        super().__init__(master=dashboard)
        self.destroy()  # the widget will want to open immediately
        self.iconbitmap("warningnav.ico")  # set WarningNav logo

    def show(self):
        """
        Open the widget.
        """
        self.deiconify()

    def destroy(self):
        """
        Close the widget.
        """
        self.withdraw()