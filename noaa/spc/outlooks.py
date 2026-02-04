from datetime import datetime
from threading import Thread
from typing import Callable
import json
import requests
import sys
import tkintermapview as tkmap


class SPCOutlookPolygon(tkmap.map_widget.CanvasPolygon):

    def __init__(self,
                 map_widget: tkmap.TkinterMapView,
                 coordinates: list[list[float]],
                 label: str,
                 name: str,
                 valid_time: str,
                 expire_time: str,
                 issue_time: str,
                 stroke: str,
                 fill: str,
                 border_width: int = 5,
                 command: Callable = None) -> None:

        data = {'label': label,
                'valid_time': datetime.strptime(valid_time, '%Y%m%d%H%M'),
                'expire_time': datetime.strptime(expire_time, '%Y%m%d%H%M'),
                'issue_time': datetime.strptime(issue_time, '%Y%m%d%H%M')}

        super().__init__(map_widget,
                         coordinates,
                         outline_color=stroke,
                         fill_color=fill,
                         border_width=border_width,
                         command=command,
                         name=name,
                         data=data)


class SPCOutlook:

    def __init__(self, dashboard, url: str) -> None:

        self.dashboard = dashboard
        self.url = url
        self.outlook_polygons = []

        outlook_thread = Thread(target=self.main, name='outlook-thread', daemon=True)
        outlook_thread.start()

    def main(self):

        sys.stdout.write(f'Retrieving outlooks from {self.url}')
        content = requests.get(self.url).content
        features = json.loads(content)['features']
        
        self.dashboard.destroy_all_outlook_polygons()
        
        for feature in features:

            label = feature['properties']['LABEL']
            name = feature['properties']['LABEL2']
            valid_time = feature['properties']['VALID']
            expire_time = feature['properties']['EXPIRE']
            issue_time = feature['properties']['ISSUE']
            stroke = feature['properties']['stroke']
            fill = None

            # extract coordinates and convert from [lon, lat] to [lat, lon]
            for coord_list in feature['geometry']['coordinates']:
                coordinates = [[float(coords[1]), float(coords[0])] for coords in coord_list[0] if len(coords) == 2]

                p = SPCOutlookPolygon(self.dashboard.map_widget,
                                      coordinates,
                                      label,
                                      name,
                                      valid_time,
                                      expire_time,
                                      issue_time,
                                      stroke,
                                      fill)
                sys.stdout.write(f'Drawing {label} outlook polygon.')
                
                p.draw()
                self.dashboard.map_widget.canvas_polygon_list.append(p)
                self.dashboard.map_widget.canvas.itemconfig(p.canvas_polygon, state='disabled')