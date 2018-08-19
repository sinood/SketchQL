import tkFont
import sqlite3 as s3
import pandas as pd
from pandas import DataFrame
import os
import Tkinter as tk
from Tkinter import Text, Frame, Button

class SketchQL(object):

    def __init__(self, width, height, master = None):
        # Sets root frame for application window
        self.f = tk.Frame(master = None, width = width, height = height, bg = 'gray')
        # Establishes a connection to a sqlite3 file
        conn1 = s3.connect('database.sqlite3')
        self.conn1 = conn1
        # Converts tuple output rows to sqlite3 Row objects
        self.conn1.row_factory = s3.Row
        # Creates a cursor for the current connection
        self.cur = conn1.cursor()
        # Displays the application window and generates the widgets inside
        self.f.grid()
        self.create_widgets()

    # Clears all text from the text area
    def clear_display(self):
        self.text_area.delete('1.0','end')

    # Retrieves all text currently in the text area as a string
    def get_text(self):
        text = self.text_area.get('1.0', 'end')
        return text

    # Executes text currently in the text area either as a single SQL statement if
    #only one statement is found. Otherwise, it is executed as a script of more than
    #one statement. In the second case, no output is printed to the text area, even
    #if one or more SELECT statements is executed.
    def execute_from_input(self):
        statement = self.get_text()
        # Executes from a .sql file if the user successfully uses the keyword 'file'
        if statement.startswith('file'):
            statement = statement.replace('file', '')
            statement = statement.strip()
            self.execute_from_script(statement)
            self.text_area.insert(tk.END, '\nScript executed.\n')
        # Drops all tables if the user types the special statement "drop all tables"
        elif statement.lower().strip() == "drop all tables":
            self.drop_all_tables()
            self.text_area.insert(tk.END, '\nAll tables dropped.\n')
        else:
            try:
                self.cur.execute(statement)
                # Displays the contents of the cursor if a SELECT statement is found
                if statement.lower().startswith('select'):
                    result = self.cur.fetchall()
                    self.display_output(result)
                else:
                    self.text_area.insert(tk.END, '\n\n'+ statement.split()[0].upper() +' statement executed.\n')
                self.conn1.commit()
            except Exception as e:
                try:
                    self.cur.executescript(statement)
                    self.conn1.commit()
                    self.text_area.insert(tk.END, '\n\nOutput:\n' + 'Multiple statements found, executed as script.')
                # Displays a generic SQLite error message after failed execution
                except s3.Error as br:
                    self.text_area.insert(tk.END, '\n\n' + str(br))

    # Prints a list of all tables and views currently stored in the connected database
    #separately to the text box
    def show_tables_and_views(self):
        self.text_area.insert(tk.END, '\nTables:')
        self.cur.execute("select name from sqlite_master where type = 'table';")
        result = self.cur.fetchall()
        self.display_output(result)

        self.text_area.insert(tk.END, '\n\nViews:\n')
        self.cur.execute("select name from sqlite_master where type = 'view';")
        result = self.cur.fetchall()
        self.display_output(result)

    # Executes SQL statements from a script file given a file path
    def execute_from_script(self, file_path):
        file = open(file_path, "r")
        script = file.read()
        file.close()
        self.cur.executescript(script)

    # Displays table information for a given table name
    def show_table_info(self):
        try:
            table_name = self.get_text()
            self.cur.execute("PRAGMA table_info(" + table_name + ");")
            result = self.cur.fetchall()
            self.display_output(result)
        except:
            self.text_area.insert(tk.END, '\nNo Table name detected. Press "Clear", '
            'type in a table name, then press "Show Table Info". ')

    # Displays rows of data currently stored in the cursor as a formatted data table
    def display_output(self, result):
        try:
            df = DataFrame(result)
            df.columns = result[0].keys()
            self.text_area.insert(tk.END, '\n' + df.to_string())
            self.text_area.insert(tk.END, '\n' + self.text_div + '\n')
        except:
            self.text_area.insert(tk.END, '\nNone\n====================================================================================================\n')

    # Drops all tables currently stored in the connected database
    def drop_all_tables(self):
        self.conn1.text_factory = str
        self.cur.execute("select name from sqlite_master where type = 'table';")
        rows = self.cur.fetchall()
        for row in rows:
            self.cur.execute("DROP TABLE " + row[0] + ";")
            self.conn1.commit()

    # Imports a demo company database and populates it with sample data
    def add_demo_data(self):
        self.execute_from_script('SketchQL/dist/sample_database.sql')
        self.execute_from_script('SketchQL/dist/sample_organizationdata.sql')
        self.conn1.commit()

    # Displays text from 'help.txt' to the text box to assist the user
    def get_help(self):
        help_file = open('SketchQL/dist/help.txt','r')
        help_text = help_file.read()
        self.text_area.insert(tk.END, '\n' + help_text + '\n')

    def get_about(self):
        help_file = open('SketchQL/dist/README.txt','r')
        help_text = help_file.read()
        self.text_area.insert(tk.END, '\n' + help_text + '\n')

    # Closes the application
    def close_app(self):
        self.cur.close()
        self.conn1.close()
        self.f.quit()

    # Generates the UI elements of the application and inserts them into the root frame
    def create_widgets(self):

        # Text area
        self.text_area = tk.Text(self.f, width = 100, font = tkFont.Font(family = 'Courier', size = 12), bd = 5, highlightbackground = 'gray')
        self.text_area.grid(sticky = tk.N+tk.S, row = 0, column = 1, columnspan = 1, rowspan = 10)

        # Menu section Frame
        menu_frame = tk.Frame(self.f, width = 150, bd = 5, bg = 'gray')
        menu_frame.grid(sticky = tk.N+tk.S, row = 0,column = 0, rowspan = 8)
        # Menu label
        menu_lbl_frame = tk.Frame(menu_frame, width = 150, height = 50, padx = 3, bg = 'gray')
        menu_lbl_frame.grid_propagate(False)
        menu_lbl_frame.columnconfigure(0, weight=1)
        menu_lbl_frame.rowconfigure(0,weight=1)

        menu_lbl = tk.Label(menu_lbl_frame, text = 'Menu', bg = 'gray')
        menu_lbl_frame.grid(sticky = tk.NW, row = 0,column = 0)
        menu_lbl.grid(sticky=tk.NSEW)

        # Clear button
        clear_button_frame = tk.Frame(menu_frame, width = 150, height = 50, padx = 3, bd = 5, highlightbackground = 'gray')
        clear_button_frame.grid_propagate(False)
        clear_button_frame.columnconfigure(0, weight=1)
        clear_button_frame.rowconfigure(0,weight=1)

        clear_button = tk.Button(clear_button_frame, text = 'Clear', command = self.clear_display)
        clear_button_frame.grid(sticky = tk.NW, row = 2,column = 0)
        clear_button.grid(sticky=tk.NSEW)

        # Execute button
        execute_button_frame = tk.Frame(menu_frame, width = 150, height = 50, padx = 3, bd = 5, highlightbackground = 'gray')
        execute_button_frame.grid_propagate(False)
        execute_button_frame.columnconfigure(0, weight=1)
        execute_button_frame.rowconfigure(0,weight=1)

        execute_button = tk.Button(execute_button_frame, text = 'Execute', command = self.execute_from_input)
        execute_button_frame.grid(sticky = tk.NW, row = 3,column = 0)
        execute_button.grid(sticky=tk.NSEW)

        # Show tables button
        show_tables_button_frame = tk.Frame(menu_frame, width = 150, height = 50, padx = 3, bd = 5, highlightbackground = 'gray')
        show_tables_button_frame.grid_propagate(False)
        show_tables_button_frame.columnconfigure(0, weight=1)
        show_tables_button_frame.rowconfigure(0,weight=1)

        show_tables_button = tk.Button(show_tables_button_frame, text = 'Show Tables', command = self.show_tables_and_views)
        show_tables_button_frame.grid(sticky = tk.NW, row = 4,column = 0)
        show_tables_button.grid(sticky=tk.NSEW)

        # Show table information button
        show_tblinfo_button_frame = tk.Frame(menu_frame, width = 150, height = 50, padx = 3, bd = 5, highlightbackground = 'gray')
        show_tblinfo_button_frame.grid_propagate(False)
        show_tblinfo_button_frame.columnconfigure(0, weight=1)
        show_tblinfo_button_frame.rowconfigure(0,weight=1)

        show_tblinfo_button = tk.Button(show_tblinfo_button_frame, text = 'Show Table Info', command = self.show_table_info)
        show_tblinfo_button_frame.grid(sticky = tk.NW, row = 5,column = 0)
        show_tblinfo_button.grid(sticky=tk.NSEW)

        # Demo button
        demo_button_frame = tk.Frame(menu_frame, width = 150, height = 50, padx = 3, bd = 5, highlightbackground = 'gray')
        demo_button_frame.grid_propagate(False)
        demo_button_frame.columnconfigure(0, weight=1)
        demo_button_frame.rowconfigure(0,weight=1)

        demo_button = tk.Button(demo_button_frame, text = 'Demo', command = self.add_demo_data)
        demo_button_frame.grid(sticky = tk.NW, row = 6,column = 0)
        demo_button.grid(sticky=tk.NSEW)

        # Help button
        help_button_frame = tk.Frame(menu_frame, width = 150, height = 50, padx = 3, bd = 5, highlightbackground = 'gray')
        help_button_frame.grid_propagate(False)
        help_button_frame.columnconfigure(0, weight=1)
        help_button_frame.rowconfigure(0,weight=1)

        help_button = tk.Button(help_button_frame, text = 'Help', command = self.get_help)
        help_button_frame.grid(sticky = tk.NW, row = 7,column = 0)
        help_button.grid(sticky=tk.NSEW)

        # About button
        about_button_frame = tk.Frame(menu_frame, width = 150, height = 50, padx = 3, bd = 5, highlightbackground = 'gray')
        about_button_frame.grid_propagate(False)
        about_button_frame.columnconfigure(0, weight=1)
        about_button_frame.rowconfigure(0,weight=1)

        about_button = tk.Button(about_button_frame, text = 'About', command = self.get_about)
        about_button_frame.grid(sticky = tk.NW, row = 8,column = 0)
        about_button.grid(sticky=tk.NSEW)

        # Quit button
        quit_button_frame = tk.Frame(menu_frame, width = 150, height = 50, padx = 3, bd = 5, highlightbackground = 'gray')
        quit_button_frame.grid_propagate(False)
        quit_button_frame.columnconfigure(0, weight=1)
        quit_button_frame.rowconfigure(0,weight=1)

        quit_button = tk.Button(quit_button_frame, text='Quit', command=self.close_app)
        quit_button_frame.grid(sticky = tk.NW, row = 9,column = 0)
        quit_button.grid(sticky=tk.NSEW)


app = SketchQL(width = 1000, height = 600)
app.f.master.title('SketchQL')
app.f.mainloop()
