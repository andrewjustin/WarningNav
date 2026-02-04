from noaa.nws.alerts import DEFAULT_ALERT_PROPERTIES
from noaa.spc.outlooks import SPCOutlook
import sys
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

        draw_test_polygon_menu.add_separator()

        draw_test_polygon_menu.add_command(label='Day 1 Convective Outlook (Categorical)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/outlook/archive/2025/day1otlk_20250315_1630_cat.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 1 Convective Outlook (Tornado)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/outlook/archive/2025/day1otlk_20250315_1630_torn.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 1 Convective Outlook (Hail)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/outlook/archive/2025/day1otlk_20250315_1630_hail.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 1 Convective Outlook (Wind)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/outlook/archive/2025/day1otlk_20250315_1630_wind.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 2 Convective Outlook (Categorical)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/outlook/archive/2025/day2otlk_20250314_1730_cat.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 2 Convective Outlook (Tornado)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/outlook/archive/2025/day2otlk_20250314_1730_torn.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 2 Convective Outlook (Hail)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/outlook/archive/2025/day2otlk_20250314_1730_hail.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 2 Convective Outlook (Wind)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/outlook/archive/2025/day2otlk_20250314_1730_wind.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 3 Convective Outlook (Categorical)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/outlook/archive/2025/day3otlk_20250313_1930_cat.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 3 Convective Outlook (Probabilistic)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/outlook/archive/2025/day3otlk_20250313_1930_prob.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 4 Convective Outlook (Probabilistic)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/exper/day4-8/archive/2025/day4prob_20250312.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 5 Convective Outlook (Probabilistic)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/exper/day4-8/archive/2025/day5prob_20250311.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 6 Convective Outlook (Probabilistic)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/exper/day4-8/archive/2025/day6prob_20250310.lyr.geojson'))
        draw_test_polygon_menu.add_command(label='Day 7 Convective Outlook (Probabilistic)',
                                           command=lambda: SPCOutlook(self.dashboard,
                                        'https://www.spc.noaa.gov/products/exper/day4-8/archive/2025/day7prob_20250309.lyr.geojson'))

        self.debug_menu.add_cascade(label="Draw Test Polygon", menu=draw_test_polygon_menu)

    def _draw_test_polygon(self,
                           alert_type: str):
        """
        Draw a single alert polygon.
        
        alert_type: str
            Name of the alert type.
        """
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