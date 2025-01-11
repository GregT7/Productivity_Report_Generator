import sys
import os
from gui import launch_gui


# Function: gets the full path of the filename located within
#           the local directory. This is needed for the pyinstaller
#           application to access the default_settings.txt file
# Inputs: str -- the name of the file assuming its in same directory
# Returns: str (full path of filename)
# Side Effects: none
def get_file_path(filename):
    # Get the base path of the executable or script
    if hasattr(sys, '_MEIPASS'):  # PyInstaller creates _MEIPASS during runtime
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, filename)

# Function: extracts default settings values from txt file for
#           the datafile and save location paths + some other info
# Inputs: str - filename of text file containing settings
# Returns: dictionary with keys containing variable names and values
#          containing the data
# Side Effects: accesses and reads text file
def import_settings(filename):
    settings = {}
    with open(filename) as my_file:
        for line in my_file:
            key, value = line.split(" = ")
            settings[key] = value.replace('\n', '')
    return settings

# Function: main function that runs the entire program
# Inputs: none
# Returns: none
# Side Effects: accesses data files, creates a gui, creates graphs,
#               creates and saves pdf file, reads from text file 
if __name__ == "__main__":
    path = get_file_path("default_settings.txt")
    settings = import_settings(path)
    launch_gui(settings)