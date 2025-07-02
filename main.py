import time
import customtkinter as ctk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import tkintermapview as tkmap
from debug.logger import DebugLogger
from nws.alerts import DEFAULT_ALERT_PROPERTIES, get_active_alerts
from menu.windows import WindowsMenu
from menu.help import HelpMenu
from zoneinfo import ZoneInfo
from datetime import datetime
from widgets.clock import RealtimeClockWidget
from threading import Thread
from widgets.debug import DebugLog, DebugLogWindow
import sys
import os


class AlertDashboard(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.geometry(f"2560x1440+0+0")  # app window size
        self.state('zoomed')  # maximized by default (doesn't seem to work????)
        self.title('WarningNav')
        self.iconbitmap('warningnav.ico')
        
        self.option_add("*Text.Font", "Helvetica 14")
        self.option_add("*Menu.Font", "Helvetica 14")
        
        ######################################### general map widget settings ##########################################
        
        # load offline tiles if available
        if os.path.isfile('offline_tiles.db'):
            self.map_widget = tkmap.TkinterMapView(self, width=2560, height=1440, corner_radius=0, max_zoom=12,
                use_database_only=True, database_path='offline_tiles.db', bg_color='transparent')
        else:
            self.map_widget = tkmap.TkinterMapView(self, width=2560, height=1440, corner_radius=0, max_zoom=1)
            
        self.map_widget.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)  # center map inside of window
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")  # default google maps tiles
        self.map_widget.fit_bounding_box((49.3457868, -124.7844079), (24.7433195, -66.9513812))  # CONUS
        self.map_widget.max_zoom = 12  # prevents zooming in too far where there are no offline tiles
        self.map_widget.min_zoom = 6  # prevents zooming out beyond CONUS coverage
        
        self.bind("<Configure>", lambda event: self.on_resize(event))  # forces the map to stay centered in the window
        self.map_widget.bind("<Configure>")  # overwrite default map behavior for window resizing
        self.map_widget.pack_propagate(False)
        
        #################################################### menubar ###################################################
        
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        menubar.add_cascade(label='Windows', menu=WindowsMenu())
        
        menubar.add_cascade(label='Help', menu=HelpMenu(self))
        self.create_debug_log(multithreading=True)
        
        # system settings
        ctk.deactivate_automatic_dpi_awareness()
        ctk.set_appearance_mode("system")
        ctk.set_widget_scaling(1)
        ctk.set_window_scaling(1)
        
        # self.display_active_alerts(multithreading=True)
        
        self.thread = Thread(target=self.display_active_alerts)
        self.thread.start()
        
        self.mainloop()
    
    def on_resize(self, event, tolerance_x=50, tolerance_y=50):
        """
        Called whenever the main window is resized or moved.
        This method keeps the map centered in the window.
        'Tolerance' argument prevent the map from updating constantly, reducing computational overhead.
        
        Parameters
        ----------
        event: dimensions of the window
        tolerance_x: int
            Maximum difference in the widths of the frame and window (pixels).
        tolerance_y: int
            Maximum difference in the heights of the frame and window (pixels).
        """
        if event.width - self.map_widget.winfo_width() > tolerance_x or \
           event.height - self.map_widget.winfo_height() > tolerance_y:
            self.map_widget.config(width=event.width, height=event.height)
            self.map_widget.pack()
    
    def create_debug_log(self, multithreading: bool = False):
        """
        Route all stdout and stderr writes to the debug logger window.
        
        multithreading: bool (default = False)
            Run the debug window on its own thread.
        """
        def _main():
            self.debug_log = DebugLog(self)
            self.debug_logger_out = DebugLogger(self.debug_log, "stdout")
            self.debug_logger_err = DebugLogger(self.debug_log, "stderr")
            sys.stdout = self.debug_logger_out
            sys.stderr = self.debug_logger_err
        
        if multithreading:
            thread = Thread(target=_main)
            thread.start()
        else:
            _main()
    
    def display_active_alerts(self):
        """
        Complete workflow for updating active alerts.
        """
        while True:
            self.get_active_alerts()
            self.destroy_polygons()
            self.draw_alert_polygons()
            time.sleep(15.)
        
    def get_active_alerts(self):
        """
        Retrieves all active NWS alerts.
        """
        sys.stdout.write('Retrieving alerts from National Weather Service')
        self.alerts = get_active_alerts()
        sys.stdout.write(f'{len(self.alerts)} alerts were found')

    def draw_alert_polygons(self):
        self.alert_polygons = []
        for alert_type in list(DEFAULT_ALERT_PROPERTIES.keys())[::-1]:
            self.alert_polygons.extend([self.map_widget.set_polygon(
                alert.geometry['coordinates'],
                fill_color=DEFAULT_ALERT_PROPERTIES[alert.alert_type][1],
                outline_color=DEFAULT_ALERT_PROPERTIES[alert.alert_type][1],
                border_width=2,
                name=alert.alert_type,
                data=alert,
                command=lambda p: self.alert_popup(p))
                for alert in self.alerts if alert.geometry is not None and alert.alert_type == alert_type])
        sys.stdout.write(f"Created {len(self.alert_polygons)} polygons")

    def destroy_polygons(self):
        """
        Remove all warning polygons.
        """
        if hasattr(self, 'alert_polygons'):
            [polygon.delete() for polygon in self.alert_polygons]
            del self.alert_polygons
        sys.stdout.write('Destroyed all polygons')

    def alert_popup(self, polygon):
        """
        Popup that appears when clicking on a warning polygon.
        """
        self.update()  # to get the height and the offset of Tk window
        dialog = tk.Toplevel(self)
        dialog.title(polygon.data.alert_type)

        # Create a scrolled Text widget (combines Text and Scrollbar)
        text_widget = ScrolledText(dialog, wrap=tk.WORD)  # Use tk.WORD for word wrapping
        text_widget.insert(tk.END, polygon.data.description)
        text_widget.config(state=tk.DISABLED)  # Make it read-only
        text_widget.pack(expand=True, fill="both")
        
        sys.stdout.write(f'Displaying alert: {polygon.data.parameters}')
        

AlertDashboard()


# showinfo(title=polygon.data.alert_type, message=polygon.data.description)


# def left_click_event(coordinates_tuple):
#     return coordinates_tuple
#
#

#

#
# self.mainloop()