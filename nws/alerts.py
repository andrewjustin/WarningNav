import requests
import json
import numpy as np


# [Priority, Hex Code (color)]
DEFAULT_ALERT_PROPERTIES = {
    'Tornado Warning': [2, '#FF0000'],
    'Severe Thunderstorm Warning': [4, '#FFA500'],
    'Flash Flood Warning': [5, '#8B0000'],
    'Fire Warning': [14, '#A0522D'],
    'Special Marine Warning': [21, '#FFA500'],
    'Dust Storm Warning': [28, '#FFE4C4'],
    'High Wind Warning': [30, '#DAA520'],
    'Flood Warning': [39, '#00FF00'],
    'Flood Advisory': [64, '#00FF7F'],
    'Flood Watch': [89, '#2E8B57'],
    'Special Weather Statement': [101, '#FFE4B5'],
    'Marine Weather Statement': [102, '#FFDAB9'],
}


class AlertData(object):
    """
    Object containing information about active NWS alerts.
    """
    def __init__(self,
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


def get_active_alerts() -> list[AlertData]:
    
    response = requests.get('https://api.weather.gov/alerts/active')
    content = json.loads(response.content)
    
    alerts = list(map(lambda alert: AlertData(
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
    
    return alerts