# Productivity_Report_Generator

## Description

## Table of Contents

## Installation

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
