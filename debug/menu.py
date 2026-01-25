from datetime import datetime
import sys
import tkinter as tk


class DebugFileMenu(tk.Menu):
    """
    Menu for the debug log window.
    """
    def __init__(self, debug_log_window):
        """
        debug_log_window: widgets.debug.DebugLogWindow instance
        """
        super().__init__(master=debug_log_window, tearoff=False)

        self.debug_log_window = debug_log_window
        self.add_command(label="Clear Log", command=self._clear_log)
        self.add_command(label="Save Log", command=self._save_log)
    
    def _clear_log(self) -> None:
        """
        Clear the debug log.
        """
        log = self._get_debug_log()
        log.config(state='normal')
        log.delete("1.0", tk.END)
        log.config(state='disabled')
        sys.stdout.write('Cleared debug log')
    
    def _save_log(self) -> None:
        """
        Save the debug log.
        """
        # generate filename and printout debug log path
        fname = self._generate_log_fname()
        full_path = f'logs/{fname}.txt'
        sys.stdout.write(f'Saving debug log to: {full_path}')
        
        # get debug log contents
        log = self._get_debug_log()
        content = log.get("1.0", "end-1c")
        
        # save the debug log
        with open(full_path, 'w') as f:
            f.write(content)
    
    @staticmethod
    def _generate_log_fname() -> str:
        """
        Generate a filename for the debug log.
        """
        current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        fname = f'debuglog_{current_time}'
        return fname
    
    def _get_debug_log(self) -> tk.Widget:
        """
        Return the Tkinter widget containing the debug log.
        """
        return self.debug_log_window.children.get('!debuglog')