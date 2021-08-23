import tkinter as tk
from tkinter import StringVar, OptionMenu
from carrier_agent_scraper.app import App


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(master=self, text="Select a carrier:")
        self.label.pack()

        self.carriers = ['Select One', 'Dairyland', 'Bristol West']

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

        self.button2 = tk.Button(self, text="Exit", command=lambda: self.master.destroy())
        self.button2.pack()

    def run_scraper(self, carrier, state):
        app = App(carrier, state)
        app.run()

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
root = tk.Tk()
root.title = "Carrier Scraper"
app = Application(master=root)
app.mainloop()