import pandas as pd
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

# Function: filters dataframe data with a date between the start and ending dates
# Inputs: df - dataframe, col_list - list of str, start_date - datetime, end_date - datetime
# Returns: dataframe
# Side Effects: none
def filter_by_daterange(df, col_list, start_date, end_date):
    df = df[col_list]
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Function: creates and formats data within dataframe for graphing a heatmap
# Inputs: df - dataframe, start_date - datetime, end_date - datetime
# Returns: dataframe
# Side Effects: none
def get_heatmap(df, start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    heatmap = pd.DataFrame(date_range, columns=["Date"])
    heatmap['Day_Name'] = heatmap['Date'].dt.day_name()
    heatmap['Work_Duration'] = [np.zeros(24, dtype=int) for _ in range(len(heatmap))]

    col_list = ['Day_Name', 'Date', 'Start', 'End']

    df = filter_by_daterange(df, col_list, start_date, end_date)

    for _, row in df.iterrows():
        start = row['Start']
        end = row['End']

        if isinstance(start, pd.Timestamp) and isinstance(end, pd.Timestamp):
            distribute_time_by_hour(heatmap, row, start, end)
            
    return heatmap

# Function: calculates the amount of time spent working within a strict 60 minute period
#           and formats the data within the dataframe based on calculation
# Inputs: heatmap - df, row - pandas series, start - pandas timestamp, end - pandas timestamp 
# Returns: none
# Side Effects: modifies the heatmap dataframe passed in
def distribute_time_by_hour(heatmap, row, start, end):
    day = row['Day_Name']
    same_day = heatmap.index[heatmap['Day_Name'] == day][0]
    time_list = heatmap.at[same_day, 'Work_Duration']

    if end.hour == start.hour:
        time_list[end.hour] += end.minute - start.minute
    else:
        time_list[start.hour] += 60 - start.minute
        time_list[start.hour + 1:end.hour] += 60
        time_list[end.hour] += end.minute

    heatmap.at[same_day, 'Work_Duration'] = time_list

# Function: adds ytick values to heatmap graphs with hours of the day
# Inputs: df - dataframe, col_name - str
# Returns: dataframe
# Side Effects: none
def add_hour_labels(df, col_name):
    hour_labels = []
    pattern = [12] + list(range(1, 12))
    for _ in range(2): hour_labels.extend(pattern)

    for i in range(12):
        hour_labels[i] = str(hour_labels[i]) + " AM"
        hour_labels[i+12] = str(hour_labels[i+12]) + " PM"

    return pd.DataFrame(df[col_name].tolist(), columns=hour_labels)

# Function: adds xtick values to heatmap graphs with days of the week
# Inputs: df - dataframe, work_duration_df - dataframe
# Returns: dataframe
# Side Effects: none
def add_date_labels(df, work_duration_df):
    df['Short_Date'] = df['Date'].dt.strftime('%m-%d') # Extract only the month and day
    df['Day_Name'] = df['Day_Name'].apply(lambda string: string[0:3])
    work_duration_df['Day_Name'] = df['Day_Name'] + ' ' + df['Short_Date'] # Combine with Day_Name
    work_duration_df.set_index('Day_Name', inplace=True) # Set Day_Name as the index
    return work_duration_df.transpose()

# Function: sets up configurations for the productivity heatmap graph
# Inputs: df - dataframe, ax - matplotlib axes, cmap - list
# Returns: none
# Side Effects: modifies fig and ax
def setup_productivity_figure(df, ax, cmap):
    xtick_df = add_hour_labels(df, "Work_Duration")
    xytick_df = add_date_labels(df, xtick_df)

    # Create a custom annotation array, leaving blanks for NaN values
    annot_array = xytick_df.to_numpy()
    annot_mask = np.where(annot_array == 0, "", annot_array)  # Replace 0 with an empty string

    # # Plot the heatmap
    # plt.figure(figsize=(12, 8))
    sns.heatmap(
        xytick_df,  # Use masked DataFrame for visualization
        ax=ax,
        annot=annot_mask,         # Pass the custom annotation mask
        cmap=cmap, # "YlGnBu"
        fmt='',                   # Avoid formatting issues (let Seaborn handle this internally)
        cbar_kws={'label': 'Work Duration (minutes)'},
        linewidth=0.5,
        linecolor='black'
    )

# Function: plots the productivity heatmap figure
# Inputs: fig - matplotlib fig, ax - matplotlib ax, df - dataframe
# Returns: none
# Side Effects: modifies fig and ax
def plot_prod_fig(fig, ax, df):
    setup_productivity_figure(df, ax, "YlGnBu")

    # Customize the plot
    ax.set_title('Productivity Time Spread Heatmap')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Hour of the Day')
    plt.setp(ax.get_xticklabels(), rotation=0)
    plt.setp(ax.get_yticklabels(), rotation=0)

    fig.tight_layout()


# Function: creates new dataframe that calculates the difference in time values between the
#           passed dataframes
# Inputs: df1 - dataframe, df2 - dataframe 
# Returns: dataframe
# Side Effects: none
def calc_delta_heatmap(df1, df2):
    combined = pd.merge(df1, df2, on="Date")
    combined['Work_Duration'] = combined['Work_Duration_x'] - combined['Work_Duration_y']

    combined.drop(columns=['Work_Duration_x', 'Work_Duration_y', 'Day_Name_y'], inplace=True)
    combined.rename(columns={'Day_Name_x':'Day_Name'}, inplace=True)

    return combined

# Function: modifies the color intensity/strength based on how close the time value
#           for the hour was to 60 mins with stronger/lighter colors being closer/farther away
#           from 60 mins
# Inputs: color_value - float, delta_duration - int
# Returns: float
# Side Effects: none
def normalize_color(color_value, delta_duration):
    if color_value in [1, 5]:
        return color_value + (0.45 - 0.45 * abs(delta_duration) / 60.0)
    elif color_value == 3:
        return color_value + (0.2 - 0.2 * abs(delta_duration) / 60.0)
    else:
        return color_value

# Function: categorizes the heatmap cell and returns a float value corresponding to the
#           category
# Inputs: goal - int, prod - int
# Returns: int
# Side Effects: none 
def calc_colorval(goal, prod):
    color_val = 0

    if goal > 0 and prod < goal:
        color_val = 1 # Did not follow plan
    elif goal > 0 and prod >= goal:
        color_val = 3 # Followed plan
    elif goal == 0 and prod > 0:
        color_val = 5 # Exceeded plan expectations
    elif goal == 0 and prod == 0:
        color_val = 6 # No plan + no work

    return color_val

# Function: creates dataframe storing the category/color values for the
#           delta heatmap
# Inputs: g_df - dataframe, p_df - dataframe
# Returns: dataframe
# Side Effects: none
def delta_categorization(g_df, p_df):
    combined = pd.merge(g_df, p_df, on="Date")
    categories = g_df[['Date', 'Day_Name']]
    categories['Eval_Categories'] = None

    date_to_categories = {}

    for _, row in combined.iterrows():
        goal_np = row['Work_Duration_x']
        prod_np = row['Work_Duration_y']
        date = row['Date']

        category_np = np.zeros(goal_np.shape, dtype=float)

        for i in range(goal_np.shape[0]):
            color_val = calc_colorval(goal_np[i], prod_np[i])
            category_np[i] = normalize_color(color_val, prod_np[i] - goal_np[i])
        
        date_to_categories[date] = category_np
        
    categories['Eval_Categories'] = categories['Date'].map(date_to_categories)

    return categories

# Function: extracts data from csv or xlsx file and puts into dataframe
# Inputs: path - str
# Returns: dataframe
# Side Effects: opens csv/xlsx file
def datetime_preprocessing(path):
    if ".csv" in path:
        df = pd.read_csv(path)
        df['Start'] = pd.to_datetime(df['Start'], format='%I:%M %p')
        df['End'] = pd.to_datetime(df['End'], format='%I:%M %p')
    elif ".xlsx" in path:
        df = pd.read_excel(path)
        df['Start'] = pd.to_datetime(df['Start'], format='%H:%M:%S')
        df['End'] = pd.to_datetime(df['End'], format='%H:%M:%S')
    else:
        df = pd.DataFrame()

    df['Date'] = pd.to_datetime(df['Date'])
    df['Day_Name'] = df['Date'].dt.day_name()

    return df

# Function: sets up the deltaheatmap figure
# Inputs: ax - matplotlib axes, df - dataframe
# Returns: none
# Side Effects: modifies ax 
def setup_performance_figure(ax, df):
    color_xtick_df = add_hour_labels(df, 'Eval_Categories')
    color_xytick_df = add_date_labels(df, color_xtick_df)

    work_xtick_df = add_hour_labels(df, 'Work_Duration')
    work_xytick_df = add_date_labels(df, work_xtick_df)

    # Create a custom annotation array, leaving blanks for NaN values
    annot_array = work_xytick_df.to_numpy()
    annot_mask = np.where((annot_array == 0) & (color_xytick_df.to_numpy() == 6), "", annot_array)

    colors = ["#a10202", "white", "green", "white", "orange", "white"]
    cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

    sns.heatmap(
        color_xytick_df,  # Use masked DataFrame for visualization
        ax=ax,
        annot=annot_mask,         # Pass the custom annotation mask
        cmap=cmap,
        fmt='',                   # Avoid formatting issues (let Seaborn handle this internally)
        cbar=False,
        linewidth=0.5,
        linecolor='black'
    )

# Function: plots the performance heatmap
# Inputs: fig - matplotlib figure, ax - matplotlib axes, performance_heatmap - dataframe
# Returns: none
# Side Effects: modifies fig, ax
def plot_performance_heatmap(fig, ax, performance_heatmap):
    # setup figure for plotting
    setup_performance_figure(ax, performance_heatmap)

    # Create custom legend labels
    legend_labels = [
        mpatches.Patch(facecolor='green', edgecolor='black', label='Followed Plan'),
        mpatches.Patch(facecolor='orange', edgecolor='black', label='Unplanned Work'),
        mpatches.Patch(facecolor='#a10202', edgecolor='black', label='Did Not Follow Plan'),
        mpatches.Patch(facecolor='white', edgecolor='black', label='No Plan & No Work'),
    ]

    # Add the custom legend
    ax.legend(handles=legend_labels, title="Legend", bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.5)

    ax.set_title('Productivitiy/Goal Differential Heatmap')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Hour of the Day')
    plt.setp(ax.get_xticklabels(), rotation=0)
    plt.setp(ax.get_yticklabels(), rotation=0)

    fig.tight_layout()

# Function: calculates summed up productive and goal time for plotting bar chart
# Inputs: prod_df - dataframe, goal_df - dataframe, start_date - datetime, end_date - datetime
# Returns: dataframe 
# Side Effects: none
def calc_summary_df(prod_df, goal_df, start_date, end_date):
    filter_cols = ['Day_Name', 'Date', 'Start', 'End', 'Time']
    prod_df = filter_by_daterange(prod_df, filter_cols, start_date, end_date)
    goal_df = filter_by_daterange(goal_df, filter_cols, start_date, end_date)

    total_prod_time = prod_df.groupby(['Date', 'Day_Name']).agg({'Time':'sum'}).reset_index()
    total_goal_time = goal_df.groupby(['Date', 'Day_Name']).agg({'Time':'sum'}).reset_index()
    
    combined = pd.merge(total_prod_time, total_goal_time, on=['Date','Day_Name'])
    combined.rename(columns={'Time_x':'Prod_Time', 'Time_y':'Goal_Time'}, inplace=True)

    combined['Delta_Time'] = combined['Prod_Time'] - combined['Goal_Time']

    return combined

# Function: plots the bar chart detailing the time sums based on the day
# Inputs: fig - matplotlib figure, matplotlib - axes, sum_data - dataframe 
# Returns: none
# Side Effects: modifies fig and ax 
def plot_sum_data(fig, ax, sum_data):
    sum_data['Short_Date'] = sum_data['Date'].dt.strftime('%m-%d') # Extract only the month and day
    sum_data['Short_Date'] = sum_data['Day_Name'] + ' ' + sum_data['Short_Date']
    sum_data.set_index('Short_Date', inplace=True)

    sum_data.drop(columns=['Day_Name', 'Date'], inplace=True)

    colors = ['#12263a', '#06bcc1', '#c5d8d1']
    bars = sum_data.plot(kind='bar', ax=ax, color=colors)

    for bar in bars.patches:
        # Get the height of each bar
        height = bar.get_height()
        # Add the label above the bar
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, str(round(height, 2)), 
                ha='center', va='bottom', fontsize=10)

    ax.set_title('Performance Totals Bar Chart')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Time (mins)')
    ax.set_xticklabels(sum_data.index, rotation=0)

    fig.tight_layout()

# Function: prepares graphs and returns a dictionary containing the fig/ax data
# Inputs: prod_path - str, goal_path - datetime, start_date - datetime, end_date - datetime
# Returns: dict
# Side Effects: opens csv/xlsx file
def prepare_graphs(prod_path, goal_path, start_date, end_date):
    # import data from csv files into dataframes
    # productivity data is the recorded data that I take when I work
    # goal data is the time periods when I want to work given a series of specific dates
    productivity_event = datetime_preprocessing(prod_path)
    goal = datetime_preprocessing(goal_path)

    goal['Time'] = (goal['End'] - goal['Start']).dt.total_seconds() / 60

    # format dataframes for creating a heatmap graph for goal and prod data
    p_heatmap = get_heatmap(productivity_event, start_date, end_date)
    g_heatmap = get_heatmap(goal, start_date, end_date)

    # create performance heatmap that is calculated by subtracting goal data from prod data
    # and categorize datapoints for coloring
    pg_df = calc_delta_heatmap(p_heatmap, g_heatmap)
    delta_categories = delta_categorization(g_heatmap, p_heatmap)
    performance_heatmap = pd.merge(pg_df, delta_categories, on=['Date','Day_Name'])

    # some plotting prep
    figs = {}
    figs['productivity_figure'], ax1 = plt.subplots(figsize=(8,6))
    figs['performance_figure'], ax2 = plt.subplots(figsize=(10,8))
    figs['totals_figure'], ax3 = plt.subplots(figsize=(9,7))

    graphs = {}
    graphs['productivity_graph'] = [figs['productivity_figure'], ax1]
    graphs['performance_graph'] = [figs['performance_figure'], ax2]
    graphs['totals_graph'] = [figs['totals_figure'], ax3]

    plot_prod_fig(figs['productivity_figure'], ax1, p_heatmap)

    # plot performance graphs
    plot_performance_heatmap(figs['performance_figure'], ax2, performance_heatmap)

    sum_data = calc_summary_df(productivity_event, goal, start_date, end_date)
    plot_sum_data(figs['totals_figure'], ax3, sum_data)

    return graphs

prod_path = '/Users/Grego/Desktop/Winter_2024/winter2024_TimeData.xlsx'
goal_path = '/Users/Grego/Desktop/Winter_2024/goal_data.xlsx'
prepare_graphs(prod_path, goal_path, '2024-12-30', '2025-01-05')
plt.show()