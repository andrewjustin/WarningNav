from json import JSONDecodeError
from threading import Thread
from tkinter.scrolledtext import ScrolledText
import json
import numpy as np
import requests
import sys
import time
import tkinter as tk
import tkintermapview as tkmap
from typing import Any


# [Priority, Hex Code (color)]
DEFAULT_ALERT_PROPERTIES = {
    'Tsunami Warning': [1, '#FD6347'],
    'Tornado Warning': [2, '#FF0000'],
    'Extreme Wind Warning': [3, '#FF8C00'],
    'Severe Thunderstorm Warning': [4, '#FFA500'],
    'Flash Flood Warning': [5, '#8B0000'],
    'Flash Flood Statement': [6, '#8B0000'],
    'Fire Warning': [14, '#A0522D'],
    'Special Marine Warning': [21, '#FFA500'],
    'Dust Storm Warning': [28, '#FFE4C4'],
    'Flood Warning': [39, '#00FF00'],
    'Flood Advisory': [64, '#00FF7F'],
    'Dense Fog Advisory': [68, '#708090'],
    'Small Craft Advisory': [70, '#D8BFD8'],
    'Flood Watch': [89, '#2E8B57'],
    'Coastal Flood Statement': [99, '#6B8E23'],
    'Special Weather Statement': [101, '#FFE4B5'],
    'Marine Weather Statement': [102, '#FFDAB9'],
}


class NWSAlert:
    """
    Object containing information about active NWS alerts.
    """
    def __init__(self,
                 alert_id: str,
                 alert_type: str,
                 alert_code: str,
                 geometry: dict,
                 time_sent: str,
                 time_effective: str,
                 time_onset: str,
                 time_expires: str,
                 parameters: dict,
                 sender: str,
                 headline: str,
                 description: str
                 ):

        self.alert_id = alert_id
        self.alert_type = alert_type
        self.alert_code = alert_code
        self.geometry = self._convert_geom_coords(geometry)
        self.time_sent = time_sent
        self.time_effective = time_effective
        self.time_onset = time_onset
        self.time_expires = time_expires
        self.parameters = parameters
        self.sender = sender
        self.headline = headline
        self.description = description

    @staticmethod
    def _convert_geom_coords(geometry: dict | None) -> dict | None:
        """
        This method does two things:
            1) Rounds all coordinates to three decimal places (required for tkintermapview)
            2) Translates [lon, lat] coordinates to [lat, lon]
        """
        if isinstance(geometry, dict):
            geometry['coordinates'] = [np.round(coords, 3)[::-1] for coords in geometry['coordinates'][0]]

        return geometry


class NWSAlerts:
    """
    Class that handles the thread for updating NWS alerts on the dashboard.
    """
    def __init__(self, dashboard):
        """
        dashboard: main.AlertDashboard
        """
        self.dashboard = dashboard
        self._map_widget = dashboard.map_widget
        self.alerts = []
        self.alerts_with_geometry = None
        self.alerts_without_geometry = None

    def start_thread(self,
                     update_freq: int = 10,
                     max_updates: int = 1440) -> None:
        """
        Starts a thread for updating NWS alerts automatically in the background.

        Parameters
        ----------
        update_freq: int (default = 10)
            Alert update frequency in seconds.
        max_updates: int (default = 1440)
            Max number of times that the NWS alerts will automatically update before terminating. This parameter is
            only used to prevent an infinite loop when updating alerts.

        Notes
        -----
        With the default parameters, the automatic alert updates will stop after the app has been continuously open
        for about 24 hours.
        """
        sys.stdout.write(f'[NWSAlerts] Starting thread. update_freq={update_freq}, max_updates={max_updates}')

        self._thread = Thread(target=self._live_alert_updates,
                              name='auto-nws-alerts-thread',
                              daemon=True,
                              args=(update_freq, max_updates))
        self._thread.start()

    def update_alerts(self):
        """
        Performs a single update of active NWS alerts.
        """
        self._retrieve_alerts()
        self._update_alert_polygons()

    def _live_alert_updates(self,
                            update_freq: int,
                            max_updates: int) -> None:
        """
        Workflow for updating NWS alerts in real time.

        Parameters
        ----------
        update_freq: int
            Alert update frequency in seconds.
        max_updates: int
            Max number of times that NWS alerts will automatically update before terminating. This parameter is only
            used to prevent an infinite loop when updating alerts.

        Notes
        -----
        With the default parameters, the automatic alert updates will stop after the app has been continuously open
        for about 24 hours.
        """
        update_count = 0
        while update_count < max_updates:
            self.update_alerts()
            time.sleep(update_freq)
            update_count += 1

    def _retrieve_alerts(self) -> None:
        """
        Retrieve/update alerts from the National Weather Service.
        """

        alerts = retrieve_alerts()

        self._check_for_new_or_expired_alerts(alerts)
        self.alerts = alerts

        if len(self.new_alert_ids) > 0 or len(self.expired_alert_ids) > 0:
            self.dashboard.alerts_widget.update_alerts_in_table(alerts=alerts)

        self.alerts_with_geometry = [alert for alert in alerts if alert.geometry is not None]
        self.alerts_without_geometry = [alert for alert in alerts if alert.geometry is None]

    def _draw_alert_polygon(self,
                           coordinates: list,
                           fill_color: str,
                           border_color: str,
                           border_width: int,
                           name: str,
                           data = None) -> None:
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
        polygon = tkmap.map_widget.CanvasPolygon(map_widget=self._map_widget,
                                                 position_list=coordinates,
                                                 command=lambda p: self._alert_popup(p),
                                                 fill_color=fill_color,
                                                 outline_color=border_color,
                                                 border_width=border_width,
                                                 name=name,
                                                 data=data)

        polygon.draw()

        self._map_widget.canvas_polygon_list.append(polygon)

    def _update_alert_polygons(self) -> None:
        """
        Internal method that draws new alert polygons and removes expired and/or canceled alert polygons.
        """
        sys.stdout.write('[NWSAlerts] Updating alert polygons.')

        ### find new alert polygons ###
        new_alert_polygons = []
        for alert_type in list(DEFAULT_ALERT_PROPERTIES.keys())[::-1]:
            new_alert_polygons.extend([dict(
                coordinates=alert.geometry['coordinates'],
                fill_color=DEFAULT_ALERT_PROPERTIES[alert.alert_type][1],
                border_color=DEFAULT_ALERT_PROPERTIES[alert.alert_type][1],
                border_width=2,
                name=alert.alert_type,
                data=alert)
                for alert in self.alerts_with_geometry
                if alert.alert_type == alert_type
                and alert.alert_id in self.new_alert_ids])

        ### identify expired/canceled alert polygons ###
        polygons = [p for p in self._map_widget.canvas_polygon_list if hasattr(p.data, 'alert_id')]
        polygons_to_remove = [p for p in polygons if p.data.alert_id in self.expired_alert_ids]

        # draw new alert polygons
        for p in new_alert_polygons:
            polygon = tkmap.map_widget.CanvasPolygon(map_widget=self._map_widget,
                                                     position_list=p['coordinates'],
                                                     command=lambda p: self._alert_popup(p),
                                                     fill_color=p['fill_color'],
                                                     outline_color=p['border_color'],
                                                     border_width=p['border_width'],
                                                     name=p['name'],
                                                     data=p['data'])
            polygon.draw()
            self._map_widget.canvas_polygon_list.append(polygon)

        # remove expired/canceled alert polygons
        for polygon in polygons_to_remove:
            polygon.delete()

    def _check_for_new_or_expired_alerts(self, alerts):
        """
        Compares an updated alert list to what is currently saved in order to find new and expired alerts.

        alerts: latest NWS alerts.
        """
        new_alerts, expired_alerts = sort_new_and_expired_alerts(old_alerts=self.alerts, current_alerts=alerts)

        self.new_alert_ids = [alert.alert_id for alert in new_alerts if alert not in expired_alerts]
        self.expired_alert_ids = [alert.alert_id for alert in expired_alerts if alert not in new_alerts]

        sys.stdout.write(f'[NWSAlerts] {len(self.new_alert_ids)} new alert(s) found, '
                         f'{len(self.expired_alert_ids)} alert(s) are no longer active')

    def _alert_popup(self, polygon: tkmap.map_widget.CanvasPolygon) -> None:
        """
        Internal method that displays a popup when clicking on an alert polygon.
        """
        dialog = tk.Toplevel(self._map_widget)
        dialog.iconbitmap('warningnav.ico')
        dialog.title(polygon.data.alert_type)

        text_widget = ScrolledText(dialog, wrap=tk.WORD)
        text_widget.insert(tk.END, polygon.data.description)
        text_widget.config(state='disabled')
        text_widget.pack(expand=True, fill='both')

        sys.stdout.write(f'[NWSAlerts] Displaying alert: {polygon.data.parameters}')


def retrieve_alerts(parse: bool = True) -> list[NWSAlert] | Any:
    """
    Pull active alerts from the National Weather Service.

    parse: convert the raw JSON response into NWSAlert objects.
    """
    try:
        response = requests.get('https://api.weather.gov/alerts/active')
        content = json.loads(response.content)
    except JSONDecodeError:
        sys.stderr.write('noaa.nws.alerts.retrieve_alerts: Error encountered when reading response from NWS API.')

    if parse:
        try:
            alerts = list(map(lambda alert: NWSAlert(
                alert_id=alert['id'],
                alert_type=alert['properties']['event'],
                alert_code=alert['properties']['eventCode']['NationalWeatherService'][0],
                geometry=alert['geometry'],
                time_sent=alert['properties']['sent'],
                time_effective=alert['properties']['effective'],
                time_onset=alert['properties']['onset'],
                time_expires=alert['properties']['expires'],
                parameters=alert['properties']['parameters'],
                sender=alert['properties']['senderName'],
                headline=alert['properties']['headline'],
                description=alert['properties']['description']), content['features']))
        except UnboundLocalError as e:
            sys.stderr.write(str(e))

        return alerts

    else:
        return content


def parse_alerts_by_type(alerts: list[NWSAlert],
                         alert_type: str) -> list[NWSAlert]:
    """
    Return alerts of a desired type.
    """
    sys.stdout.write(f'noaa.nws.alerts.parse_alerts_by_type: returning alerts of type {alert_type}')
    return [alert for alert in alerts if alert.alert_type == alert_type]


def sort_new_and_expired_alerts(old_alerts: list[NWSAlert],
                                current_alerts: list[NWSAlert]) -> tuple[list[NWSAlert], list[NWSAlert]]:
    """
    Given lists of old alerts and current alerts, return lists of new alerts and expired alerts.
    """
    expired_alert_ids = [alert.alert_id for alert in old_alerts]
    current_alert_ids = [alert.alert_id for alert in current_alerts]

    new_alerts = [alert for alert in current_alerts if alert.alert_id not in expired_alert_ids]
    expired_alerts = [alert for alert in old_alerts if alert.alert_id not in current_alert_ids]

    return new_alerts, expired_alerts