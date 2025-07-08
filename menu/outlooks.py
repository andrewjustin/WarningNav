import tkinter as tk


class OutlooksMenu(tk.Menu):
    """
    Outlook menu on the main dashboard's menubar.
    """
    def __init__(self, widget):
        """
        widget: main.AlertDashboard instance
        """
        super().__init__(master=widget, tearoff=False)
        self.widget = widget
        self.add_command(label="Convective Outlook",
                         command=lambda: ConvectiveOutlookMenu(widget))
        self.add_command(label="Fire Weather Outlook",
                         command=lambda: FireOutlookMenu(widget))
        self.add_command(label="Excessive Precipitation Outlook",
                         command=lambda: ExcessivePrecipitationOutlookMenu(widget))
    

class ConvectiveOutlookMenu(tk.Toplevel):
    def __init__(self, widget):
        """
        widget: main.AlertDashboard instance
        """
        super().__init__(master=widget)
        
        self.title('Convective Outlook')
        
        self.type_options = {
            'Day 1': ['Categorical', 'Tornado', 'Hail', 'Wind'],
            'Day 2': ['Categorical', 'Tornado', 'Hail', 'Wind'],
            'Day 3': ['--'],
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
        
        self.day = tk.StringVar(self)
        self.day.set(self.day_options[0])
        self.day_menu = tk.OptionMenu(self,
                                      self.day,
                                      *self.day_options,
                                      command=lambda e: self._day_selection(e))
        self.day_menu.pack()
        
        self.otlk_type = tk.StringVar(self)
        self.otlk_type.set(self.type_options['Day 1'][0])
        self.otlk_type_menu = tk.OptionMenu(self,
                                            self.otlk_type,
                                            *self.type_options['Day 1'])
        self.otlk_type_menu.pack()
        
        self.otlk_time = tk.StringVar(self)
        self.otlk_time.set(self.time_options['Day 1'][0])
        self.otlk_time_menu = tk.OptionMenu(self,
                                            self.otlk_time,
                                            *self.time_options['Day 1'])
        self.otlk_time_menu.pack()
        
        apply_button = tk.Button(self, text="Show Outlook")
        apply_button.pack()
    
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


class FireOutlookMenu(tk.Toplevel):
    def __init__(self, widget):
        """
        widget: main.AlertDashboard instance
        """
        super().__init__(master=widget)
        
        self.title('Fire Weather Outlook')

        self.day_options = [f'Day {day}' for day in range(1, 9)]
        
        self.day = tk.StringVar(self)
        self.day.set(self.day_options[0])
        self.day_menu = tk.OptionMenu(self,
                                      self.day,
                                      *self.day_options)
        self.day_menu.pack()

        apply_button = tk.Button(self, text="Show Outlook")
        apply_button.pack()


class ExcessivePrecipitationOutlookMenu(tk.Toplevel):
    def __init__(self, widget):
        """
        widget: main.AlertDashboard instance
        """
        super().__init__(master=widget)
        
        self.title('Excessive Precipitation Outlook')

        self.day_options = [f'Day {day}' for day in range(1, 6)]
        
        self.day = tk.StringVar(self)
        self.day.set(self.day_options[0])
        self.day_menu = tk.OptionMenu(self,
                                      self.day,
                                      *self.day_options)
        self.day_menu.pack()

        apply_button = tk.Button(self, text="Show Outlook")
        apply_button.pack()