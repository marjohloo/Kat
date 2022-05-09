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

# Useful characters ← ↑ → ↓ × ▲ ► ▼ ◄ ˂ ˃ ˄ ˅

STYLE_FRAME = False
PAD         = 1
WIDTH_ROW   = 48
WIDTH_COL   = 16
WIDTH_BUT   = 1

class Cell:

    def __init__(self, parent, row, col, type, value):
        self.row       = row
        self.col       = col
        self.type      = type
        self.var       = ttk.StringVar(value=value)
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
        self.button    = None
        self.entry     = None
        self.button_ul = None
        self.button_dr = None
        if self.type == "data":
            self.button = ttk.Button(self.frame, textvariable=self.var, command=self.button_data)
            self.button.grid(column=0, row=0, sticky=(N, W, S, E), padx=PAD, pady=PAD)
            self.frame.columnconfigure(0, weight=1)
            self.button_data_style()
        elif self.type == "row":
            self.button_ul = ttk.Button(self.frame, text="˄", width=WIDTH_BUT, command=self.button_row_up,    bootstyle="primary")
            self.button_dr = ttk.Button(self.frame, text="˅", width=WIDTH_BUT, command=self.button_row_down,  bootstyle="primary")
            self.entry     = ttk.Entry (self.frame,           width=WIDTH_ROW, textvariable=self.var,         bootstyle="primary")
            self.button    = ttk.Button(self.frame, text="×", width=WIDTH_BUT, command=self.button_row_del,   bootstyle="danger")
            self.button_ul.grid(column=0, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
            self.button_dr.grid(column=1, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=PAD)
            self.entry.grid    (column=2, row=0, sticky=(N, W, S, E), padx=PAD,     pady=PAD)
            self.button.grid   (column=3, row=0, sticky=(N, W, S, E), padx=(0,PAD), pady=PAD)
            self.frame.columnconfigure(2, weight=1)
        elif self.type == "col":
            self.button_ul = ttk.Button(self.frame, text="˂", width=WIDTH_BUT, command=self.button_col_left,  bootstyle="info")
            self.button    = ttk.Button(self.frame, text="×", width=WIDTH_BUT, command=self.button_col_del,   bootstyle="danger")
            self.button_dr = ttk.Button(self.frame, text="˃", width=WIDTH_BUT, command=self.button_col_right, bootstyle="info")
            self.entry     = ttk.Entry (self.frame,           width=WIDTH_COL, textvariable=self.var,         bootstyle="info")
            self.button_ul.grid(column=0, row=0, sticky=(N, W, S, E), padx=(PAD,0), pady=(PAD,0))
            self.button.grid   (column=1, row=0, sticky=(N, W, S, E), padx=PAD,     pady=(PAD,0))
            self.button_dr.grid(column=2, row=0, sticky=(N, W, S, E), padx=(0,PAD), pady=(PAD,0))
            self.entry.grid    (column=0, row=1, sticky=(N, W, S, E), padx=PAD, pady=PAD, columnspan=3)
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)
            self.frame.columnconfigure(2, weight=1)
        elif self.type == "origin":
            self.button_ul = ttk.Button(self.frame, text="+", width=WIDTH_BUT, command=self.button_row_add,   bootstyle="primary")
            self.button    = ttk.Button(self.frame, text="*", width=WIDTH_BUT, command=self.button_origin,    bootstyle="success")
            self.entry     = ttk.Entry (self.frame,           width=WIDTH_ROW, textvariable=self.var,         bootstyle="dark")
            self.button_dr = ttk.Button(self.frame, text="+", width=WIDTH_BUT, command=self.button_col_add,   bootstyle="info")
            self.button_ul.grid(column=0, row=0, sticky=(W, S, E), padx=(PAD,0), pady=PAD)
            self.button.grid   (column=1, row=0, sticky=(W, S, E), padx=(PAD,0), pady=PAD)
            self.entry.grid    (column=2, row=0, sticky=(W, S, E), padx=PAD,     pady=PAD)
            self.button_dr.grid(column=3, row=0, sticky=(W, S, E), padx=(0,PAD), pady=PAD)
            self.frame.columnconfigure(2, weight=1)

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
        self.button_data_style()

    def button_origin(self):
        print(f'button_origin   ({self.row}, {self.col})')

    def button_row_add(self):
        print(f'button_row_add  ({self.row}, {self.col})')

    def button_col_add(self):
        print(f'button_col_add  ({self.row}, {self.col})')

    def button_row_del(self):
        print(f'button_row_del  ({self.row}, {self.col})')

    def button_col_del(self):
        print(f'button_col_del  ({self.row}, {self.col})')

    def button_row_up(self):
        print(f'button_row_up   ({self.row}, {self.col})')

    def button_row_down(self):
        print(f'button_row_down ({self.row}, {self.col})')

    def button_col_left(self):
        print(f'button_col_left ({self.row}, {self.col})')

    def button_col_right(self):
        print(f'button_col_right({self.row}, {self.col})')

    def button_data_style(self):
        value = self.var.get()
        if value == "3":
            self.button.configure(bootstyle="danger")
        elif value == "2":
            self.button.configure(bootstyle="warning")
        elif value == "1":
            self.button.configure(bootstyle="success")
        else:
            self.button.configure(bootstyle="secondary")

    def grid(self):
        self.frame.grid(column=self.col, row=self.row, sticky=(N, W))

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