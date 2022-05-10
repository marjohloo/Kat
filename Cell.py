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
from   tkinter import filedialog

# https://ttkbootstrap.readthedocs.io/en/latest/
# python -m pip install ttkbootstrap
import ttkbootstrap as ttk
from   ttkbootstrap.constants import *
from   ttkbootstrap.dialogs   import Messagebox

# Project imports
from Kat import *

# Useful characters ← ↑ → ↓ × ▲ ► ▼ ◄ ˂ ˃ ˄ ˅

STYLE_FRAME = False
PAD         = 1
WIDTH_ROW   = 32
WIDTH_COL   = 16
WIDTH_BUT   = 1

class Cell:

    def __init__(self, kat, parent, row, col, type, value):
        self.kat       = kat
        self.row       = row
        self.col       = col
        self.type      = type
        self.var       = ttk.StringVar(value=value)
        self.var.trace_add("write", lambda *_: self.var_write())
        self.frame     = ttk.Frame(parent)
        if STYLE_FRAME:
            if row & 0x1:
                if col & 0x1:
                    self.frame.configure(bootstyle="light")
                else:
                    self.frame.configure(bootstyle="dark")
            else:
                if col & 0x1:
                    self.frame.configure(bootstyle="dark")
                else:
                    self.frame.configure(bootstyle="light")
        self.frame.grid(column=self.col, row=self.row, sticky=(W, S, E))
        self.button      = None
        self.entry       = None
        self.button_ul   = None
        self.button_dr   = None
        if self.type == "data":
            self.button = ttk.Button(self.frame, textvariable=self.var, command=self.button_data)
            self.button.grid(column=0, row=0, sticky=(N, W, S, E), padx=PAD, pady=PAD)
            self.frame.columnconfigure(0, weight=1)
            self.data_style()
            self.kat.saved = False
            #self.kat.window.update()
            #print(self.frame.grid_bbox())
        elif self.type == "row":
            self.button_ul   = ttk.Button(self.frame, text="˄", width=WIDTH_BUT, command=self.button_row_up,    bootstyle="primary")
            self.button      = ttk.Button(self.frame, text="×", width=WIDTH_BUT, command=self.button_row_del,   bootstyle="danger")
            self.button_dr   = ttk.Button(self.frame, text="˅", width=WIDTH_BUT, command=self.button_row_down,  bootstyle="primary")
            self.entry       = ttk.Entry (self.frame,           width=WIDTH_ROW, textvariable=self.var,         bootstyle="primary")
            self.button_ul.grid  (column=0, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
            self.button.grid     (column=1, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
            self.button_dr.grid  (column=2, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
            self.entry.grid      (column=3, row=0, sticky=(N, W, S, E), padx=PAD,     pady=PAD)
            self.frame.columnconfigure(3, weight=1)
            self.view()
            self.kat.saved = False
        elif self.type == "col":
            self.button_ul   = ttk.Button   (self.frame, text="˂", width=WIDTH_BUT, command=self.button_col_left,  bootstyle="info")
            self.button      = ttk.Button   (self.frame, text="×", width=WIDTH_BUT, command=self.button_col_del,   bootstyle="danger")
            self.button_dr   = ttk.Button   (self.frame, text="˃", width=WIDTH_BUT, command=self.button_col_right, bootstyle="info")
            self.entry       = ttk.Entry    (self.frame,           width=WIDTH_COL, textvariable=self.var,         bootstyle="info")
            self.button_ul.grid  (column=0, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=(PAD,0))
            self.button.grid     (column=1, row=0, sticky=(N, W, S, E), padx=PAD,     pady=(PAD,0))
            self.button_dr.grid  (column=2, row=0, sticky=(N, W, S, E), padx=(0,PAD), pady=(PAD,0))
            self.entry.grid      (column=0, row=1, sticky=(N, W, S, E), padx=PAD, pady=PAD, columnspan=3)
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)
            self.frame.columnconfigure(2, weight=1)
            self.view()
            self.kat.saved = False
        elif self.type == "origin":
            self.button_ul = ttk.Button(self.frame, text="+", width=WIDTH_BUT, command=self.kat.row_add,     bootstyle="primary")
            self.button    = ttk.Button(self.frame, text="*", width=WIDTH_BUT, command=self.kat.view_toggle, bootstyle="success")
            self.button_dr = ttk.Button(self.frame, text="+", width=WIDTH_BUT, command=self.kat.col_add,     bootstyle="info")
            self.entry     = ttk.Entry (self.frame,           width=WIDTH_ROW, textvariable=self.var,        bootstyle="dark")
            if self.col == 0:
                # Arrange like a row (for now)
                self.button_ul.grid(column=0, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
                self.button.grid   (column=1, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
                self.button_dr.grid(column=2, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
                self.entry.grid    (column=3, row=0, sticky=(N, W, S, E), padx=PAD,     pady=PAD)
                self.frame.columnconfigure(3, weight=1)
                # Force an update
                self.kat.window.update()
                # Get size
                x, y, w, h = self.frame.grid_bbox()
                # Apply width as minimum width for column
                self.kat.window.columnconfigure(self.col, minsize=w)
            # Now arrange as we want them
            self.frame.columnconfigure(3, weight=0)
            self.button_ul.grid(column=0, row=1, sticky=(N, W, S, E), padx=(PAD,0), pady=(0,PAD))
            self.button.grid   (column=1, row=1, sticky=(N, W, S, E), padx=PAD,     pady=(0,PAD))
            self.button_dr.grid(column=2, row=1, sticky=(N, W, S, E), padx=(0,PAD), pady=(0,PAD))
            self.entry.grid    (column=0, row=0, sticky=(N, W, S, E), padx=PAD, pady=PAD, columnspan=3)
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)
            self.frame.columnconfigure(2, weight=1)
            self.view()

    def var_write(self):
        # print(f'var_write       ({self.row}, {self.col})')
        self.kat.saved = False

    def button_data(self):
        value = self.var.get()
        if value == "0":
            value = "1"
        elif value == "1":
            value = "2"
        elif value == "2":
            value = "3"
        else:
            value = "0"
        self.var.set(value)
        self.data_style()

    def button_row_del(self):
        # print(f'button_row_del  ({self.row}, {self.col})')
        self.kat.row_del(self.row)

    def button_col_del(self):
        # print(f'button_col_del  ({self.row}, {self.col})')
        self.kat.col_del(self.col)

    def button_row_up(self):
        # print(f'button_row_up   ({self.row}, {self.col})')
        if self.row > 1:
            self.kat.row_swap(self.row, self.row-1)

    def button_row_down(self):
        # print(f'button_row_down ({self.row}, {self.col})')
        if self.row < self.kat.rows - 1:
            self.kat.row_swap(self.row, self.row+1)

    def button_col_left(self):
        # print(f'button_col_left ({self.row}, {self.col})')
        if self.col > 1:
            self.kat.col_swap(self.col, self.col-1)

    def button_col_right(self):
        # print(f'button_col_right({self.row}, {self.col})')
        if self.col < self.kat.cols - 1:
            self.kat.col_swap(self.col, self.col+1)

    def data_style(self):
        value = self.var.get()
        if value == "3":
            self.button.configure(bootstyle="success")
        elif value == "2":
            self.button.configure(bootstyle="warning")
        elif value == "1":
            self.button.configure(bootstyle="danger")
        else:
            self.button.configure(bootstyle="secondary")

    def grid(self):
        self.frame.grid(column=self.col, row=self.row, sticky=(W, S, E))
        if self.type == "row":
            if self.row == 1:
                self.button_ul.configure(state="disabled")
            else:
                self.button_ul.configure(state="normal")
            if self.row == self.kat.rows-1:
                self.button_dr.configure(state="disabled")
            else:
                self.button_dr.configure(state="normal")
        elif self.type == "col":
            if self.col == 1:
                self.button_ul.configure(state="disabled")
            else:
                self.button_ul.configure(state="normal")
            if self.col == self.kat.cols-1:
                self.button_dr.configure(state="disabled")
            else:
                self.button_dr.configure(state="normal")


    def view(self):
        if self.type == "row":
            if self.kat.view == "max":
                self.button_ul.grid()
                self.button_dr.grid()
                self.button.grid()
            else:
                self.button.grid_remove()
                self.button_dr.grid_remove()
                self.button_ul.grid_remove()
        elif self.type == "col":
            if self.kat.view == "max":
                self.button_ul.grid()
                self.button.grid()
                self.button_dr.grid()
            else:
                self.button_dr.grid_remove()
                self.button.grid_remove()
                self.button_ul.grid_remove()
        elif self.type == "origin":
            if self.kat.view == "max":
                self.button.configure(bootstyle="success")
            else:
                self.button.configure(bootstyle="success-outline")

    def move(self, row, col):
        self.row = row
        self.col = col
        self.grid()

    def destroy(self):
        if self.button != None:
            self.button.destroy()
        if self.entry != None:
            self.entry.destroy()
        if self.button_ul != None:
            self.button_ul.destroy()
        if self.button_dr != None:
            self.button_dr.destroy()
        self.frame.destroy()

    def key(row, col):
        return f'R{row:02}C{col:02}'