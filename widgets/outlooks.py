import tkinter as tk
from tkcalendar import Calendar
from noaa.spc.outlooks import ConvectiveOutlooks


class ConvectiveOutlookWidget(tk.Toplevel):
    def __init__(self, dashboard):
        """
        dashboard: main.AlertDashboard instance
        """
        super().__init__(master=dashboard)
        
        self.dashboard = dashboard
        
        screen_width = self.dashboard.winfo_width()
        screen_height = self.dashboard.winfo_height()
        
        self.attributes('-topmost', True)  # forces outlook selection window to stay on top
        self.geometry(f'{int(screen_width / 4)}x{int(screen_height / 4)}')
        self.resizable(False, False)
        self.title('Convective Outlook')
        self.type_options = {
            'Day 1': ['Categorical', 'Tornado', 'Hail', 'Wind'],
            'Day 2': ['Categorical', 'Tornado', 'Hail', 'Wind'],
            'Day 3': ['Categorical'],
            'Day 4': ['--'],
            'Day 5': ['--'],
            'Day 6': ['--'],
            'Day 7': ['--'],
            'Day 8': ['--'],
        }
        self.day_options = [f'Day {day}' for day in range(1, 9)]
        self.time_options = {
            'Day 1': ['0100', '1200', '1300', '1630', '2000'],
            'Day 2': ['0600', '1730'],
            'Day 3': ['0730', '1930'],
            'Day 4': ['--'],
            'Day 5': ['--'],
            'Day 6': ['--'],
            'Day 7': ['--'],
            'Day 8': ['--']
        }
        
        self.outlooks = ConvectiveOutlooks(self.dashboard)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        self.calendar = Calendar(self, selectmode="day")
        self.calendar.grid(column=1, sticky='nsew', rowspan=3)
        
        self.day = tk.StringVar(self)
        self.day.set(self.day_options[0])
        self.day_menu = tk.OptionMenu(self,
                                      self.day,
                                      *self.day_options,
                                      command=lambda e: self._day_selection(e))
        self.day_menu.config(bg='lightgray', font=('Times New Roman', '24'), indicatoron=False)
        self.day_menu.grid(row=0, column=0, sticky='nsew')
        
        self.otlk_type = tk.StringVar(self)
        self.otlk_type.set(self.type_options['Day 1'][0])
        self.otlk_type_menu = tk.OptionMenu(self,
                                            self.otlk_type,
                                            *self.type_options['Day 1'])
        self.otlk_type_menu.config(bg='lightgray', font=('Times New Roman', '24'), indicatoron=False)
        self.otlk_type_menu.grid(row=1, column=0, sticky='nsew')
        
        self.otlk_time = tk.StringVar(self)
        self.otlk_time.set(self.time_options['Day 1'][0])
        self.otlk_time_menu = tk.OptionMenu(self,
                                            self.otlk_time,
                                            *self.time_options['Day 1'])
        self.otlk_time_menu.config(bg='lightgray', font=('Times New Roman', '24'), indicatoron=False)
        self.otlk_time_menu.grid(row=2, column=0, sticky='nsew')
        
        apply_button = tk.Button(self, text="Show Outlook", command=self._show_outlook)
        apply_button.config(bg='lightblue', font=('Times New Roman', '24'))
        apply_button.grid(row=3, sticky='we', columnspan=2)
    
    def _day_selection(self, event):
        
        otlk_time_menu = self.otlk_time_menu["menu"]
        otlk_time_menu.delete(0, "end")
        new_options = self.time_options[event]
        self.otlk_time.set(new_options[0])
        for option in new_options:
            otlk_time_menu.add_command(label=option, command=tk._setit(self.otlk_time, option))
        
        otlk_type_menu = self.otlk_type_menu["menu"]
        otlk_type_menu.delete(0, "end")
        new_options = self.type_options[event]
        self.otlk_type.set(new_options[0])
        for option in new_options:
            otlk_type_menu.add_command(label=option, command=tk._setit(self.otlk_type, option))
    
    def _show_outlook(self):
        date = self.calendar.get_date()
        otlk_day = self.day.get()[-1]  # the outlook day is a single-digit integer at the end of the string
        otlk_type = self.otlk_type.get()
        otlk_time = self.otlk_time.get()
        
        self.outlooks.show_outlooks(date, otlk_day, otlk_type, otlk_time)


class FireOutlookWidget(tk.Toplevel):
    def __init__(self, dashboard):
        """
        dashboard: main.AlertDashboard instance
        """
        super().__init__(master=dashboard)
        
        self.title('Fire Weather Outlook')
        self.attributes('-topmost', True)  # forces outlook selection window to stay on top
        
        self.day_options = [f'Day {day}' for day in range(1, 9)]
        
        self.day = tk.StringVar(self)
        self.day.set(self.day_options[0])
        self.day_menu = tk.OptionMenu(self,
                                      self.day,
                                      *self.day_options)
        self.day_menu.pack()

        apply_button = tk.Button(self, text="Show Outlook")
        apply_button.pack()


class ExcessivePrecipitationOutlookWidget(tk.Toplevel):
    def __init__(self, dashboard):
        """
        dashboard: main.AlertDashboard instance
        """
        super().__init__(master=dashboard)
        
        self.title('Excessive Precipitation Outlook')
        self.attributes('-topmost', True)  # forces outlook selection window to stay on top
        
        self.day_options = [f'Day {day}' for day in range(1, 6)]
        
        self.day = tk.StringVar(self)
        self.day.set(self.day_options[0])
        self.day_menu = tk.OptionMenu(self,
                                      self.day,
                                      *self.day_options)
        self.day_menu.pack()

        apply_button = tk.Button(self, text="Show Outlook")
        apply_button.pack()