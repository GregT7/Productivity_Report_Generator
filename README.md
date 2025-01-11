# Productivity_Report_Generator

## Description
A python program that analyzes productivity and goal data, produces graphs to visualize data, and outputs results to a formatted pdf file using a GUI.

## Installation
1. Clone repository
   ```
   git clone https://github.com/GregT7/Productivity_Report_Generator.git
   ```
2. Install dependencies
   ```
   pip install -r .\requirements.txt
   ```
3. Update default_settings.txt file
   * starting_week - update with date in format '%YYYY-%MM-%DD' for the week number calculation to be based on
      * used in the pdf report text at top of file saying "Week #1" where the "1" is calculated based on the number of weeks passed from the start_date filtering variable
    * prod_path - update with file path of productivity data
    * goal_path - update with file path of goal data
    * save_path - update with directory path where you want the pdf file to be saved to
    * naming_pattern - update with naming pattern
4. Ensure default_settings.txt is in same directory as source code
5. Enter or modify data in productivity/goal data files
6. Run main.py to launch GUI

## Usage
1. Handle data entry and formatting
   * goal and productivity data is entered with the following schema: Date, Subject, Type, Activity, Start, End
      * Date
         * Type: datetime
         * Description: Date has to be in the following format within the csv/xlsx file: YYYY-MM-DD
         * Required: Yes
      * Subject
         * Type: str
         * Description: The general category that the task belongs to - helpful for organizing data, examples: Operating Systems, Data Structures & Algorithms
         * Required: No
      * Type
         * Type: str
         * Description: Subcategory of the general category (subject) that the task belongs to, examples: Homework, Project, Quiz
         * Required: No
      * Activity
         * Type: str
         * Description: The title of the specific task describing what is being worked on or accomplished
         * Required: No
      * Start
         * Type: datetime
         * Description: The time the task is started, must have format of HH:MM PM/AM, examples: 11:30 PM, 1:17 AM
         * Required: Yes 
      * End
         * Type: datetime
         * Description: The time the task is ended, must have format of HH:MM PM/AM, examples: 11:30 PM, 1:17 AM
         * Required: Yes 
      * note: empty or improperly formatted entries in the required data fields will raise a runtime error
   * goal data has at least one entry for each corresponding day that exists in the productivity data selection
   * neither of the files can be empty or improperly formatted for the program to work
2. Validate default_settings.txt contents and storage location
   * contains updated path values
   * starting_week contains a date value stored as a string with no quotation marks separated by '-'
   * contains a naming pattern
   * the text file is stored in the same directory at the same level as the source code
3. Compile and run main.py
   * Select data files and save location or leave blank if using default values
   * Select the data range to filter the data
   * Generate the report
4. Note: Data is collected by hand using a data collection form
## Features
 * GUI
   * Select paths for files containing goal data and productivity data
   * Select directory path to save generated pdf file to
   * Select the date range for filtering data
   * Report generation button
   * Label text updates dynamically to reflect selected files or the success/failure of report generation
   * Modern styling using customtkinter
   * ![gui](https://github.com/user-attachments/assets/d95c0474-c5f6-4bd4-a58c-fd63b2743492)
 * Automatic report generation including three graphs
   * Graphs
     * Accepts data in csv or xlsx files
     * Productivity Time Spread Heatmap
       * ![productivity_time_spread_heatmap](https://github.com/user-attachments/assets/945a183a-61fa-4afb-9578-a7e630fb39fc)
     * Productivitiy/Goal Differential Heatmap
       * ![productivity_goal_differential_heatmap](https://github.com/user-attachments/assets/41d957b3-6893-41c4-bc48-431370d77464)
     * Performance Totals Bar Chart
       * ![performance_totals_bar_chart](https://github.com/user-attachments/assets/2327df9a-9549-4fb6-b0a7-5475ed496e86)
   * Formatted pdf file
      * Saves pdf file with unique name based on naming pattern
      * Inserts and labels graphs
      * Includes time and date information used to filter data
      * ![report_prototype_screenshot](https://github.com/user-attachments/assets/645fcf7c-aa58-456d-aee8-0a7284782765)
   * Default settings
      * Path values for data files and save location
      * Naming pattern for the pdf files to be saved with
      * As of right now, I am using 'prod_report_spr2025_wX.pdf' as the naming pattern with the 'X' being replaced with the number of weeks passed from the starting_week date
      * Starting week date for calculating the current work week number
      * This is helpful for me because I organize my school content based on the current week of the semester
      * ```
        starting_week = 2024-12-30
        prod_path = /Users/Grego/Desktop/Winter_2024/winter2024_TimeData.xlsx
        goal_path = /Users/Grego/Desktop/Winter_2024/goal_data.xlsx
        save_path = /Users/Grego/Desktop
        naming_pattern = prod_report_spr2025_wX.pdf
        ```

## Libraries
 - pandas
 - matplotlib
 - seaborn
 - FPDF
 - tkinter
 - customtkinter
 - tkcalendar
 - numpy
