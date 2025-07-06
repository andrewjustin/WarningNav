import time
import customtkinter as ctk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import tkintermapview as tkmap
from debug.logger import DebugLogger
from nws.alerts import DEFAULT_ALERT_PROPERTIES, Alerts
from menu.file import FileMenu
from menu.windows import WindowsMenu
from menu.help import HelpMenu
from threading import Thread
from widgets.debug import DebugLog
import sys
import os


class AlertDashboard(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.geometry('2560x1440+0+0')  # app window size
        self.state('zoomed')  # maximized by default (doesn't seem to work????)
        self.title('WarningNav')
        self.iconbitmap('warningnav.ico')
        
        self.option_add('*Text.Font', 'Helvetica 14')
        self.option_add('*Menu.Font', 'Helvetica 14')
        
        ######################################### general map widget settings ##########################################
        
        # load offline tiles if available
        if os.path.isfile('offline_tiles.db'):
            self.map_widget = tkmap.TkinterMapView(self, width=2560, height=1440, corner_radius=0, max_zoom=12,
                                                   use_database_only=True, database_path='offline_tiles.db', bg_color='transparent')
        else:
            self.map_widget = tkmap.TkinterMapView(self, width=2560, height=1440, corner_radius=0, max_zoom=1)
            
        self.map_widget.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)  # center map inside of window
        self.map_widget.set_tile_server('https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga')  # default google maps tiles
        self.map_widget.fit_bounding_box((49.3457868, -124.7844079), (24.7433195, -66.9513812))  # CONUS
        self.map_widget.max_zoom = 12  # prevents zooming in too far where there are no offline tiles
        self.map_widget.min_zoom = 6  # prevents zooming out beyond CONUS coverage
        
        self.bind('<Configure>', lambda event: self.on_resize(event))  # forces the map to stay centered in the window
        self.map_widget.bind('<Configure>')  # overwrite default map behavior for window resizing
        self.map_widget.pack_propagate(False)
        
        #################################################### menubar ###################################################
        
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        menubar.add_cascade(label='File', menu=FileMenu(self))
        menubar.add_cascade(label='Windows', menu=WindowsMenu(self))
        menubar.add_cascade(label='Help', menu=HelpMenu(self))
        self.create_debug_log(multithreading=True)
        
        # system settings
        ctk.deactivate_automatic_dpi_awareness()
        ctk.set_appearance_mode('system')
        ctk.set_widget_scaling(1)
        ctk.set_window_scaling(1)
        
        self.alerts = Alerts()
        self.thread = Thread(target=self._display_active_alerts)
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
            self.debug_logger_out = DebugLogger(self.debug_log, 'stdout')
            self.debug_logger_err = DebugLogger(self.debug_log, 'stderr')
            sys.stdout = self.debug_logger_out
            sys.stderr = self.debug_logger_err
        
        if multithreading:
            thread = Thread(target=_main)
            thread.start()
        else:
            _main()
    
    def _display_active_alerts(self, update_freq: int = 60):
        """
        Complete workflow for updating active alerts.
        
        update_freq: update frequency in seconds.
        """
        while True:
            time.sleep(1.0)  # allows warning retrieval information to buffer to debug log
            self.alerts.update_alerts()
            self._draw_new_alert_polygons()
            self._remove_old_alert_polygons()
            sys.stdout.write(f'Active alert polygons: {len(self._canvas_polygon_list())}')
            time.sleep(update_freq - 1.0)

    def _draw_new_alert_polygons(self):
        sys.stdout.write('Searching for new alerts to draw as polygons')
        new_alert_polygons = []
        for alert_type in list(DEFAULT_ALERT_PROPERTIES.keys())[::-1]:
            new_alert_polygons.extend([dict(
                position_list=alert.geometry['coordinates'],
                fill_color=DEFAULT_ALERT_PROPERTIES[alert.alert_type][1],
                outline_color=DEFAULT_ALERT_PROPERTIES[alert.alert_type][1],
                border_width=2,
                name=alert.alert_type,
                data=alert)
                for alert in self.alerts.alerts_with_geometry
                if alert.alert_type == alert_type
                and alert.alert_id in self.alerts.new_alert_ids])
        
        for polygon in new_alert_polygons:
            self.map_widget.set_polygon(command=lambda p: self._alert_popup(p), **polygon)
        sys.stdout.write(f'Created {len(new_alert_polygons)} new polygons')

    def _remove_old_alert_polygons(self):
        sys.stdout.write('Searching for expired alert polygons')
        polygons = self._canvas_polygon_list()
        polygons_to_remove = [p for p in polygons if p.data.alert_id in self.alerts.old_alert_ids]
        for polygon in polygons_to_remove:
            polygon.delete()
        sys.stdout.write(f'Removed {len(polygons_to_remove)} alert polygons')
    
    def _canvas_polygon_list(self):
        """
        Returns a list of all polygons currently shown on the map.
        """
        return self.map_widget.canvas_polygon_list

    def _alert_popup(self, polygon):
        """
        Popup that appears when clicking on an alert polygon.
        """
        self.update()  # to get the height and the offset of Tk window
        dialog = tk.Toplevel(self)
        dialog.iconbitmap('warningnav.ico')
        dialog.title(polygon.data.alert_type)

        text_widget = ScrolledText(dialog, wrap=tk.WORD)
        text_widget.insert(tk.END, polygon.data.description)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill="both")
        
        sys.stdout.write(f'Displaying alert: {polygon.data.parameters}')


AlertDashboard()