import sys
import requests
from lxml import etree
import tkinter as tk


class ConvectiveOutlooks:
    
    def __init__(self, dashboard):
        self.dashboard = dashboard

    def show_outlooks(self, date, otlk_day, otlk_type, otlk_time):
        
        self.destroy_convective_outlook_polygons()
        
        self.outlooks = {
            'Categorical': [],
            'Tornado': [],
            'Hail': [],
            'Wind': []
        }
        
        self._get_outlooks(date, otlk_day, otlk_time)
        self._plot_outlook_polygons(self.outlooks[otlk_type])
    
    def _get_outlooks(self, date, otlk_day, otlk_time):
        mo, dy, yr = date.split('/')
        yr = int('20' + yr)
        mo = int(mo)
        dy = int(dy)
        url = f'https://www.spc.noaa.gov/products/outlook/archive/{yr}/day{otlk_day}otlk_{yr}{mo:02d}{dy:02d}_{otlk_time}.kml'
        sys.stdout.write(f"Retrieving SPC outlooks from url: {url}")
        response = requests.get(url)
        
        ns = {"kml": "http://earth.google.com/kml/2.2"}
        tree = etree.fromstring(response.content)
        placemarks = tree.findall('.//kml:Placemark', namespaces=ns)
        
        for pm in placemarks:
            
            risk_info = {
                'name': pm.xpath(".//kml:SimpleData[@name='LABEL2']", namespaces=ns)[0].text,
                'stroke': pm.xpath(".//kml:SimpleData[@name='stroke']", namespaces=ns)[0].text,
                'fill': pm.xpath(".//kml:SimpleData[@name='fill']", namespaces=ns)[0].text,
                'polygons': self._extract_polygons(pm.xpath(".//kml:coordinates", namespaces=ns))
            }
            
            if risk_info['name'] is None:
                continue
            elif 'Tornado' in risk_info['name']:
                self.outlooks['Tornado'].append(risk_info)
            elif 'Hail' in risk_info['name']:
                self.outlooks['Hail'].append(risk_info)
            elif 'Wind' in risk_info['name']:
                self.outlooks['Wind'].append(risk_info)
            elif 'Any Severe Risk' not in risk_info['name']:
                self.outlooks['Categorical'].append(risk_info)
            else:
                pass
            
    def _plot_outlook_polygons(self, outlooks):
        sys.stdout.write('Drawing SPC outlook polygons')
        
        for outlook in outlooks:
            name = outlook['name']
            outline_color = outlook['stroke']
            border_width = 1 if 'Significant' in name else 3
            polygons = outlook['polygons']
            
            for polygon in polygons:
                p = self.dashboard.map_widget.set_polygon(
                    position_list=polygon,
                    fill_color=None,
                    border_width=border_width,
                    outline_color=outline_color,
                    data={'type': 'Convective Outlook',
                          'name': name})
                self.dashboard.map_widget.canvas.itemconfig(p.canvas_polygon, state=tk.DISABLED)
    
    def destroy_convective_outlook_polygons(self):
        sys.stdout.write('Destroying convective outlook polygons')
        polygons_with_dict_data = [p for p in self.dashboard.canvas_polygon_list() if isinstance(p.data, dict)]
        conv_outlook_polygons = [p for p in polygons_with_dict_data if p.data['type'] == 'Convective Outlook']
        for polygon in conv_outlook_polygons:
            polygon.delete()
        sys.stdout.write(f'Destroyed {len(conv_outlook_polygons)} outlook polygons')
    
    @staticmethod
    def _extract_polygons(elements):
        return [[tuple(map(float, coords.split(',')[::-1])) for coords in el.text.split(' ')] for el in elements]
        

def destroy_all_outlook_polygons(dashboard):
    """
    dashboard: main.AlertDashboard instance
    """
    polygons_with_dict_data = [p for p in dashboard.canvas_polygon_list() if isinstance(p.data, dict)]
    outlook_polygons = [p for p in polygons_with_dict_data if ['Outlook'] in p.data['type']]
    for polygon in outlook_polygons:
        polygon.delete()
    sys.stdout.write(f'Removed {len(outlook_polygons)} outlook polygons')