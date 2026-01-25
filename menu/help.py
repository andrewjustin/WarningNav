import sys
from noaa.nws.alerts import DEFAULT_ALERT_PROPERTIES
import tkinter as tk


class HelpMenu(tk.Menu):
    """
    Help menu on the main dashboard's menubar.
    """
    def __init__(self, dashboard):
        """
        widget: main.AlertDashboard instance
        """
        super().__init__(master=dashboard, tearoff=False)
        self.dashboard = dashboard
        self._add_debug_cascade()
        self._add_draw_test_polygon_cascade()
        
    def _add_debug_cascade(self):
        """
        Internal method that adds a debug cascade to the help menu.
        """
        # debug menu
        self.debug_menu = tk.Menu(self, tearoff=False)
        self.debug_menu.add_command(label="Show Debug Log", command=lambda: self.dashboard.debug_log.master.deiconify())
        self.add_cascade(label="Debug", menu=self.debug_menu)
        
    def _add_draw_test_polygon_cascade(self):
        """
        Adds a cascade to the debug cascade with options to draw test polygons.
        """
        draw_test_polygon_menu = tk.Menu(self.debug_menu, tearoff=False)

        draw_test_polygon_menu.add_command(label='Tornado Warning',
                                           command=lambda: self._draw_test_polygon('Tornado Warning'))
        draw_test_polygon_menu.add_command(label='Severe Thunderstorm Warning',
                                           command=lambda: self._draw_test_polygon('Severe Thunderstorm Warning'))
        draw_test_polygon_menu.add_command(label='Flash Flood Warning',
                                           command=lambda: self._draw_test_polygon('Flash Flood Warning'))
        draw_test_polygon_menu.add_command(label='Fire Warning',
                                           command=lambda: self._draw_test_polygon('Fire Warning'))
        draw_test_polygon_menu.add_command(label='Special Marine Warning',
                                           command=lambda: self._draw_test_polygon('Special Marine Warning'))
        draw_test_polygon_menu.add_command(label='Dust Storm Warning',
                                           command=lambda: self._draw_test_polygon('Dust Storm Warning'))
        draw_test_polygon_menu.add_command(label='Flood Warning',
                                           command=lambda: self._draw_test_polygon('Flood Warning'))
        draw_test_polygon_menu.add_command(label='Special Weather Statement',
                                           command=lambda: self._draw_test_polygon('Special Weather Statement'))
        draw_test_polygon_menu.add_command(label='Marine Weather Statement',
                                           command=lambda: self._draw_test_polygon('Marine Weather Statement'))

        self.debug_menu.add_cascade(label="Draw Test Polygon", menu=draw_test_polygon_menu)

    def _draw_test_polygon(self,
                           alert_type: str):
        """
        Draw a single alert polygon.
        
        alert_type: str
            Name of the alert type.
        """
        sys.stdout.write(alert_type)
        test_polygon_data = {
            'coordinates': [[35.52, -97.8], [35.42, -97.8], [35.32, -97.4], [35.62, -97.4]],
            'fill_color': DEFAULT_ALERT_PROPERTIES[alert_type][1],
            'border_color': DEFAULT_ALERT_PROPERTIES[alert_type][1],
            'border_width': 2,
            'name': alert_type,
        }
        sys.stdout.write(f'TEST POLYGON {test_polygon_data}')
        
        self.dashboard.draw_alert_polygon(
            **test_polygon_data,
            data=test_polygon_data)