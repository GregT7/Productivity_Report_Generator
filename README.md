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

## Features
 * GUI
   * Select paths for files containing goal data and productivity data
   * Select directory path to save generated pdf file to
   * Select the date range for filtering data
   * Report generation button
   * Label text updates dynamically to reflect selected files or the success/failure of report generation
   * Modern styling using customtkinter
 * Automatic report generation including three graphs
   * Graphs
     * Productivity Time Spread Heatmap
       * ![productivity_time_spread_heatmap](https://github.com/user-attachments/assets/945a183a-61fa-4afb-9578-a7e630fb39fc)
     * Productivitiy/Goal Differential Heatmap
       * ![productivity_goal_differential_heatmap](https://github.com/user-attachments/assets/41d957b3-6893-41c4-bc48-431370d77464)
     * Performance Totals Bar Chart
       * ![performance_totals_bar_chart](https://github.com/user-attachments/assets/2327df9a-9549-4fb6-b0a7-5475ed496e86)
     * Accepts data in csv or xlsx files
   * Formatted pdf file
     * Saves pdf file with unique name based on naming pattern
     * Inserts and labels graphs
     * Includes time and date information used to filter data
 * Default settings
     * Path values for data files and save location
     * Naming pattern for the pdf files to be saved with
       * As of right now, I am using 'prod_report_spr2025_wX.pdf' as the naming pattern with the 'X' being replaced with the number of weeks passed from the starting_week date
     * Starting week date for calculating the current work week number
       * This is helpful for me because I organize my school content based on the current week of the semester

## Libraries
 - pandas
 - matplotlib
 - seaborn
 - FPDF
 - tkinter
 - customtkinter
 - tkcalendar
 - numpy
