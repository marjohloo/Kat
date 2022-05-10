########################################################################
#
# Kerry's Assessment Tracker
#
# A tool to track pupil progress using a simple traffic light system.
#
# https://github.com/marjohloo/Kat
#
# Copyright 2022 Martin Looker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
########################################################################

# Package imports
import json
import os
import webbrowser
from   tkinter import filedialog

# https://ttkbootstrap.readthedocs.io/en/latest/
# python -m pip install ttkbootstrap
import ttkbootstrap as ttk
from   ttkbootstrap.constants import *
from   ttkbootstrap.dialogs   import Messagebox

# Project imports
from Cell import *

# Useful characters ← ↑ → ↓ × ▲ ► ▼ ◄ ˂ ˃ ˄ ˅

class Kat:

    def __init__(self):
        # Initialise data
        self.title = "Kerry's Assessment Tracker"
        self.version = "v1.0.3"
        self.cells = {}
        self.rows = 0
        self.cols = 0
        self.saved = True
        self.filename = ""
        #self.view_full = True
        self.view = "min"
        # Invalidate outer frame
        #self.frame_table = None
        # Initialise window
        self.window = ttk.Window()
        self.window.resizable(FALSE,FALSE)
        self.window.title(f'{self.title} - {self.version}')
        self.window.columnconfigure(0, weight=1)
        # Extract colors from window theme
        self.colors = self.window.style.colors
        # Create window menu
        self.window.option_add("*tearOff", FALSE)
        #self.toplevel = ttk.Toplevel(self.window)
        self.menubar  = ttk.Menu(self.window)
        self.menu = ttk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu, label="File")
        self.menu.add_command(label="New", accelerator="Ctrl+N", command=self.menu_new)
        self.window.bind("<Control-n>", lambda *_: self.menu_new())
        self.menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.menu_open)
        self.window.bind("<Control-o>", lambda *_: self.menu_open())
        self.menu.add_command(label="Save", accelerator="Ctrl+S", command=self.menu_save)
        self.window.bind("<Control-s>", lambda *_: self.menu_save())
        self.menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.menu_save_as)
        self.window.bind("<Control-S>", lambda *_: self.menu_save_as())
        self.menu.add_command(label="View HTML...", accelerator="Ctrl+H", command=self.menu_view_html)
        self.menu.entryconfigure("View HTML...", state=DISABLED)
        self.window.bind("<Control-h>", lambda *_: self.menu_view_html())
        self.menu.add_separator()
        self.menu.add_command(label="View Manual...", accelerator="F1", command=self.menu_view_manual)
        self.window.bind("<F1>",        lambda *_: self.menu_view_manual())
        self.menu.add_command(label="View Homepage...", accelerator="Ctrl+G", command=self.menu_view_homepage)
        self.window.bind("<Control-g>", lambda *_: self.menu_view_homepage())
        self.window["menu"] = self.menubar
        # Start with new file
        self.file_new()
        # Start main loop
        self.window.mainloop()

    def menu_new(self):
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

    def menu_open(self):
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

    def menu_save(self):
        # Don't have a current filename ?
        if self.filename == "":
            # Do a save as instead
            self.menu_save_as()
        # Have a current filename ?
        else:
            self.file_write(self.filename)

    def menu_save_as(self):
        filename = filedialog.asksaveasfilename(title            = "File > Save As",
                                                filetypes        = [("HTML Files", ".html")],
                                                defaultextension = ".html",
                                                parent           = self.window)
        if len(filename):
            self.file_write(filename)

    def menu_view_html(self):
        self.file_view_html()

    def menu_view_manual(self):
        os.startfile('Kat.pdf', 'open')

    def menu_view_homepage(self):
        webbrowser.open('https://github.com/marjohloo/Kat')

    def file_new(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell_key = Cell.key(row, col)
                if cell_key in self.cells:
                    cell = self.cells.pop(cell_key)
                    cell.destroy()
        self.rows = 0
        self.cols = 0
        cell_key = Cell.key(0, 0)
        if cell_key not in self.cells:
            self.cells[cell_key] = Cell(self, self.window, 0, 0, "origin", "TITLE")
        self.rows += 1
        self.cols += 1
        # Clear filename
        self.filename_set("")
        # Treat as saved (there is nothing there anyway)
        self.saved == True

    def file_read(self, filename):
        if len(filename) > 0:
            in_table = False
            out_table = False
            title = "TITLE"
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
            if False:
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
                        cell_key = Cell.key(row, col)
                        if row == 0 and col == 0:
                            if cell_key in self.cells:
                                self.cells[cell_key].var.set(title)
                            else:
                                self.cells[cell_key] = Cell(self, self.window, row, col, "origin", title)
                        elif row == 0:
                            if cell_key not in self.cells:
                                self.cells[cell_key] = Cell(self, self.window, row, col, "col", data[row][col])
                        elif col == 0:
                            if cell_key not in self.cells:
                                self.cells[cell_key] = Cell(self, self.window, row, col, "row", data[row][col])
                        else:
                            if cell_key not in self.cells:
                                self.cells[cell_key] = Cell(self, self.window, row, col, "data", data[row][col])
                # Update counts
                self.rows = rows
                self.cols = cols
                # Retain filename
                self.filename_set(filename)
                # Data is saved
                self.saved = True

    def cell_value(self, row, col):
        value = ""
        cell_key = Cell.key(row, col)
        if cell_key in self.cells:
            value = self.cells[cell_key].var.get()
        return value

    def cell_html(self, row, col, row_width):
        cell_value = self.cell_value(row, col)
        cell_html = '<'
        if row == 0:
            cell_html += 'th'
        else:
            cell_html += 'td'
        if row == 0 and col == 0:
            cell_html += ' class="left"'
        elif row == 0:
            pass
        elif col == 0:
            cell_html += ' class="left"'
        elif cell_value == "3":
            cell_html += ' class="success"'
        elif cell_value == "2":
            cell_html += ' class="warning"'
        elif cell_value == "1":
            cell_html += ' class="danger"'
        else:
            cell_html += ' class="secondary"'
        if col > 0 and row == row_width:
            cell_html += f' width="{int(100/(self.cols+1))}%"'
        cell_html += f'>{cell_value}<'
        if row == 0:
            cell_html += '/th'
        else:
            cell_html += '/td'
        cell_html += '>'
        return cell_html

    def file_write(self, filename):
        if len(filename) > 0:
            with open(filename, "w") as f:
                # Output header
                f.write( '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n')
                f.write( '  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
                f.write( '<html xmlns="http://www.w3.org/1999/xhtml">\n')
                f.write( '  <head>\n')
                f.write(f'    <title>{self.cell_value(0,0)}</title>\n')
                f.write(f'    <meta name="description" content="{self.cell_value(0,0)}" />\n')
                f.write(f'    <meta name="generator"   content="{self.title} {self.version}" />\n')
                f.write(f'    <link rel="help"         href="https://github.com/marjohloo/Kat" />\n')
                f.write(f'    <link rel="author"       href="https://github.com/marjohloo" />\n')
                f.write(f'    <link rel="license"      href="https://www.gnu.org/licenses/gpl-3.0.html" />\n')
                f.write( '    <style>\n')
                f.write( '        body              { font-size: 10pt; font-family: Calibri,Arial,Helvetica,sans-serif; }\n')
                f.write( '        div               { page-break-inside: avoid; }\n')
                f.write( '        p                 { font-size: 10pt; }\n')
                f.write( '        h1                { font-size: 16pt; font-weight: bold; }\n')
                f.write( '        h2                { font-size: 12pt; font-weight: bold; /* page-break-before: always; */ }\n')
                f.write( '        table, tr, th, td { font-size: 10pt; text-align: center; vertical-align: top; border: 1px solid black; border-collapse: collapse; padding: 2pt}\n')
                f.write( '        .page             { page-break-before: always; }\n')
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
                # Calculate column width percentage
                col_width = int(100/(self.cols+1))
                # Begin body
                f.write( '  <body>\n')
                f.write( '    <div>\n')
                f.write(f'      <h1>{self.cell_value(0,0)}</h1>\n')
                # Output table data
                f.write('      <table id="KAT" width="100%">\n')
                for row in range(self.rows):
                    f.write('        <tr>\n')
                    for col in range(self.cols):
                        if row == 0 and col == 0:
                            f.write('          <th></th>\n')
                        else:
                            f.write(f'          {self.cell_html(row, col, 0)}\n')
                    f.write('        </tr>\n')
                f.write('      </table>\n')
                f.write('    </div>\n')
                # Output individual data
                for col in range(1, self.cols):
                    if col == 1:
                        f.write('    <div class="page">\n')
                    else:
                        f.write('    <div>\n')
                    f.write(f'      <h2>{self.cell_value(0,0)}: {self.cell_value(0, col)}</h2>\n')
                    f.write( '      <table width="100%">\n')
                    for row in range(1, self.rows):
                        f.write( '        <tr>\n')
                        f.write(f'          {self.cell_html(row, 0,   1)}\n')
                        f.write(f'          {self.cell_html(row, col, 1)}\n')
                        f.write( '        </tr>\n')
                    f.write( '      </table>\n')
                    f.write('    </div>\n')
                # End file
                f.write('  </body>\n')
                f.write('</html>\n')
                f.close()
                # Retain filename
                self.filename_set(filename)
                # Data is saved
                self.saved = True

    def filename_set(self, filename):
        # Retain filename
        self.filename = filename
        # Got a filename ?
        if len(self.filename):
            self.window.title(f'{self.title} - {os.path.basename(self.filename)}')
            self.menu.entryconfigure("View HTML...", state=NORMAL)
        else:
            self.window.title(f'{self.title} - {self.version}')
            self.menu.entryconfigure("View HTML...", state=DISABLED)

    def view_toggle(self):
        if self.view == "min":
            self.view = "max"
        else:
            self.view = "min"
        for cell_key in sorted(self.cells):
            cell = self.cells[cell_key]
            if cell.row == 0 or cell.col == 0:
                cell.view()

    def row_add(self):
        row = self.rows
        for col in range(self.cols):
            cell_key = Cell.key(row, col)
            if cell_key not in self.cells:
                if col == 0:
                    self.cells[cell_key] = Cell(self, self.window, row, col, "row", f'ROW {row}')
                else:
                    self.cells[cell_key] = Cell(self, self.window, row, col, "data", "0")
        self.rows += 1
        cell_key = Cell.key(self.rows-1, 0)
        if cell_key in self.cells:
            self.cells[cell_key].grid()
        if self.rows > 1:
            cell_key = Cell.key(self.rows-2, 0)
            if cell_key in self.cells:
                self.cells[cell_key].grid()

    def col_add(self):
        col = self.cols
        for row in range(self.rows):
            cell_key = Cell.key(row, col)
            if cell_key not in self.cells:
                if row == 0:
                    self.cells[cell_key] = Cell(self, self.window, row, col, "col", f'COL {col}')
                else:
                    self.cells[cell_key] = Cell(self, self.window, row, col, "data", "0")
        self.cols += 1
        cell_key = Cell.key(0, self.cols-1)
        if cell_key in self.cells:
            self.cells[cell_key].grid()
        if self.cols > 1:
            cell_key = Cell.key(0, self.cols-2)
            if cell_key in self.cells:
                self.cells[cell_key].grid()

    def row_del(self, row):
        if row > 0 and row < self.rows:
            for col in range(self.cols):
                cell_key = Cell.key(row, col)
                if cell_key in self.cells:
                    self.cells.pop(cell_key).destroy()
            for row_move in range(row+1, self.rows):
                for col in range(self.cols):
                    cell_key = Cell.key(row_move, col)
                    if cell_key in self.cells:
                        cell = self.cells.pop(cell_key)
                        cell.move(row_move-1, col)
                        cell_key = Cell.key(row_move-1, col)
                        self.cells[cell_key] = cell
            self.rows -= 1
            cell_key = Cell.key(self.rows-1, 0)
            if cell_key in self.cells:
                self.cells[cell_key].grid()

    def col_del(self, col):
        if col > 0 and col < self.cols:
            for row in range(self.rows):
                cell_key = Cell.key(row, col)
                if cell_key in self.cells:
                    self.cells.pop(cell_key).destroy()
            for col_move in range(col+1, self.cols):
                for row in range(self.rows):
                    cell_key = Cell.key(row, col_move)
                    if cell_key in self.cells:
                        cell = self.cells.pop(cell_key)
                        cell.move(row, col_move-1)
                        cell_key = Cell.key(row, col_move-1)
                        self.cells[cell_key] = cell
            self.cols -= 1
            cell_key = Cell.key(0, self.cols-1)
            if cell_key in self.cells:
                self.cells[cell_key].grid()

    def row_swap(self, row_a, row_b):
        if row_a > 0 and row_a < self.rows and row_b > 0 and row_b < self.rows and row_a != row_b:
            for col in range(self.cols):
                cell_key_a = Cell.key(row_a, col)
                cell_key_b = Cell.key(row_b, col)
                if cell_key_a in self.cells and cell_key_b in self.cells:
                    cell_a = self.cells.pop(cell_key_a)
                    cell_b = self.cells.pop(cell_key_b)
                    cell_a.move(row_b, col)
                    cell_b.move(row_a, col)
                    self.cells[cell_key_b] = cell_a
                    self.cells[cell_key_a] = cell_b

    def col_swap(self, col_a, col_b):
        if col_a > 0 and col_a < self.cols and col_b > 0 and col_b < self.cols and col_a != col_b:
            for row in range(self.rows):
                cell_key_a = Cell.key(row, col_a)
                cell_key_b = Cell.key(row, col_b)
                if cell_key_a in self.cells and cell_key_b in self.cells:
                    cell_a = self.cells.pop(cell_key_a)
                    cell_b = self.cells.pop(cell_key_b)
                    cell_a.move(row, col_b)
                    cell_b.move(row, col_a)
                    self.cells[cell_key_b] = cell_a
                    self.cells[cell_key_a] = cell_b

    def file_view_html(self):
        if self.filename != "":
            # Open file in browser
            os.startfile(self.filename, 'open')

if __name__ == '__main__':
    kat = Kat()