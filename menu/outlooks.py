import tkinter as tk
from noaa.spc.outlooks import destroy_all_outlook_polygons
from widgets.outlooks import ConvectiveOutlookWidget, ExcessivePrecipitationOutlookWidget, FireOutlookWidget


class OutlooksMenu(tk.Menu):
    """
    Outlook menu on the main dashboard's menubar.
    """
    def __init__(self, dashboard):
        """
        dashboard: main.AlertDashboard instance
        """
        super().__init__(master=dashboard, tearoff=False)
        self.dashboard = dashboard
        self.add_command(label="Convective Outlook",
                         command=lambda: ConvectiveOutlookWidget(self.dashboard))
        self.add_command(label="Fire Weather Outlook",
                         command=lambda: FireOutlookWidget(self.dashboard))
        self.add_command(label="Excessive Precipitation Outlook",
                         command=lambda: ExcessivePrecipitationOutlookWidget(self.dashboard))
        self.add_separator()
        self.add_command(label="Clear Outlook Polygons",
                         command=lambda: destroy_all_outlook_polygons(self.dashboard))