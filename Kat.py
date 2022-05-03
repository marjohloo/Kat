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
        # Create window menu
        self.window.option_add("*tearOff", FALSE)
        #self.toplevel = ttk.Toplevel(self.window)
        self.menubar  = ttk.Menu(self.window)
        self.menufile = ttk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menufile, label="File")
        self.menufile.add_command(label="New",                accelerator="Ctrl+N",       command=self.menu_file_new)
        self.menufile.add_command(label="Open...",            accelerator="Ctrl+O",       command=self.file_open)
        self.menufile.add_command(label="Save",               accelerator="Ctrl+S",       command=self.file_save)
        self.menufile.add_command(label="Save As...",         accelerator="Ctrl+Shift+S", command=self.file_save_as)
        self.window["menu"] = self.menubar
        # Bind key presses to match menu
        self.window.bind("<Control-n>", lambda *_: self.menu_file_new())
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
        self.menu_file_new()
        # Start main loop
        self.window.mainloop()

    def cell_key(self, row, col):
        return f'R{row:02}C{col:02}'

    def cell_value(self, row, col):
        value = "-"
        cell_key = self.cell_key(row, col)
        if cell_key in self.cells:
            value = self.cells[cell_key]["var"].get()
        return value

    def cell_class(self, row, col):
        cell_class = ""
        if row == 0 and col == 0:
            cell_class = "left"
        elif row == 0:
            cell_class = ""
        elif col == 0:
            cell_class = "left"
        else:
            value = self.cell_value(row, col)
            if value == 3:
                cell_class = "success"
            elif value == 2:
                cell_class = "warning"
            elif value == 1:
                cell_class = "danger"
            else:
                cell_class = "secondary"
        if len(cell_class):
            cell_class = ' class="'+cell_class+'"'
        return cell_class

    def cell_create(self, row, col, type, value):
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
        # Cell type ?
        if type == "data":
            self.cell_create_data(cell, value)
        elif type == "col":
            self.cell_create_col(cell, value)
        elif type == "row":
            self.cell_create_row(cell, value)
        elif type == "origin":
            self.cell_create_origin(cell, value)

    def cell_create_data(self, cell, value):
        #cell["frame"].configure(bootstyle="secondary")
        cell["var"] = ttk.IntVar(value=int(value))
        cell["button"] = ttk.Button(cell["frame"], textvariable=cell["var"], command=lambda *_, cell=cell: self.button_data(cell), bootstyle="secondary")
        cell["button"].grid(column=0, row=0, sticky=(N, W, S, E))
        cell["frame"].columnconfigure(0, weight=1)
        self.cell_data_style(cell)

    def cell_create_col(self, cell, value):
        #cell["frame"].configure(bootstyle="info")
        if False:
            cell["button_left_col"] = ttk.Button(cell["frame"], text="˂", command=self.button_left_col, bootstyle="info")
            cell["button_left_col"].grid(row= 0, column=0, sticky=(N, W, S, E), padx=0, pady=0)
            cell["button_delete_col"] = ttk.Button(cell["frame"], text="X", command=self.button_delete_col, bootstyle="danger")
            cell["button_delete_col"].grid(row= 0, column=1, sticky=(N, W, S, E), padx=0, pady=0)
            cell["button_right_col"] = ttk.Button(cell["frame"], text="˃", command=self.button_right_col, bootstyle="info")
            cell["button_right_col"].grid(row=0, column=2, sticky=(N, W, S, E), padx=0, pady=0)
        cell["var"] = ttk.StringVar(value=value)
        cell["entry"] = ttk.Entry(cell["frame"], width=14, textvariable=cell["var"], bootstyle="info")
        cell["entry"].grid(row=0, column=3, sticky=(N, W, S, E), padx=0, pady=0)
        cell["frame"].columnconfigure(3, weight=1)

    def cell_create_row(self, cell, value):
        cell["var"] = ttk.StringVar(value=value)
        cell["entry"] = ttk.Entry(cell["frame"], width=28, textvariable=cell["var"], bootstyle="primary")
        cell["entry"].grid(row=0, column=3, sticky=(N, W, S, E), padx=0, pady=0)
        cell["frame"].columnconfigure(3, weight=1)

    def cell_create_origin(self, cell, value):
        cell["var"] = ttk.StringVar(value=value)
        cell["button_add_row"] = ttk.Button(cell["frame"], text="R+", width=3, command=self.button_add_row, bootstyle="primary")
        cell["button_add_row"].grid(row= 0, column=0, sticky=(N, W), padx=0, pady=0)
        cell["frame"].columnconfigure(0, weight=1)
        cell["button_add_col"] = ttk.Button(cell["frame"], text="C+", width=3, command=self.button_add_col, bootstyle="info")
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
        self.cell_create(row, col, "row", f'ROW {row}')
        if self.cols > 1:
            for col in range(1, self.cols):
                self.cell_create(row, col, "data", 0)
        self.rows += 1
        self.cells_grid()
        self.saved = False

    def button_add_col(self):
        row = 0
        col = self.cols
        self.cell_create(row, col, "col", f'COL {col}')
        if self.rows > 1:
            for row in range(1, self.rows):
                self.cell_create(row, col, "data", 0)
        self.cols += 1
        self.cells_grid()
        self.saved = False

    def button_data(self, cell):
        cell_value = cell["var"].get()
        cell_value += 1
        if cell_value > 3 or cell_value < 0:
            cell_value = 0
        cell["var"].set(cell_value)
        self.saved = False
        self.cell_data_style(cell)

    def cell_data_style(self, cell):
        cell_value = cell["var"].get()
        if cell_value > 3 or cell_value < 0:
            cell_value = 0
        style = "secondary"
        if cell_value == 3:
            style = "success"
        elif cell_value == 2:
            style = "warning"
        elif cell_value == 1:
            style = "danger"
        cell["button"].configure(bootstyle=style)


    def menu_file_new(self):
        do_new = False
        # Empty so need to create
        if self.rows < 1 or self.cols < 1:
            do_new = True
        # Unsaved user data is present
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
            self.file_new()

    def file_new(self):
        self.var_title.set("Title")
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
        self.cell_create(self.rows, self.cols, "origin", "")
        self.rows += 1
        self.cols += 1
        # Treat as unsaved
        self.saved == False
        # Grid the cells
        self.cells_grid()

    def file_open(self):
        do_open = False
        # Unsaved user data is present
        if self.rows > 1 or self.cols > 1:
            if self.saved == False:
                confirm_new = Messagebox.show_question(title   = "File > Open",
                                                       message = "Discard unsaved data and open file?",
                                                       parent  = self.window)
                if confirm_new == "Yes":
                    do_open = True
            else:
                do_open = True
        else:
            do_open = True
        # Ok to open ?
        if do_open:
            filename = filedialog.askopenfilename(title            = "File > Open",
                                                  filetypes        = [("HTML Files", ".html")],
                                                  defaultextension = ".html",
                                                  parent           = self.window)
            if len(filename):
                self.file_read(filename)

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
                f.write( '        body              { font-size: 10pt; font-family: Calibri,Arial,Helvetica,sans-serif; }\n')
                f.write( '        div               { page-break-inside: avoid; }\n')
                f.write( '        p                 { font-size: 10pt; }\n')
                f.write( '        h1                { font-size: 16pt; font-weight: bold; }\n')
                f.write( '        h2                { font-size: 12pt; font-weight: bold; /* page-break-before: always; */ }\n')
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
                if False:
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
                    f.write('\n  KAT_END -->\n')
                # Calculate column width percentage
                col_width = int(100/(self.cols+1))
                # Begin body
                f.write( '  <body>\n')
                f.write( '    <div>\n')
                f.write(f'      <h1>{self.var_title.get()}</h1>\n')
                # Output table data
                f.write('      <table id="KAT" width="100%">\n')
                for row in range(self.rows):
                    f.write('        <tr>\n')
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
                            f.write( '          <th')
                            if hclass != "":
                                f.write(f' class="{hclass}"')
                            if col > 0:
                                f.write(f' width="{col_width}%"')
                            f.write( '>')
                        else:
                            if hclass == "":
                                f.write( '          <td>')
                            else:
                                f.write(f'          <td class="{hclass}">')
                        f.write(f'{val}')
                        if row == 0:
                            f.write('</th>\n')
                        else:
                            f.write('</td>\n')
                    f.write('        </tr>\n')
                f.write('      </table>\n')
                f.write('    </div>\n')
                # Output individual data
                for col in range(1, self.cols):
                    f.write('    <div>\n')
                    f.write(f'      <h2>{self.var_title.get()}: {self.cell_value(0, col)}</h2>\n')
                    f.write( '      <table width="100%">\n')
                    for row in range(1, self.rows):
                        f.write( '        <tr>\n')
                        f.write(f'          <td{self.cell_class(row, 0)}>{self.cell_value(row, 0)}</td>\n')
                        if row == 1:
                            f.write(f'          <td{self.cell_class(row, col)} width="{col_width}%">{self.cell_value(row, col)}</td>\n')
                        else:
                            f.write(f'          <td{self.cell_class(row, col)}>{self.cell_value(row, col)}</td>\n')
                        f.write( '        </tr>\n')
                    f.write( '      </table>\n')
                    f.write('    </div>\n')
                # End file
                f.write('  </body>\n')
                f.write('</html>\n')
                f.close()
                # Data is saved
                self.saved = True
                # Retain filename
                self.filename = filename
                # Update window
                self.window.title(f'{self.title}: {os.path.basename(self.filename)}')
                # Open file in browser
                os.startfile(self.filename, 'open')

    def file_read(self, filename):
        if len(filename) > 0:
            in_table = False
            out_table = False
            title = "Title"
            data = []
            rows = 0
            cols = 0
            with open(filename, "r") as f:
                for line in f:
                    if in_table == False:
                        search = "<title>"
                        if search in line:
                            index = line.find(search)
                            if index >= 0:
                                line = line[index+len(search):]
                                search = "</title>"
                                if search in line:
                                    index = line.find(search)
                                    if index >= 0:
                                        line = line[:index]
                                        line = line.strip()
                                        title = line
                        search = '<table id="KAT"'
                        if search in line:
                            in_table = True
                    elif out_table == False:
                        if '<tr' in line:
                            data.append([])
                            rows += 1
                        elif '<th' in line:
                            index = line.find('<th')
                            start = line.find('>', index+len('<th'))+1
                            end   = line.find('</th>')
                            line  = line[start:end].strip()
                            data[-1].append(line)
                            if rows == 1:
                                cols += 1
                        elif '<td' in line:
                            index = line.find('<td')
                            start = line.find('>', index+len('<td'))+1
                            end   = line.find('</td>')
                            line  = line[start:end].strip()
                            data[-1].append(line)
                            if rows == 1:
                                cols += 1
                        elif '</table' in line:
                            out_table = True
                f.close()
            print(f'file_read({filename})')
            print(f'    title="{title}"')
            print(f'    out_table={out_table}')
            print(f'    rows={rows}')
            print(f'    cols={cols}')
            print(f'    data[{len(data)}]={data}')
            if len(data) == 0 or out_table == False:
                confirm_new = Messagebox.show_error(title   = "File > Open",
                                                    message = "KAT data not found in opened file!",
                                                    parent  = self.window)
            else:
                # Clear existing data
                self.file_new()
                # Rebuild new data
                for row in range(rows):
                    for col in range(cols):
                        if row == 0 and col == 0:
                            self.cell_create(row, col, "origin", data[row][col])
                        elif row == 0:
                            self.cell_create(row, col, "col", data[row][col])
                        elif col == 0:
                            self.cell_create(row, col, "row", data[row][col])
                        else:
                            self.cell_create(row, col, "data", data[row][col])
                # Update counts
                self.rows = rows
                self.cols = cols
                # Update title
                self.var_title.set(title)
                # Grid the cells
                self.cells_grid()
                # Data is saved
                self.saved = True
                # Retain filename
                self.filename = filename
                # Update window
                self.window.title(f'{self.title}: {os.path.basename(self.filename)}')

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

if __name__ == '__main__':
    kat = Kat()