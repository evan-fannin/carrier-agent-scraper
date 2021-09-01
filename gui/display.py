import tkinter as tk
from tkinter import StringVar, OptionMenu, messagebox
from carrier_agent_scraper.app import App
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(master=self, text="Select a carrier:")
        self.label.pack()

        self.carriers = ['Select One', 'Dairyland', 'Founders']

        self.selected_carrier = StringVar(self)
        self.selected_carrier.set(self.carriers[0])

        self.select1 = OptionMenu(self, self.selected_carrier, *self.carriers)
        self.select1.pack(pady=(0, 10))

        self.label2 = tk.Label(self, text="Select a state:")
        self.label2.pack()

        self.states = ['Select One', 'OH', 'PA']

        self.selected_state = StringVar(self)
        self.selected_state.set(self.states[0])

        self.select2 = OptionMenu(self, self.selected_state, *self.states)
        self.select2.pack(pady=(0, 10))

        self.button = tk.Button(self, text="Run", command=lambda: self.run_scraper(self.selected_carrier.get(), self.selected_state.get()))
        self.button.pack()

        self.progress_bar = tk.Label(self, text="", bg="light green")
        self.progress_bar.pack()
        self.progress_bar.pack_forget()

        self.button2 = tk.Button(self, text="Exit", command=lambda: self.master.destroy())
        self.button2.pack()

    def run_scraper(self, carrier, state):
        if not self.check_for_chromedriver_exec():
            return
        valid = self.validate_input()
        if valid:
            self.show_progress()
            self.app = App(self, carrier, state)
            self.app.run()

    def check_for_chromedriver_exec(self):
        base_path = os.path.expanduser("~\Downloads")
        specific_path = "chromedriver_win32\chromedriver.exe"
        webdriver_exec_path = os.path.join(base_path, specific_path)

        if not os.path.isfile(webdriver_exec_path):
            messagebox.showerror("ChromeDriver not found.", "Please download ChromeDriver at "
                                                            "https://chromedriver.chromium.org/ \n\n"
                                                            "You will find it under 'Latest Stable Release'.\n\n"
                                                            "Once downloaded, unzip it and leave it as is in your 'Downloads' folder.")
            return False
        return True

    def validate_input(self):
        if self.selected_carrier.get() == self.carriers[0]:  # Check if no carrier was selected
            messagebox.showerror("No Carrier Selected", "Please select a carrier.")
            return False

        elif self.selected_state.get() == self.states[0]:  # Check if no state was selected
            messagebox.showerror("No State Selected", "Please select a state.")
            return False

        return True

    def show_progress(self):
        self.progress_bar.config(text="Running now!")
        self.progress_bar.pack(pady=(20, 20))
        self.update()

    def update_progress(self, text):
        self.progress_bar.config(text=text)
        self.update()
        self.lift()

# Create a new window with the title "Address Entry Form"


# form = tk.Frame(master=window, borderwidth=3, bg='red')
# form.pack()

# label = tk.Label(master=form, text="Select a carrier:")
# label.pack()
#
# carriers = ['Dairyland', 'Bristol West']
#
# variable = StringVar(form)
# variable.set(carriers[0])
#
# select1 = OptionMenu(form, variable, *carriers)
# select1.pack(pady=10)
#
# button = tk.Button(form, text="Okay", command=lambda: gui_functions.ok(variable))
# button.pack()
#
# button2 = tk.Button(form, text="Exit", command=lambda: self.master.destroy())
# button2.pack()
