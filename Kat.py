# Package imports
import json
import os
from   tkinter import filedialog

# https://ttkbootstrap.readthedocs.io/en/latest/
# python -m pip install ttkbootstrap
import ttkbootstrap as ttk
from   ttkbootstrap.constants import *
from   ttkbootstrap.dialogs   import Messagebox

class Kat:

    def __init__(self):
        # Initialise data
        self.title = "KAT"
        self.cells = {}
        self.rows = 0
        self.cols = 0
        self.saved = False
        self.filename = ""
        # Invalidate outer frame
        self.frame_table = None
        # Initialise window
        self.window = ttk.Window()
        self.window.title(self.title)
        self.window.columnconfigure(0, weight=1)
        # Extract colors from window theme
        self.colors = self.window.style.colors
        print(f'primary={self.colors.get("primary")}')
        # Create window menu
        self.window.option_add("*tearOff", FALSE)
        #self.toplevel = ttk.Toplevel(self.window)
        self.menubar  = ttk.Menu(self.window)
        self.menufile = ttk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menufile, label="File")
        self.menufile.add_command(label="New",                accelerator="Ctrl+N",       command=self.file_new)
        #self.menufile.add_command(label="Open...",            accelerator="Ctrl+O",       command=self.file_open)
        self.menufile.add_command(label="Save",               accelerator="Ctrl+S",       command=self.file_save)
        self.menufile.add_command(label="Save As...",         accelerator="Ctrl+Shift+S", command=self.file_save_as)
        self.window["menu"] = self.menubar
        # Bind key presses to match menu
        self.window.bind("<Control-n>", lambda *_: self.file_new())
        self.window.bind("<Control-o>", lambda *_: self.file_open())
        self.window.bind("<Control-s>", lambda *_: self.file_save())
        self.window.bind("<Control-S>", lambda *_: self.file_save_as())
        # Create upper frame
        self.frame_upper = ttk.Frame(self.window)
        self.frame_upper.grid(row=0, column=0, sticky=(N, W, S, E))
        # Add frame controls
        self.var_title = ttk.StringVar(value="Title")
        self.entry_title = ttk.Entry(self.frame_upper, textvariable=self.var_title, bootstyle="success")
        self.entry_title.grid(row=0, column=0, sticky=(N, W, S, E), padx=1, pady=1)
        self.frame_upper.columnconfigure(0, weight=1)
        # Start with new file
        self.file_new()
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
        cell["frame"] = ttk.Frame(self.frame_table)
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
        cell["entry"] = ttk.Entry(cell["frame"], width=14, textvariable=cell["var"], bootstyle="info")
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
        cell["entry"] = ttk.Entry(cell["frame"], width=28, textvariable=cell["var"], bootstyle="primary")
        cell["entry"].grid(row=0, column=3, sticky=(N, W, S, E), padx=0, pady=0)
        cell["frame"].columnconfigure(3, weight=1)

    def cell_create_origin(self, cell):
        cell["value"] = "Target"
        cell["var"] = ttk.StringVar(value=cell["value"])
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
                    if col == 0:
                        self.frame_table.columnconfigure(col, weight=2)
                    else:
                        self.frame_table.columnconfigure(col, weight=1)
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
        self.saved = False

    def button_add_col(self):
        row = 0
        col = self.cols
        self.cell_create(row, col, "col")
        if self.rows > 1:
            for row in range(1, self.rows):
                self.cell_create(row, col, "data")
        self.cols += 1
        self.cells_grid()
        self.saved = False

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
        self.saved = False

    def file_new(self):
        do_new = False
        # Empty so need to create
        if self.rows < 1 or self.cols < 1:
            do_new = True
        # User data is present
        elif self.rows > 1 or self.cols > 1:
            if self.saved == False:
                confirm_new = Messagebox.show_question(title   = "File > New",
                                                       message = "Discard unsaved data and create new file?",
                                                       parent  = self.window)
                if confirm_new == "Yes":
                    do_new = True
            else:
                do_new = True
        if do_new:
            # Destroy widgets
            if self.frame_table != None:
                self.frame_table.destroy()
                self.frame_table = None
            # Reset data
            self.cells.clear()
            self.rows = 0
            self.cols = 0
            self.saved = True
            # Create table frame
            self.frame_table = ttk.Frame(self.window)
            self.frame_table.grid(row=1, column=0, sticky=(N, W, S, E))
            self.window.rowconfigure(1, weight=1)
            # Create origin cell
            self.cell_create(self.rows, self.cols, "origin")
            self.rows += 1
            self.cols += 1
            # Treat as unsaved
            self.saved == False
            # Grid the cells
            self.cells_grid()

    def file_open(self):
        do_open = Messagebox.okcancel(message="File > Open: not yet implemented", title="File > Open", parent=self.window)
        print(f'do_open = {do_open}')

    def file_save(self):
        # Don't have a current filename ?
        if self.filename == "":
            # Do a save as instead
            self.file_save_as()
        # Have a current filename ?
        else:
            self.file_write(self.filename)

    def file_save_as(self):
        filename = filedialog.asksaveasfilename(title            = "File > Save As",
                                                filetypes        = [("HTML Files", ".html")],
                                                defaultextension = ".html",
                                                parent           = self.window)
        if len(filename):
            self.file_write(filename)

    def file_view_saved(self):
        if self.filename != "":
            os.startfile(self.filename, 'open')

    def file_write(self, filename):
        if len(filename) > 0:
            with open(filename, "w") as f:
                # Output header
                f.write( '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n')
                f.write( '  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
                f.write( '<html xmlns="http://www.w3.org/1999/xhtml">\n')
                f.write( '  <head>\n')
                f.write(f'    <title>{self.var_title.get()}</title>\n')
                f.write( '    <style>\n')
                f.write( '        body              { font-size: 10pt; font-family: Arial,Helvetica,sans-serif; }\n')
                f.write( '        p                 { font-size: 10pt; }\n')
                f.write( '        h1                { font-size: 16pt; font-weight: bold; }\n')
                f.write( '        h2                { font-size: 12pt; font-weight: bold; }\n')
                f.write( '        table, tr, th, td { font-size: 10pt; text-align: center; vertical-align: top; border: 1px solid black; border-collapse: collapse; padding: 2pt}\n')
                f.write( '        .left             { text-align: left; }\n')
                f.write(f'        .primary          {{ background: {self.colors.get("primary")}; }}\n')
                f.write(f'        .secondary        {{ background: {self.colors.get("secondary")}; }}\n')
                f.write(f'        .success          {{ background: {self.colors.get("success")}; }}\n')
                f.write(f'        .warning          {{ background: {self.colors.get("warning")}; }}\n')
                f.write(f'        .primary          {{ background: {self.colors.get("primary")}; }}\n')
                f.write(f'        .danger           {{ background: {self.colors.get("danger")}; }}\n')
                f.write(f'        .info             {{ background: {self.colors.get("info")}; }}\n')
                f.write( '    </style>\n')
                f.write( '  </head>\n')
                # Output raw data
                f.write(f'  <!-- KAT_START "{self.var_title.get()}"')
                for row in range(self.rows):
                    for col in range(self.cols):
                        cell_key = self.cell_key(row, col)
                        if cell_key in self.cells:
                            cell = self.cells[cell_key]
                            val  = cell["var"].get()
                            # Quote if string
                            if isinstance(val, str):
                                val = '"'+val+'"'
                            # Need a new line ?
                            if col == 0:
                                f.write(f'\n    {val}')
                            else:
                                f.write(f', {val}')
                col_width = int(100/(self.cols+1))
                f.write('\n  KAT_END -->\n')
                # Begin body
                f.write('  <body>\n')
                f.write(f'    <h1>{self.var_title.get()}</h1>\n')
                # Output table data
                f.write('    <table width="100%">\n')
                for row in range(self.rows):
                    f.write('      <tr>\n')
                    for col in range(self.cols):
                        val = "-"
                        cell_key = self.cell_key(row, col)
                        if cell_key in self.cells:
                            cell = self.cells[cell_key]
                            val  = cell["var"].get()
                        hclass = ""
                        if row == 0 and col == 0:
                            hclass = "left"
                        elif row == 0:
                            hclass = ""
                        elif col == 0:
                            hclass = "left"
                        else:
                            if val == 3:
                                hclass = "success"
                            elif val == 2:
                                hclass = "warning"
                            elif val == 1:
                                hclass = "danger"
                            else:
                                hclass = "secondary"
                        if row == 0:
                            f.write( '        <th')
                            if hclass != "":
                                f.write(f' class="{hclass}"')
                            if col > 0:
                                f.write(f' width="{col_width}%"')
                            f.write( '>')
                        else:
                            if hclass == "":
                                f.write( '        <td>')
                            else:
                                f.write(f'        <td class="{hclass}">')
                        f.write(f'{val}')
                        if row == 0:
                            f.write('</th>\n')
                        else:
                            f.write('</td>\n')
                    f.write('      </tr>\n')
                f.write('    </table>\n')
                # End file
                f.write('  </body>\n')
                f.write('</html>\n')
                f.close()
                # Retain filename
                self.filename = filename
                # Update window
                self.window.title(f'{self.title}: {os.path.basename(self.filename)}')
                # Open file in browser
                os.startfile(self.filename, 'open')

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
        self.saved = False

if __name__ == '__main__':
    kat = Kat()