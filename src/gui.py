import customtkinter as ctk
from matplotlib import pyplot as plt
from datetime import datetime, date, timedelta
from tkinter import filedialog
from tkcalendar import DateEntry
import automated_report as report


# Function: calculates the number of weeks passed since the date
#           stored within the starting_week argument
# Inputs: starting_week - str, start_date - datetime.date
# Returns: str
# Side Effects: none
def calc_week_num(starting_week, start_date):
    starting_week = datetime.strptime(starting_week, '%Y-%m-%d').date()
    delta = (start_date - starting_week).days
    return str(int(delta / 7) + 1)

# Function: extracts only the filename from a given path
# Inputs: file_str - str
# Returns: str
# Side Effects: none
def format_file_text(file_str):
    if "/" not in file_str:
        return file_str
    else:
        ind = file_str.rfind("/") + 1
        return file_str[ind:]

# Function: Returns dictionary containing the default start and end date
#           values that will populate the DateEntry widgets. The default values
#           are always on Mondays and Sundays
# Inputs: none
# Returns: dictionary - contains start/end date values for the year, month, and day
# Side Effects: none
def get_default_dates():
    today = date.today()
    day_n = today.weekday()

    s_days = 6 if day_n == 6 else day_n + 7
    e_days = day_n + 1

    start_date = today - timedelta(days=s_days)
    end_date = today - timedelta(days=e_days)

    dates = {}
    dates['start'] = {'y': start_date.year, 'm': start_date.month, 'd': start_date.day}
    dates['end'] = {'y': end_date.year, 'm': end_date.month, 'd': end_date.day}

    return dates

# Function: creates a title, label, and button widget then packages them together
# Inputs: root - CTk object, path - str, title_text - str, label_str - str, button_text - str,
#         func - str, frow - int, fcol - int
# Returns: CustomButton object
# Side Effects: creates a new object and modifies the tkinter main app window by populating
#               the frame with a new widget and labels
def create_CustomButton(root, path, title_text, label_str, button_text, func, frow, fcol):
    title = ctk.CTkLabel(root, text=title_text, font=("Verdana", 18))
    title.grid(row=frow, column=fcol, pady=(10,0), padx=20, columnspan=2)

    label = ctk.CTkLabel(root, text=label_str, font=("Verdana", 12))
    label.grid(row=frow+1, column=fcol, pady=(0,3), columnspan=2)

    file_button = CustomButton(title, ctk.CTkButton(root, text=button_text, font=("Verdana", 12)), label)

    if func == "select":
        file_button.configure_button_select()
    elif func == "save":
        file_button.configure_button_save()
    elif callable(func):
        file_button.configure_button(func)

    file_button.button.grid(row=frow + 2, column=fcol, columnspan=2)
    file_button.fpath = path if path else ''

    return file_button


# Class: holds together a button widget and associated labels for easy
#        access and manipulation, useful for dynamically changing labels based
#        on the state of the application process
# Side Effects: configures button widgets with different functions and updates label
#               text, also opens file explorer to select save locations and different datafile
#               paths
class CustomButton:
    # Function: instantiates button with a title, button, and label
    # Inputs: title - ctk.CTkLabel, button - ctk.CTkButton, label - ctk.CTkLabel
    # Returns: none
    # Side Effects: instantiates CustomButton object
    def __init__(self, title, button, label):
        self.fpath = ""
        self.title = title
        self.button = button
        self.text = ""
        self.label = label
        
    # Function: configures button with the select file function so that
    #           the path str returned by the window explorer selection can
    #           be saved and so that the label text can be updated dynamically
    # Inputs: none
    # Returns: none
    # Side Effects: modifies function of button
    def configure_button_select(self):
        self.button.configure(command=lambda: self.select_file(self.label))

    # Function: configures button with the save file function that saves the path of
    #           the desired save location
    # Inputs: none
    # Returns: none
    # Side Effects: modifies function of button
    def configure_button_save(self):
        self.button.configure(command=lambda: self.get_save_location())

    # Function: configures button with function to generate the report based on the data
    #           collected by the input field widgets
    # Inputs: sdate - datetime.date, edate - datetime.date, wno - str, sloc - str, ppath - str
    #         gpath - str, npattern - str
    # Returns: none
    # Side Effects: modifies function of button
    def configure_report_button(self, sdate, edate, wno, sloc, ppath, gpath, npattern):
        self.button.configure(command=self.generate_report(sdate, edate, wno, sloc, ppath, gpath, npattern))

    # Function: opens window explorer and allows user to select a file, returning its path
    #           and modifying the label to display the currently selected file name
    # Inputs: label - ctk.CTkLabel
    # Returns: none
    # Side Effects: updates fpath and label widget's text value, also opens file explorer
    def select_file(self, label):
        temp_path = filedialog.askopenfilename()
        if temp_path:
            self.fpath = temp_path
            self.label.configure(text=f"Selected file: {format_file_text(self.fpath)}")
        
        if not self.fpath:
            self.label.configure(text="No path selected")

    # Function: selects save file location for the report to be generated
    # Inputs: none
    # Returns: none
    # Side Effects: opens file explorer, modifies fpath, changes label widget text value
    def get_save_location(self):
        temp_path = filedialog.askdirectory(title="Select Folder")
        if temp_path:
            self.fpath = temp_path
            self.label.configure(text=f"Save location: {format_file_text(self.fpath)}")

        if not self.fpath:
            self.label.configure(text="No save location selected")

# Class: packages together tkinter widgets and labels for date range selection
# Side Effects: none
class CustomDateEntry:
    # Function: instantiates CustomDateEntry object
    # Inputs: title - ctk.CTkLabel, st_label - ctk.CTkLabel, st_ds - DateEnry, ed_label - ctk.CTkLabel,
    #         ed_ds - DateEntry 
    # Returns: none
    # Side Effects: creates a new object
    def __init__(self, title, st_label, st_ds, ed_label, ed_ds):
        self.title = title
        self.start_label = st_label
        self.start_ds = st_ds
        self.end_label = ed_label
        self.end_ds = ed_ds
        
# Function: sets up date selection widgets and labels while populating the widgets
#           with default values
# Inputs: root - CTk object, frow - int, fcol - int
# Returns: CustomDateEntry object
# Side Effects: creates new labels and widgets, modifies main app window
def setup_date_select(root, frow, fcol):
    default_dates = get_default_dates()

    date_selector_label = ctk.CTkLabel(root, text="Date Range Selection", font=("Verdana", 18))
    date_selector_label.grid(row=frow, column=fcol, pady=(10,0), columnspan=2)

    # Label for the start date
    start_label = ctk.CTkLabel(root, text="Start Date:")
    start_label.grid(row=frow + 1, column=fcol, padx=10)

    # Create a DateEntry widget for the start date
    start_date = DateEntry(
        root,
        year=default_dates['start']['y'],
        month=default_dates['start']['m'],
        day=default_dates['start']['d'],
        width=12, date_pattern="yyyy-mm-dd", font=("Verdana", 10)
    )
    start_date.grid(row=frow + 2, column=fcol, padx=10)

    # Label for the end date
    end_label = ctk.CTkLabel(root, text="End Date:")
    end_label.grid(row=frow + 1, column=fcol + 1, padx=10)

    # Create a DateEntry widget for the end date
    end_date = DateEntry(
        root,
        year=default_dates['end']['y'],
        month=default_dates['end']['m'],
        day=default_dates['end']['d'],
        width=12, date_pattern="yyyy-mm-dd", font=("Verdana", 10)
    )
    end_date.grid(row=frow+2, column=fcol + 1, padx=10)
    return CustomDateEntry(date_selector_label, start_label, start_date, end_label, end_date)

    # Inputs: sdate - 
    #         
# Function: Handles the automatic generation of the report. This function is needed so that the
#           the input values from the buttons can be dynamically extracted and passed to the report
#           generation function
# Inputs: cbutton - CustomButton, sdate - datetime.date, edate - datetime.date, wno - str, sloc - str, 
#         ppath - str, gpath - str, npattern - str
# Returns: none
# Side Effects: creates and saves new pdf file, updates label text
def handle_report_gen(cbutton, sdate, edate, wno, sloc, ppath, gpath, npattern):
    update_str = report.generate_report(sdate, edate, wno, sloc, ppath, gpath, npattern)
    cbutton.label.configure(text=update_str)

# Function: sets up a CustomButton for report generation
# Inputs: root - CTk object, settings - dict, date_sel - CustomDateEntry, paths - dict, frow - int,
#         fcol - int
# Returns: CustomButton
# Side Effects: modifies main application window, creates and saves pdf file
def setup_report_button(root, settings, date_sel, paths, frow, fcol):
    report_title = ctk.CTkLabel(root, text="Generate Report", font=("Verdana", 18))
    report_title.grid(row=frow, column=fcol, pady=(10,0), columnspan=2)

    report_label = ctk.CTkLabel(root, text="No Issues", font=("Verdana", 12))
    report_label.grid(row=frow + 1, column=fcol, pady=(0,3), columnspan=2)

    report_button = CustomButton(report_title, ctk.CTkButton(root, text="Generate", font=("Verdana", 12)), report_label)
    report_button.button.grid(row=frow + 2, column=fcol, pady=(0,10), columnspan=2)
    report_button.button.configure(command=lambda: handle_report_gen(
        report_button,
        date_sel.start_ds.get_date(),
        date_sel.end_ds.get_date(),
        calc_week_num(settings['starting_week'], date_sel.start_ds.get_date()),
        paths['save_path'],
        paths['prod_path'],
        paths['goal_path'],
        settings['naming_pattern'])
    )
    return report_button

# Function: launches gui where user can select productivity data, goal data, and a save location + generate a pdf file
# Inputs: settings - dict
# Returns: none
# Side Effects: launches gui, creates pdf file, reads in data files 
def launch_gui(settings):
    root = ctk.CTk()
    root.title("Automated Productivity Report GUI")

    title_text = "Productivity Data Selection"
    prod_str = f"Selected file: {format_file_text(settings['prod_path'])}"
    pselButton = create_CustomButton(root, settings['prod_path'], title_text, prod_str, "Select File", "select", 0, 0)

    title_text = "Goal Data Selection"
    goal_str = f"Selected file: {format_file_text(settings['goal_path'])}"
    gselButton = create_CustomButton(root, settings['goal_path'], title_text, goal_str, "Select File", "select", 3, 0)

    date_sel = setup_date_select(root, 6, 0)

    title_text = "Save Location Selection"
    save_str = f"Selected location: {format_file_text(settings['save_path'])}"
    sselButton = create_CustomButton(root, settings['save_path'], title_text, save_str, "Select location", "save", 9, 0)

    paths = {'prod_path': pselButton.fpath, 'goal_path': gselButton.fpath, "save_path": sselButton.fpath}
    report_button = setup_report_button(root, settings, date_sel, paths, 12, 0)

    root.mainloop()
