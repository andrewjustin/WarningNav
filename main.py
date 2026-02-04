"""
TODO
    * HIGH priority
        - allow selection of polygons that are on top of each other
        - creating warning list widget
        - allow toggling of offline tiles
        - fix warning popup text (some text is missing and level of detail is not consistent between warnings)
        - allow customizable warning polygon colors
    * MEDIUM priority
        - customizable warning view options (e.g., only show tornado warnings)
        - SPC convective/fire outlooks
            - change popup appearance
        - SPC reports and mesoscale discussions
        - WPC precipitation outlooks
        - only allow a maximum of one warning popup per polygon
        - add user option for warning update frequency
    * LOW priority
        - create config files for app settings and user-defined markers
        - figure out realtime clock placement
"""
from debug.logger import DebugLogger
from menu.file import FileMenu
from menu.gis import GISMenu
from menu.windows import WindowsMenu
from menu.help import HelpMenu
from noaa.nws.alerts import DEFAULT_ALERT_PROPERTIES, NWSAlerts
from threading import Thread
from tkinter.scrolledtext import ScrolledText
from tkvideo import tkvideo
from widgets.debug import DebugLog
import customtkinter as ctk
import os
import pyautogui
import random
import sys
import time
import tkinter as tk
import tkintermapview as tkmap


class AlertDashboard(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.geometry(f'{screen_width}x{screen_height}+0+0')  # app window size
        # self.update_idletasks()
        self.title('WarningNav')
        self.iconbitmap('warningnav.ico')

        self.option_add('*Text.Font', 'Helvetica 11')
        self.option_add('*Menu.Font', 'Helvetica 11')
        
        self.bind('<B1-Motion>', self._map_motion)

        self.debug_log = DebugLog(self)  # initialize the debug log

        ### reroute all stdout and stderr printouts to the debug log ###
        self.debug_logger_out = DebugLogger(self.debug_log, 'stdout')
        self.debug_logger_err = DebugLogger(self.debug_log, 'stderr')
        sys.stdout = self.debug_logger_out
        sys.stderr = self.debug_logger_err

        ######################################### general map widget settings ##########################################

        # load offline tiles if available
        if os.path.isfile('offline_tiles.db'):
            self.map_widget = tkmap.TkinterMapView(self,
                                                   width=screen_width,
                                                   height=screen_height,
                                                   corner_radius=0,
                                                   max_zoom=12,
                                                   use_database_only=True,
                                                   database_path='offline_tiles.db',
                                                   bg_color='transparent')
        else:
            self.map_widget = tkmap.TkinterMapView(self,
                                                   width=screen_width,
                                                   height=screen_height,
                                                   corner_radius=0)

        self.map_widget.place(relx=0.5, rely=0.5, anchor='center', bordermode='inside')  # center map inside of window
        self.map_widget.set_tile_server('https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga')  # default google maps tiles
        self.map_widget.fit_bounding_box((49.3457868, -124.7844079),
                                         (24.7433195, -66.9513812))  # CONUS
        self.map_widget.max_zoom = 12  # prevents zooming in too far where there are no offline tiles
        self.map_widget.min_zoom = 6  # prevents zooming out beyond CONUS coverage
        self._define_map_bounds()
        
        self.bind('<Configure>', lambda event: self.on_resize(event))  # forces the map to stay centered in the window
        self.map_widget.bind('<Configure>')  # overwrite default map behavior for window resizing
        self.map_widget.pack_propagate(False)

        #################################################### menubar ###################################################
        
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        menubar.add_cascade(label='File', menu=FileMenu(self))
        menubar.add_cascade(label='GIS', menu=GISMenu(self))
        menubar.add_cascade(label='Windows', menu=WindowsMenu(self))
        menubar.add_cascade(label='Help', menu=HelpMenu(self))
        
        ################################################################################################################
        
        # system settings
        ctk.deactivate_automatic_dpi_awareness()
        ctk.set_appearance_mode('system')
        ctk.set_widget_scaling(1)
        ctk.set_window_scaling(1)
        
        # NWS alerts
        self.alerts = NWSAlerts()

        ### enable automatic alert updates and run the updates on a separate thread ###
        automatic_alerts_thread = Thread(target=self._run_automatic_alert_updates,
                                         name='auto-alerts-thread',
                                         daemon=True)
        automatic_alerts_thread.start()

        self.mainloop()
    
    def _define_map_bounds(self):
        """
        Internal method that defines the bounds of the map based on the current zoom.
        """
        
        # {zoom: [left (x), top (y), right (x), bottom (y)]
        self.center_positions = {6: [-101.25, 41.688, -84.371, 31.355],
                                 7: [-112.504, 45.42, -75.937, 28.666],
                                 8: [-118.129, 47.377, -71.714, 26.617],
                                 9: [-121.641, 48.157, -69.608, 25.575],
                                 10: [-123.047, 48.774, -68.200, 25.052],
                                 11: [-123.926, 49.079, -67.5, 24.95],
                                 12: [-124.365, 49.231, -67.235, 24.818]}
    
    def on_resize(self,
                  event: tk.Event,
                  tolerance_x: int = 50,
                  tolerance_y: int = 50
                  ) -> None:
        """
        Called whenever the main window is resized or moved.
        This method keeps the map centered in the window.
        'Tolerance' arguments prevent the map from updating constantly, reducing computational overhead.
        
        Parameters
        ----------
        event: tk.Event
            Dimensions of the window.
        tolerance_x: int
            Maximum difference in the widths of the frame and window (pixels).
        tolerance_y: int
            Maximum difference in the heights of the frame and window (pixels).
        """
        if self.map_widget.zoom < self.map_widget.min_zoom:
            self.map_widget.set_zoom(self.map_widget.min_zoom)
            self.map_widget.update()
        
        window_width = event.width
        window_height = event.height
        map_width = self.map_widget.winfo_width()
        map_height = self.map_widget.winfo_height()
        sys.stdout.write(f'Window size: {window_width}x{window_height}')

        if abs(window_width - map_width) > tolerance_x or abs(window_height - map_height) > tolerance_y:
            sys.stdout.write('Resizing map')
            self.map_widget.config(width=event.width, height=event.height)
            self.map_widget.pack(anchor='nw')

    def draw_alert_polygon(self,
                           coordinates: list,
                           fill_color: str,
                           border_color: str,
                           border_width: int,
                           name: str,
                           data = None):
        """
        Draw a single alert polygon.
        
        coordinates: list
            List of (lat, lon) coordinate pairs marking the polygon vertices.
        fill_color: str
            Color of the polygon fill (HEX code).
        border_color: str
            Color of the polygon border/outline (HEX code).
        border_width: int
            Width of the polygon border.
        name: str
            Name of the polygon alert type.
        data: Any
            Optional data to include with the polygon.
        """
        polygon = tkmap.map_widget.CanvasPolygon(map_widget=self.map_widget,
                                                 position_list=coordinates,
                                                 command=lambda p: self.alert_popup(p),
                                                 fill_color=fill_color,
                                                 outline_color=border_color,
                                                 border_width=border_width,
                                                 name=name,
                                                 data=data)

        polygon.draw()

        self.map_widget.canvas_polygon_list.append(polygon)

    def destroy_all_outlook_polygons(self):
        """
        dashboard: main.AlertDashboard instance
        """
        outlook_polygons = [p for p in self.canvas_polygon_list() if 'Risk' in p.name]
        for polygon in outlook_polygons:
            polygon.delete()
        sys.stdout.write(f'Removed {len(outlook_polygons)} outlook polygons')
    
    def alert_popup(self, polygon: tkmap.map_widget.CanvasPolygon) -> None:
        """
        Internal method that displays a popup when clicking on an alert polygon.
        """
        dialog = tk.Toplevel(self)
        dialog.iconbitmap('warningnav.ico')
        dialog.title(polygon.data.alert_type)

        text_widget = ScrolledText(dialog, wrap=tk.WORD)
        text_widget.insert(tk.END, polygon.data.description)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill='both')
        
        sys.stdout.write(f'Displaying alert: {polygon.data.parameters}')
    
    def _map_motion(self, event: tk.Event) -> None:
        """
        Method that is called whenever the map is moved.
        
        Parameters
        ----------
        event: tk.Event
            Event that is generated whenever the map is moved. This parameter is not currently used for anything but is
            required for binding this method to the map motion.
        """
        # current map zoom
        zoom = int(self.map_widget.zoom)
        if zoom < self.map_widget.min_zoom:
            self.map_widget.set_zoom(self.map_widget.min_zoom)
        
        y, x = self.map_widget.get_position()
        
        left, top, right, bottom = self.center_positions[zoom]
        sys.stdout.write(f'BEFORE: [zoom={zoom}, {self.map_widget.get_position()}')
        
        if x < left:
            self.map_widget.set_position(y, left)
        elif x > right:
            self.map_widget.set_position(y, right)
        
        if y > top:
            self.map_widget.set_position(top, x)
        elif y < bottom:
            self.map_widget.set_position(bottom, x)
        
    def _run_automatic_alert_updates(self,
                                     update_freq: int = 10,
                                     max_updates: int = 8640,
                                     buffer_time_sec: float = 1.0
                                     ) -> None:
        """
        Complete workflow for updating active alerts.
        
        Parameters
        ----------
        update_freq: int (default = 10)
            Alert update frequency in seconds.
        max_updates: int (default = 8640)
            Max number of times that the warnings will automatically update before terminating. This parameter is only
            used to prevent an infinite loop when updating alerts.
        buffer_time_sec: float (default = 1.0)
            Number of seconds to allow for debug information to buffer to the debug log. This only affects the first
            update to NWS alerts right after the app is opened.
        
        Notes
        -----
        With the default parameters, the automatic warning updates will stop after the app has been continuously open
        for about 24 hours.
        """
        update_count = 0
        while update_count < max_updates:
            time.sleep(buffer_time_sec)  # allows warning retrieval information to buffer to debug log
            self.alerts.update_alerts()
            self._draw_new_alert_polygons()
            self._remove_old_alert_polygons()
            sys.stdout.write(f'Active alert polygons: {len(self.canvas_polygon_list())}')
            time.sleep(update_freq - buffer_time_sec)
            update_count += 1

    def _draw_new_alert_polygons(self) -> None:
        """
        Draw polygons for new NWS alerts.
        """
        new_alert_polygons = []
        for alert_type in list(DEFAULT_ALERT_PROPERTIES.keys())[::-1]:
            new_alert_polygons.extend([dict(
                coordinates=alert.geometry['coordinates'],
                fill_color=DEFAULT_ALERT_PROPERTIES[alert.alert_type][1],
                border_color=DEFAULT_ALERT_PROPERTIES[alert.alert_type][1],
                border_width=2,
                name=alert.alert_type,
                data=alert)
                for alert in self.alerts.alerts_with_geometry
                if alert.alert_type == alert_type
                and alert.alert_id in self.alerts.new_alert_ids])
        
        for polygon in new_alert_polygons:
            self.draw_alert_polygon(**polygon)
    
    def _remove_old_alert_polygons(self) -> None:
        """
        Remove polygons for NWS alerts that are no longer active.
        """
        polygons = [p for p in self.canvas_polygon_list() if hasattr(p.data, 'alert_id')]
        polygons_to_remove = [p for p in polygons if p.data.alert_id in self.alerts.old_alert_ids]
        for polygon in polygons_to_remove:
            polygon.delete()
    
    def canvas_polygon_list(self) -> list[tkmap.map_widget.CanvasPolygon]:
        """
        Returns a list of all polygons currently shown on the map.
        """
        return self.map_widget.canvas_polygon_list


def start_application():

    loading_screen_root.destroy()
    AlertDashboard()


if __name__ == '__main__':
    
    # loading_screen_root = tk.Tk()
    # loading_screen_root.title('WarningNav')
    #
    # label = tk.Label(loading_screen_root)
    # label.pack(fill='both')
    #
    # player = tkvideo('loading_720p.mp4', label, loop=1, size=(1280, 720))
    # player.play()
    #
    # loading_screen_root.state('zoomed')
    # loading_screen_root.iconbitmap('warningnav.ico')
    # loading_screen_root.after(random.randint(4600, 9200), start_application)
    # loading_screen_root.mainloop()

    AlertDashboard()