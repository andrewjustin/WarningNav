import sys
from datetime import datetime
from widgets.widget import Widget
from tkinter import ttk
from noaa.nws.alerts import NWSAlert, sort_new_and_expired_alerts, DEFAULT_ALERT_PROPERTIES
from typing import Any
import pytz


class AlertsWindowWidget(Widget):

    def __init__(self, dashboard):
        """
        dashboard: main.AlertDashboard instance
        """
        super().__init__(dashboard=dashboard)

        s = ttk.Style()
        s.configure('Treeview', rowheight=40)

        # attributes that will be used to sort the warnings window automatically whenever an alert(s) is added
        self._sort_by = 'issued'
        self._descending = True

        self.title('Active Alerts')
        self.attributes('-topmost', True)

        # configure the table columns
        self.tree = ttk.Treeview(self, columns=['id', 'alert_type', 'sender', 'issued', 'expires'], show='headings')
        self.tree.column('id')
        self.tree.heading('id', text='ID')
        self.tree.column('alert_type', stretch=True)
        self.tree.heading('alert_type', text='Alert Type', command=lambda: self.sort_by_values_in_column('alert_type'))
        self.tree.column('sender', stretch=True)
        self.tree.heading('sender', text='Sender', command=lambda: self.sort_by_values_in_column('sender'))
        self.tree.column('issued', stretch=True)
        self.tree.heading('issued', text='Issued (UTC)', command=lambda: self.sort_by_values_in_column('issued'))
        self.tree.column('expires', stretch=True)
        self.tree.heading('expires', text='Expires (UTC)', command=lambda: self.sort_by_values_in_column('expires'))
        self.tree.pack(fill='both', expand=True)

        self.tree['displaycolumns'] = ('alert_type', 'sender', 'issued', 'expires')

        # vertical scrollbar
        v_scrollbar = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side='right', fill='y')

        # configure tags for warnings
        for alert_type in DEFAULT_ALERT_PROPERTIES:
            self.tree.tag_configure(alert_type, background=DEFAULT_ALERT_PROPERTIES[alert_type][1])

        self.alerts = []

    def update_alerts_in_table(self, alerts: list[NWSAlert]) -> None:
        """
        Method that updates active alerts in the table.

        alerts: list of NWSAlert instances
            Latest set of active alerts.
        """
        sys.stdout.write('[AlertsWindowWidget] Updating alerts in table')

        new_alerts, expired_alerts = sort_new_and_expired_alerts(old_alerts=self.alerts, current_alerts=alerts)

        for new_alert in new_alerts:
            self.add_alert_to_table(alert=new_alert)

        for expired_alert in expired_alerts:
            self.remove_alert_from_table(alert=expired_alert)

        self.sort_by_values_in_column(col=self._sort_by, descending=self._descending)

        self.alerts = alerts

    def add_alert_to_table(self, alert: NWSAlert) -> None:
        """
        Adds an alert to the table.
        """
        alert = self.set_alert_timezone_to_utc(alert)
        values = (alert.alert_id, alert.alert_type, alert.sender, alert.time_effective, alert.time_expires)
        self.tree.insert('', 'end', values=values, tags=(alert.alert_type,))

    def remove_alert_from_table(self, alert: NWSAlert):
        """
        Removes an alert from the table by matching the alert ID.
        """
        for row in self.tree.get_children():
            row_alert_id = self.tree.item(row, 'values')[0]
            if row_alert_id == alert.alert_id:
                self.tree.delete(row)
                break  # there should be only alert for a given ID, so we can just stop the loop once we find the alert

    def sort_by_values_in_column(self, col: str, descending: bool = False) -> None:
        """
        Sort rows by values in the specified columns.

        col: str
        descending: bool (default = False)
            Sort the values in descending order.
        """
        data = [(self.tree.set(item, col), item) for item in self.get_rows()]
        data.sort(reverse=descending)
        for idx, (val, item) in enumerate(data):
            self.tree.move(item, '', idx)

        self.tree.heading(col, command=lambda: self.sort_by_values_in_column(col, not descending))

        self._sort_by = col
        self._descending = descending

    def get_column_values(self, col: str) -> list[Any]:
        """
        Retrieve all values for a specified column.

        col: str
        """
        values = []

        for child in self.tree.get_children():
            value = self.tree.set(child, col)  # value of the column for this row
            values.append(value)

        return values

    @staticmethod
    def set_alert_timezone_to_utc(alert: NWSAlert) -> NWSAlert:
        """
        Convert all time attributes in an alert to UTC.
        """

        input_format = '%Y-%m-%dT%H:%M:%S%z'
        output_format = '%Y-%m-%d %H:%M'

        old_time_sent = alert.time_sent
        old_time_effective = alert.time_effective
        old_time_onset = alert.time_onset
        old_time_expires = alert.time_expires

        try:
            new_time_sent = datetime.strptime(old_time_sent, input_format).astimezone(pytz.utc).strftime(output_format)
            new_time_effective = datetime.strptime(old_time_effective, input_format).astimezone(pytz.utc).strftime(output_format)
            new_time_onset = datetime.strptime(old_time_onset, input_format).astimezone(pytz.utc).strftime(output_format)
            new_time_expires = datetime.strptime(old_time_expires, input_format).astimezone(pytz.utc).strftime(output_format)
        except TypeError:
            sys.stderr.write(f'[AlertsWindowWidget] error encountered when converting timezone of alert (type={alert.alert_type}, '
                             f'sent={alert.time_sent}, effective={alert.time_effective}, onset={alert.time_onset}, '
                             f'expires={alert.time_expires}, parameters={alert.headline})')
            new_time_sent = 'unk'
            new_time_effective = 'unk'
            new_time_onset = 'unk'
            new_time_expires = 'unk'

        alert.time_sent = new_time_sent
        alert.time_effective = new_time_effective
        alert.time_onset = new_time_onset
        alert.time_expires = new_time_expires

        return alert

    def get_rows(self) -> tuple[str, ...]:
        return self.tree.get_children()