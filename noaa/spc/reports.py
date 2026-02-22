from lxml import etree
from pykml import parser
from threading import Thread
import hashlib
import io
import requests
import sys
import time
import vlc
import zipfile


DEFAULT_REPORT_COLORS = {
    'tornado': 'red',
    'hail': 'green',
    'wind': 'blue'
}


class SPCReport:
    """
    Object containing information for an SPC storm report.
    """
    def __init__(self, placemark):
        
        parser = etree.HTMLParser(encoding='utf-8')
        root = etree.fromstring(placemark.description.text, parser)
        
        tr = root[0][0][0]
        
        self.report_type = tr[0][0][0].tail.split(' ')[0].replace(' ', '')
        self.date, self.t = tr[0][1][6].tail.split('  ')[:2]
        self.mag = tr[0][1][8].tail
        self.location = tr[0][0][0].text
        self.county, self.state = tr[0][1][0].tail.split(', ')
        self.lat = float(tr[0][1][3].tail.replace(',', ''))
        self.lon = float(tr[0][1][4].tail.replace(',', ''))
        self.description = tr[0][2].text
        
        # reformatting and ID generation
        self._reformat_mag()
        self._generate_id()
        
    def _generate_id(self):
        """
        Generates a unique ID for the storm report.
        """
        report_str = str(f"{self.report_type}{self.date}{self.t}{self.mag}{self.location}{self.county}{self.state}"
                         f"{self.description}{self.lat}{self.lon}")
        self.id = hashlib.sha256(report_str.encode('utf-8')).hexdigest()

    def _reformat_mag(self):
        """
        Reformats the magnitude string of the storm report.
        """
        if 'Hail' in self.report_type:
            self.mag = self.mag.split(' ')[1]  # hail size (in.)
        elif 'Wind' in self.report_type:
            self.mag = "" if "Unknown" in self.mag else self.mag.split(' ')[1]  # mph
        else:
            self.mag = ""  # tornado reports do not have a magnitude


class SPCReports:
    """
    Class that handles the thread for updating SPC alerts on the dashboard.
    """
    def __init__(self, map_widget) -> None:
        """
        map_widget: main.AlertDashboard.map_widget
        """
        self._map_widget = map_widget
        self.reports = {'tornado': [], 'wind': [], 'hail': []}

    def start_thread(self,
                     update_freq: int = 60,
                     max_updates: int = 1440) -> None:
        """
        Starts a thread for updating SPC reports automatically in the background.
        
        Parameters
        ----------
        update_freq: int (default = 60)
            Report update frequency in seconds.
        max_updates: int (default = 1440)
            Max number of times that the SPC reports will automatically update before terminating. This parameter is
            only used to prevent an infinite loop when updating reports.

        Notes
        -----
        With the default parameters, the automatic report updates will stop after the app has been continuously open
        for about 24 hours.
        """
        sys.stdout.write(f'[SPCReports] Starting thread. update_freq={update_freq}, max_updates={max_updates}')
        
        self._thread = Thread(target=self._live_report_updates,
                              name='auto-spc-reports-thread',
                              daemon=True,
                              args=(update_freq, max_updates))
        self._thread.start()
    
    def update_reports(self):
        """
        Performs a single update of today's storm reports.
        """
        self._retrieve_reports()
        
        if len(self.new_report_ids) > 0:
            self._play_new_report_sound()
        
        self._draw_new_spc_reports()
    
    def _live_report_updates(self,
                             update_freq: int,
                             max_updates: int):
        """
        Workflow for updating storm reports in real time.
        
        Parameters
        ----------
        update_freq: int (default = 60)
            Report update frequency in seconds.
        max_updates: int (default = 1440)
            Max number of times that the SPC reports will automatically update before terminating. This parameter is
            only used to prevent an infinite loop when updating reports.

        Notes
        -----
        With the default parameters, the automatic report updates will stop after the app has been continuously open
        for about 24 hours.
        """
        update_count = 0  # total update count
        while update_count < max_updates:
            self.update_reports()
            time.sleep(update_freq)
    
    def _draw_new_spc_reports(self) -> None:
        """
        Draws new storm reports on the map widget.
        """
        new_reports = []
        for report_type in ['tornado', 'hail', 'wind']:
            new_reports.extend([dict(
                deg_x=report.lat,
                deg_y=report.lon,
                text=report.mag,
                marker_color_circle=DEFAULT_REPORT_COLORS[report_type],
                marker_color_outside='#000000',
                )
                for report in self.reports[report_type]
                if report.id in self.new_report_ids])
        
        for report in new_reports:
            self._map_widget.set_marker(**report)
        
        sys.stdout.write(f'[SPCReports] {len(new_reports)} new reports found.')
        
    def _retrieve_reports(self) -> None:
        """
        Retrieves today's filtered storm reports from the SPC.
        """
        sys.stdout.write('[SPCReports] Retrieving storm reports.')
        url = 'https://www.spc.noaa.gov/climo/reports/today_filtered.kmz'
        response = requests.get(url)
        kmz = io.BytesIO(response.content)
        
        # read the KMZ file containing today's reports
        try:
            kmz_zip = zipfile.ZipFile(kmz)
        except zipfile.BadZipFile:
            sys.stderr.write('[SPCReports] Error encountered when reading KMZ file. This error usually corrects itself after '
                             'a few minutes; contact Andrew Justin at andrewjustinwx@gmail.com or open an issue on our '
                             'GitHub page if this error persists.')
        else:
            with kmz_zip as f:
                kml_name = f.namelist()[0]
                kml = f.read(kml_name)
            
        root = parser.fromstring(kml)
        
        reports_torn = []
        reports_hail = []
        reports_wind = []
        
        """
        The KML will contain a 'Document' if any storm reports exist.
        If there are no reports, the 'Document' attribute will not exist.
        """
        try:
            _ = root.Document
        except AttributeError:
            sys.stdout.write('[SPCReports] No storm reports were found.')
    
        folder_torn = root.Document.Folder[1]
        folder_wind = root.Document.Folder[2]
        folder_hail = root.Document.Folder[3]
        
        # tornado reports
        try:
            reports_torn = [SPCReport(pm) for pm in folder_torn.Placemark]
        except AttributeError:
            sys.stdout.write('[SPCReports] No tornado reports found.')
        
        # wind reports
        try:
            reports_wind = [SPCReport(pm) for pm in folder_wind.Placemark]
        except AttributeError:
            sys.stdout.write('[SPCReports] No wind reports found.')
        
        # hail reports
        try:
            reports_hail = [SPCReport(pm) for pm in folder_hail.Placemark]
        except AttributeError:
            sys.stdout.write('[SPCReports] No hail reports found.')
    
        sys.stdout.write(f'[SPCReports] Total reports: T={len(reports_torn)} W={len(reports_wind)} H={len(reports_hail)}')
        
        reports = {'tornado': reports_torn,
                   'wind': reports_wind,
                   'hail': reports_hail}
        
        self._check_for_new_or_old_reports(reports)
        
        self.reports = reports
    
    def _check_for_new_or_old_reports(self, reports):
        """
        Checks for new storm reports.
        """
        saved_report_ids = []
        current_report_ids = []
        
        for report_type in ['tornado', 'wind', 'hail']:
            saved_report_ids.extend([report.id for report in self.reports[report_type]])
            current_report_ids.extend([report.id for report in reports[report_type]])
        
        self.new_report_ids = [report_id for report_id in current_report_ids if report_id not in saved_report_ids]
        self.old_report_ids = [report_id for report_id in saved_report_ids if report_id not in current_report_ids]
        
    @staticmethod
    def _play_new_report_sound():
        sound = vlc.MediaPlayer('default-report.mp3')
        sound.play()