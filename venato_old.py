# Package imports
import json

# https://ttkbootstrap.readthedocs.io/en/latest/
# python -m pip install ttkbootstrap
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Venato:

    def __init__(self):
        # Initialise
        self.dat = {}
        self.gui = {}
        self.gui["window"] = ttk.Window()
        self.gui["window"].title("Venato")
        self.gui["window"].columnconfigure(0, weight=1)
        self.gui["window"].rowconfigure(0, weight=1)
        # Create outer frame
        self.gui["frame_outer"] = ttk.Frame(self.gui["window"])
        self.gui["frame_outer"].grid(column=0, row=0, sticky=(N, W, S, E))
        # Create table
        self.rows = 0
        self.cols = 0
        self.dat["table"] = []
        self.gui["table"] = []
        self.dat["table"].append([])
        self.gui["table"].append([])
        self.dat["table"][-1].append("ORIGIN")
        self.gui["table"][-1].append({})
        self.gui["table"][-1][-1]["frame"] = ttk.Frame(self.gui["frame_outer"])
        self.gui["table"][-1][-1]["frame"].grid(column=self.cols, row=self.rows, sticky=(N, W, S, E))
        self.gui["table"][-1][-1]["button_add_row"] = ttk.Button(self.gui["table"][-1][-1]["frame"], text="R+", command=self.button_add_row, bootstyle="primary")
        self.gui["table"][-1][-1]["button_add_row"].grid(column=0, row=0, sticky=(N, W, S, E), padx=1, pady=1)
        self.gui["table"][-1][-1]["button_add_col"] = ttk.Button(self.gui["table"][-1][-1]["frame"], text="C+", command=self.button_add_col, bootstyle="info")
        self.gui["table"][-1][-1]["button_add_col"].grid(column=1, row=0, sticky=(N, W, S, E), padx=1, pady=1)
        self.gui["table"][-1][-1]["frame"].columnconfigure(0, weight=1)
        self.gui["table"][-1][-1]["frame"].columnconfigure(1, weight=1)
        self.gui["frame_outer"].columnconfigure(self.cols, weight=1)
        # Debug
        print(json.dumps(self.dat, indent=4))
        print(f'rows={self.get_rows()}')
        print(f'cols={self.get_cols()}')
        # Start main loop
        self.gui["window"].mainloop()

    def get_rows(self):
        return len(self.dat["table"])

    def get_cols(self):
        return len(self.dat["table"][0])

    def button_add_row(self):
        self.add_row(f'ROW {self.get_rows()}', True)

    def button_add_col(self):
        self.add_col(f'COL {self.get_cols()}', True)

    def combo_changed(self, table_entry):
        combo_val = table_entry["var"].get()
        if combo_val < 0 or combo_val > 3:
            combo_val = 0
        style = "secondary"
        if combo_val == 1:
            style = "danger"
        elif combo_val == 2:
            style = "warning"
        elif combo_val == 3:
            style = "success"
        table_entry["combobox"].configure(bootstyle=style)
        table_entry["combobox"].selection_clear()

    def add_row(self, title, cells):
        r = self.get_rows()
        c = 0
        # Append new row
        self.dat["table"].append([])
        self.gui["table"].append([])
        # Append new title
        self.dat["table"][-1].append(title)
        self.gui["table"][-1].append({})
        row_title_cell = self.gui["table"][r][c]
        # Add row title
        row_title_cell["var"]   = ttk.StringVar(value=title)
        row_title_cell["entry"] = ttk.Entry(self.gui["frame_outer"], textvariable=row_title_cell["var"], bootstyle="primary")
        row_title_cell["entry"].grid(column=c, row=r, sticky=(N, W, S, E), padx=1, pady=1)
        # Add cells too ?
        if cells:
            self.add_row_cells(r)
        # Debug
        print(json.dumps(self.dat, indent=4))
        print(f'rows={self.get_rows()}')
        print(f'cols={self.get_cols()}')

    def add_row_cells(self, r):
        for c in range(1, self.get_cols()):
            # Append new cell
            self.dat["table"][r].append(f'(R{r},C{c})')
            self.gui["table"][r].append({})
            cell = self.gui["table"][r][c]
            # Add cell combo
            cell["var"] = ttk.IntVar(value=0)
            cell["combobox"] = ttk.Combobox(self.gui["frame_outer"], textvariable=cell["var"], bootstyle="secondary")
            cell["combobox"]["values"] = (0, 1, 2, 3)
            cell["combobox"].state(["readonly"])
            cell["combobox"].grid(column=c, row=r, sticky=(N, W, S, E), padx=1, pady=1)
            cell["combobox"].bind("<<ComboboxSelected>>", lambda *_, table_entry=self.gui["table"][-1][-1]: self.combo_changed(table_entry))

    def add_col(self, title, cells):
        r = 0
        c = self.get_cols()
        # Append new title
        self.dat["table"][0].append(title)
        self.gui["table"][0].append({})
        col_title_cell = self.gui["table"][r][c]
        # Add row title
        col_title_cell["var"]   = ttk.StringVar(value=title)
        col_title_cell["entry"] = ttk.Entry(self.gui["frame_outer"], textvariable=col_title_cell["var"], bootstyle="info")
        col_title_cell["entry"].grid(column=c, row=r, sticky=(N, W, S, E), padx=1, pady=1)
        # Add cells too ?
        if cells:
            self.add_col_cells(c)
        # Debug
        print(json.dumps(self.dat, indent=4))
        print(f'rows={self.get_rows()}')
        print(f'cols={self.get_cols()}')

    def add_col_cells(self, c):
        for r in range(1, self.get_rows()):
            # Append new cell
            self.dat["table"][r].append(f'(R{r},C{c})')
            self.gui["table"][r].append({})
            cell = self.gui["table"][r][c]
            # Add cell combo
            cell["var"] = ttk.IntVar(value=0)
            cell["combobox"] = ttk.Combobox(self.gui["frame_outer"], textvariable=cell["var"], bootstyle="secondary")
            cell["combobox"]["values"] = (0, 1, 2, 3)
            cell["combobox"].state(["readonly"])
            cell["combobox"].grid(column=c, row=r, sticky=(N, W, S, E), padx=1, pady=1)
            cell["combobox"].bind("<<ComboboxSelected>>", lambda *_, table_entry=self.gui["table"][-1][-1]: self.combo_changed(table_entry))

if __name__ == '__main__':
    venato = Venato()