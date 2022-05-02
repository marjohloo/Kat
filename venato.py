# Package imports
import json

# https://ttkbootstrap.readthedocs.io/en/latest/
# python -m pip install ttkbootstrap
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Venato:

    def __init__(self):
        # Initialise data
        self.cells = {}
        self.rows = 0
        self.cols = 0
        # Initialise window
        self.window = ttk.Window()
        self.window.title("Venato")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        # Create outer frame
        self.frame_outer = ttk.Frame(self.window)
        self.frame_outer.grid(row=0, column=0, sticky=(N, W, S, E))
        # Create origin cell
        self.cell_create(self.rows, self.cols, "origin")
        self.rows += 1
        self.cols += 1
        # Grid the cells
        self.cells_grid()
        # Start main loop
        self.window.mainloop()

    def cell_key(self, row, col):
        return f'R{row:02}C{col:02}'

    def cell_create(self, row, col, type):
        # Create empty cell info
        cell_key = self.cell_key(row, col)
        self.cells[cell_key] = {}
        cell = self.cells[cell_key]
        # Store fixed data
        cell["key"]   = cell_key
        cell["type"]  = type
        cell["row"]   = row
        cell["col"]   = col
        cell["frame"] = ttk.Frame(self.frame_outer)
        cell["value"] = None
        # Cell type ?
        if type == "data":
            self.cell_create_data(cell)
        elif type == "col":
            self.cell_create_col(cell)
        elif type == "row":
            self.cell_create_row(cell)
        elif type == "origin":
            self.cell_create_origin(cell)

    def cell_create_data(self, cell):
        #cell["frame"].configure(bootstyle="secondary")
        cell["value"] = 0
        cell["var"] = ttk.IntVar(value=cell["value"])
        if False:
            cell["radio0"] = ttk.Radiobutton(cell["frame"], text="0", variable=cell["var"], value=0, bootstyle="secondary-outline-toolbutton")
            cell["radio0"].grid(column=0, row=0, sticky=(N, W, S, E))
            cell["radio1"] = ttk.Radiobutton(cell["frame"], text="1", variable=cell["var"], value=1, bootstyle="danger-outline-toolbutton")
            cell["radio1"].grid(column=1, row=0, sticky=(N, W, S, E))
            cell["radio2"] = ttk.Radiobutton(cell["frame"], text="2", variable=cell["var"], value=2, bootstyle="warning-outline-toolbutton")
            cell["radio2"].grid(column=2, row=0, sticky=(N, W, S, E))
            cell["radio3"] = ttk.Radiobutton(cell["frame"], text="3", variable=cell["var"], value=3, bootstyle="success-outline-toolbutton")
            cell["radio3"].grid(column=3, row=0, sticky=(N, W, S, E))
            cell["frame"].columnconfigure(0, weight=1)
            cell["frame"].columnconfigure(1, weight=1)
            cell["frame"].columnconfigure(2, weight=1)
            cell["frame"].columnconfigure(3, weight=1)
        elif False:
            cell["combobox"] = ttk.Combobox(cell["frame"], textvariable=cell["var"], bootstyle="secondary")
            cell["combobox"]["values"] = (0, 1, 2, 3)
            cell["combobox"].state(["readonly"])
            cell["combobox"].grid(column=0, row=0, sticky=(N, W, S, E), padx=0, pady=0)
            cell["combobox"].bind("<<ComboboxSelected>>", lambda *_, cell=cell: self.combo_changed(cell))
            cell["frame"].columnconfigure(0, weight=1)
        else:
            cell["button"] = ttk.Button(cell["frame"], textvariable=cell["var"], command=lambda *_, cell=cell: self.button_data(cell), bootstyle="secondary")
            cell["button"].grid(column=0, row=0, sticky=(N, W, S, E))
            cell["frame"].columnconfigure(0, weight=1)

    def cell_create_col(self, cell):
        #cell["frame"].configure(bootstyle="info")
        if False:
            cell["button_left_col"] = ttk.Button(cell["frame"], text="˂", command=self.button_left_col, bootstyle="info")
            cell["button_left_col"].grid(row= 0, column=0, sticky=(N, W, S, E), padx=0, pady=0)
            cell["button_delete_col"] = ttk.Button(cell["frame"], text="X", command=self.button_delete_col, bootstyle="danger")
            cell["button_delete_col"].grid(row= 0, column=1, sticky=(N, W, S, E), padx=0, pady=0)
            cell["button_right_col"] = ttk.Button(cell["frame"], text="˃", command=self.button_right_col, bootstyle="info")
            cell["button_right_col"].grid(row=0, column=2, sticky=(N, W, S, E), padx=0, pady=0)
        cell["value"] = f'COL {cell["col"]}'
        cell["var"] = ttk.StringVar(value=cell["value"])
        cell["entry"] = ttk.Entry(cell["frame"], textvariable=cell["var"], bootstyle="info")
        cell["entry"].grid(row=0, column=3, sticky=(N, W, S, E), padx=0, pady=0)
        cell["frame"].columnconfigure(3, weight=1)

    def cell_create_row(self, cell):
        #cell["frame"].configure(bootstyle="primary")
        if False:
            cell["button_up_row"] = ttk.Button(cell["frame"], text="˄", command=self.button_up_row, bootstyle="primary")
            cell["button_up_row"].grid(row= 0, column=0, sticky=(N, W, S, E), padx=0, pady=0)
            cell["button_delete_row"] = ttk.Button(cell["frame"], text="X", command=self.button_delete_row, bootstyle="danger")
            cell["button_delete_row"].grid(row= 0, column=1, sticky=(N, W, S, E), padx=0, pady=0)
            cell["button_down_row"] = ttk.Button(cell["frame"], text="˅", command=self.button_down_row, bootstyle="primary")
            cell["button_down_row"].grid(row=0, column=2, sticky=(N, W, S, E), padx=0, pady=0)
        cell["value"] = f'ROW {cell["row"]}'
        cell["var"] = ttk.StringVar(value=cell["value"])
        cell["entry"] = ttk.Entry(cell["frame"], textvariable=cell["var"], bootstyle="primary")
        cell["entry"].grid(row=0, column=3, sticky=(N, W, S, E), padx=0, pady=0)
        cell["frame"].columnconfigure(3, weight=1)

    def cell_create_origin(self, cell):
        cell["button_add_row"] = ttk.Button(cell["frame"], text="R+", command=self.button_add_row, bootstyle="primary")
        cell["button_add_row"].grid(row= 0, column=0, sticky=(N, W), padx=0, pady=0)
        cell["frame"].columnconfigure(0, weight=1)
        cell["button_add_col"] = ttk.Button(cell["frame"], text="C+", command=self.button_add_col, bootstyle="info")
        cell["button_add_col"].grid(row=0, column=1, sticky=(N, E), padx=0, pady=0)
        cell["frame"].columnconfigure(1, weight=1)

    def cells_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if row == 0:
                    self.frame_outer.columnconfigure(col, weight=1)
                cell_key = self.cell_key(row, col)
                if cell_key in self.cells:
                    cell = self.cells[cell_key]
                    cell["frame"].grid(row=row, column=col, sticky=(N, W, S, E), padx=1, pady=1)

    def button_add_row(self):
        row = self.rows
        col = 0
        self.cell_create(row, col, "row")
        if self.cols > 1:
            for col in range(1, self.cols):
                self.cell_create(row, col, "data")
        self.rows += 1
        self.cells_grid()

    def button_add_col(self):
        row = 0
        col = self.cols
        self.cell_create(row, col, "col")
        if self.rows > 1:
            for row in range(1, self.rows):
                self.cell_create(row, col, "data")
        self.cols += 1
        self.cells_grid()

    def button_data(self, cell):
        cell_value = cell["var"].get()
        cell_value += 1
        if cell_value > 3 or cell_value < 0:
            cell_value = 0
        style = "secondary"
        if cell_value == 3:
            style = "success"
        elif cell_value == 2:
            style = "warning"
        elif cell_value == 1:
            style = "danger"
        cell["var"].set(cell_value)
        cell["button"].configure(bootstyle=style)

    def button_up_row(self):
        pass

    def button_down_row(self):
        pass

    def button_left_col(self):
        pass

    def button_right_col(self):
        pass

    def button_delete_row(self):
        pass

    def button_delete_col(self):
        pass

    def combo_changed(self, cell):
        combo_val = cell["var"].get()
        if combo_val < 0 or combo_val > 3:
            combo_val = 0
        style = "secondary"
        if combo_val == 1:
            style = "danger"
        elif combo_val == 2:
            style = "warning"
        elif combo_val == 3:
            style = "success"
        cell["combobox"].configure(bootstyle=style)
        cell["combobox"].selection_clear()

if __name__ == '__main__':
    venato = Venato()