from noaa.spc.outlooks import SPCOutlook
import sys
import tkinter as tk


class GISMenu(tk.Menu):
    """
    GIS menu on the main dashboard's menubar.
    """
    def __init__(self, dashboard):
        """
        dashboard: main.AlertDashboard instance
        """
        super().__init__(master=dashboard, tearoff=False)
        self.dashboard = dashboard
        self._convective_outlook_cascade()
        self._fire_outlook_cascade()

        self.add_separator()
        self.add_command(label='Clear Outlook Polygons', command=lambda: self.dashboard.destroy_all_outlook_polygons())

    def _convective_outlook_cascade(self):
        """
        Internal method that adds options for selecting SPC convective outlooks.
        """
        convective_menu = tk.Menu(self.dashboard, tearoff=False)
        convective_menu.add_command(label='Day 1: Categorical',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/outlook/day1otlk_cat.lyr.geojson'))
        convective_menu.add_command(label='Day 1: Tornado',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/outlook/day1otlk_torn.lyr.geojson'))
        convective_menu.add_command(label='Day 1: Hail',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/outlook/day1otlk_hail.lyr.geojson'))
        convective_menu.add_command(label='Day 1: Wind',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/outlook/day1otlk_wind.lyr.geojson'))
        convective_menu.add_command(label='Day 2: Categorical',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/outlook/day2otlk_cat.lyr.geojson'))
        convective_menu.add_command(label='Day 2: Tornado',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/outlook/day2otlk_torn.lyr.geojson'))
        convective_menu.add_command(label='Day 2: Hail',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/outlook/day2otlk_hail.lyr.geojson'))
        convective_menu.add_command(label='Day 2: Wind',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/outlook/day2otlk_wind.lyr.geojson'))
        convective_menu.add_command(label='Day 3: Categorical',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/outlook/day3otlk_cat.lyr.geojson'))
        convective_menu.add_command(label='Day 3: Probabilistic',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/outlook/day3otlk_prob.lyr.geojson'))
        convective_menu.add_command(label='Day 4: Probabilistic',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/exper/day4-8/day4prob.nolyr.geojson'))
        convective_menu.add_command(label='Day 5: Probabilistic',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/exper/day4-8/day5prob.nolyr.geojson'))
        convective_menu.add_command(label='Day 6: Probabilistic',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/exper/day4-8/day6prob.nolyr.geojson'))
        convective_menu.add_command(label='Day 7: Probabilistic',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/exper/day4-8/day7prob.nolyr.geojson'))
        convective_menu.add_command(label='Day 8: Probabilistic',
                                    command=lambda: SPCOutlook(self.dashboard,
                                    'https://www.spc.noaa.gov/products/exper/day4-8/day8prob.nolyr.geojson'))

        self.add_cascade(label='(SPC) Convective Outlook', menu=convective_menu)

    def _fire_outlook_cascade(self):

        fire_menu = tk.Menu(self.dashboard, tearoff=False)
        fire_menu.add_command(label='Day 1: Dry Thunderstorms',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/fire_wx/day1fw_dryt.lyr.geojson'))
        fire_menu.add_command(label='Day 1: Wind/LowRH',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/fire_wx/day1fw_windrh.lyr.geojson'))
        fire_menu.add_command(label='Day 2: Dry Thunderstorms',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/fire_wx/day2fw_dryt.lyr.geojson'))
        fire_menu.add_command(label='Day 2: Wind/LowRH',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/fire_wx/day2fw_windrh.lyr.geojson'))
        fire_menu.add_command(label='Day 3: Dry Thunderstorms (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day3fw_drytcat.lyr.geojson'))
        fire_menu.add_command(label='Day 3: Dry Thunderstorms (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day3fw_drytprob.lyr.geojson'))
        fire_menu.add_command(label='Day 3: Wind/LowRH (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day3fw_windrhcat.lyr.geojson'))
        fire_menu.add_command(label='Day 3: Wind/LowRH (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day3fw_windrhprob.lyr.geojson'))
        fire_menu.add_command(label='Day 4: Dry Thunderstorms (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day4fw_drytcat.lyr.geojson'))
        fire_menu.add_command(label='Day 4: Dry Thunderstorms (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day4fw_drytprob.lyr.geojson'))
        fire_menu.add_command(label='Day 4: Wind/LowRH (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day4fw_windrhcat.lyr.geojson'))
        fire_menu.add_command(label='Day 4: Wind/LowRH (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day4fw_windrhprob.lyr.geojson'))
        fire_menu.add_command(label='Day 5: Dry Thunderstorms (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day5fw_drytcat.lyr.geojson'))
        fire_menu.add_command(label='Day 5: Dry Thunderstorms (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day5fw_drytprob.lyr.geojson'))
        fire_menu.add_command(label='Day 5: Wind/LowRH (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day5fw_windrhcat.lyr.geojson'))
        fire_menu.add_command(label='Day 5: Wind/LowRH (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day5fw_windrhprob.lyr.geojson'))
        fire_menu.add_command(label='Day 6: Dry Thunderstorms (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day6fw_drytcat.lyr.geojson'))
        fire_menu.add_command(label='Day 6: Dry Thunderstorms (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day6fw_drytprob.lyr.geojson'))
        fire_menu.add_command(label='Day 6: Wind/LowRH (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day6fw_windrhcat.lyr.geojson'))
        fire_menu.add_command(label='Day 6: Wind/LowRH (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day6fw_windrhprob.lyr.geojson'))
        fire_menu.add_command(label='Day 7: Dry Thunderstorms (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day7fw_drytcat.lyr.geojson'))
        fire_menu.add_command(label='Day 7: Dry Thunderstorms (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day7fw_drytprob.lyr.geojson'))
        fire_menu.add_command(label='Day 7: Wind/LowRH (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day7fw_windrhcat.lyr.geojson'))
        fire_menu.add_command(label='Day 7: Wind/LowRH (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day7fw_windrhprob.lyr.geojson'))
        fire_menu.add_command(label='Day 8: Dry Thunderstorms (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day8fw_drytcat.lyr.geojson'))
        fire_menu.add_command(label='Day 8: Dry Thunderstorms (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day8fw_drytprob.lyr.geojson'))
        fire_menu.add_command(label='Day 8: Wind/LowRH (Categorical)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day8fw_windrhcat.lyr.geojson'))
        fire_menu.add_command(label='Day 8: Wind/LowRH (Probabilistic)',
                              command=lambda: SPCOutlook(self.dashboard,
                              'https://www.spc.noaa.gov/products/exper/fire_wx/day8fw_windrhprob.lyr.geojson'))
        self.add_cascade(label='(SPC) FireWX Outlook', menu=fire_menu)

    @staticmethod
    def _null_function():
        """
        Internal method used as a placeholder for unimplemented functionality.
        """
        sys.stdout.write('Clicked command has no current functionality.')
        pass