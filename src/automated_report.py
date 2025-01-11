from fpdf import FPDF
import productivity_graphs as graph
from datetime import datetime
import matplotlib.pyplot as plt
import io, tempfile, os

# Function: adds a graph to the pdf file with a title and description
# Inputs: pdf - fpdf.fpdf.FPDF, graph_dict - dict, title_dict - dict, desc_dict - dict
# Returns: r_dict - dict
# Side Effects: modifies the pdf object
def add_graph(pdf, graph_dict, title_dict, desc_dict):
    fig = graph_dict['fig']
    ax = graph_dict['ax']

    img_stream = io.BytesIO()
    fig.savefig(img_stream, format='png')
    img_stream.seek(0)  # Reset the stream position to the beginning
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        # Write the BytesIO content to the temp file
        temp_file.write(img_stream.getvalue())
        temp_file_path = temp_file.name
    
    pdf.set_font("Tahoma", size=title_dict['size'], style="")
    pdf.set_xy(title_dict['x'], title_dict['y'])  # Set x to 10 and y to 20 (adjust as needed)
    pdf.cell(0, 0, title_dict['title'], ln=True, align="L")
    
    pdf.image(temp_file_path, x=graph_dict['x'], y=graph_dict['y'],
    w=graph_dict['w'], h=graph_dict['h'])
    plt.close(fig)

    pdf.set_font("Times", size=desc_dict['size'])
    pdf.set_xy(desc_dict['x'], desc_dict['y'])
    pdf.cell(0, 0, desc_dict['description'], ln=True, align="L")

    r_dict = {'tpath': temp_file_path, 'height': 185}
    return r_dict

# Function: adds fonts to be used in the pdf file
# Inputs: pdf - fpdf.fpdf.FPDF
# Returns: none
# Side Effects: modifies the pdf object
def load_fonts(pdf):
    pdf.add_font('Tahoma', '', 'C:/Windows/Fonts/tahoma.ttf', uni=True)  # Regular
    pdf.add_font('Tahoma', 'B', 'C:/Windows/Fonts/tahomabd.ttf', uni=True)  # Bold (Optional)
    pdf.add_font('Times', '', 'C:/Windows/Fonts/times.ttf', uni=True)  # Regular
    pdf.add_font('Times', 'B', 'C:/Windows/Fonts/times.ttf', uni=True)  # Bold (Optional)

# Function: adds the title of the document and details the date range the calcs are based on
# Inputs: pdf - fpdf.fpdf.FPDF, start_date - str, end_date - str, week_no - str
# Returns: none
# Side Effects: modifies pdf object
def add_title(pdf, start_date, end_date, week_no):
    pdf.set_font("Tahoma", size=14, style="B")
    pdf.set_xy(0, 10)  # Set x to 10 and y to 20 (adjust as needed)
    pdf.cell(0, 0, "Weekly Productivity Report", ln=True, align="C")

    pdf.set_font("Times", size=12)
    week_str = "Week #" + week_no + ": " + start_date + " --- " + end_date
    pdf.set_xy(0, 18)  # Set x to 10 and y to 20 (adjust as needed)
    pdf.cell(0, 0, week_str, ln=True, align="C")

    pdf.set_xy(0, 26)  # Set x to 10 and y to 20 (adjust as needed)

    # time_12_hour = time_obj.strftime("%I:%M %p")
    pdf.cell(0, 0, f"Generated On: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}", ln=True, align="C")

# Function: removes temp files created to save graph images
# Inputs: lst - list of str containing paths of files to remove
# Returns: none
# Side Effects: deletes temporary files
def remove_temp_files(lst):
    for path in lst:
        os.remove(path)

# Function: creates and saves the file after generating the graphs created from the data files
# Inputs: start_date - datetime.date, end_date - datetime.date, week_no - str, save_loc - str, prod_path - str
#         goal_path - str, naming_pattern - str
# Returns: str - status of report generation (success or the error produced)
# Side Effects: creates pdf file and saves to save location
def generate_report(start_date, end_date, week_no, save_loc, prod_path, goal_path, naming_pattern):
    try:
        # Create PDF instance
        pdf = FPDF()
        pdf.add_page()
        load_fonts(pdf)

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        sd = start_date.strftime("%A, %B %d, %Y")
        ed = end_date.strftime("%A, %B %d, %Y")
        add_title(pdf, sd, ed, week_no)

        graphs = graph.prepare_graphs(prod_path, goal_path, start_date, end_date)
        temp_paths = []
        height = 125

        title_dict = {'title': 'Productive Time Heatmap', 'x':16, 'y':35, 'size':12}
        graph_dict = {'x': 20, 'y': 38, 'w':190, 'h':height,
                      'fig': graphs['productivity_graph'][0],
                      'ax':graphs['productivity_graph'][1]
        }

        ypos = 38 + height
        description = "Figure #1: Total time spent working by each hour of the day for the week."
        desc_dict = {'description': description, 'x': 16, 'y':ypos, 'size':12}
        r_dict = add_graph(pdf, graph_dict, title_dict, desc_dict)
        temp_paths.append(r_dict['tpath'])

        ypos += 8
        title_dict = {'title': 'Productivitiy/Goal Differential Heatmap', 'x':16, 'y':ypos, 'size':12}
        ypos += height + 3
        graph_dict = {'x': 20, 'y': 175, 'w':190, 'h':height-15,
                      'fig': graphs['performance_graph'][0],
                      'ax':graphs['performance_graph'][1]
        }
        description = "Figure #2: Summed productive time – goal productive time by the hour"
        description += " displaying how close my work"
        ypos += height + 8
        desc_dict = {'description': description, 'x': 16, 'y':375, 'size':12}
        r_dict = add_graph(pdf, graph_dict, title_dict, desc_dict)
        temp_paths.append(r_dict['tpath'])

        desc2 = "performance was to the planned schedule."
        pdf.set_xy(16, 16)
        pdf.cell(0, 0, desc2, ln=True, align="L")


        title_dict = {'title': 'Performance Totals Bar Chart', 'x':16, 'y':24, 'size':12}
        graph_dict = {'x': 20, 'y': 28, 'w':180, 'h':height,
                      'fig': graphs['totals_graph'][0],
                      'ax':graphs['totals_graph'][1]
        }
        description = "Figure #3: Alternative view to performance heatmap where the total goal and productive times are"
        desc_dict = {'description': description, 'x': 16, 'y':155, 'size':12}
        r_dict = add_graph(pdf, graph_dict, title_dict, desc_dict)
        temp_paths.append(r_dict['tpath'])

        desc2 = "visualized alongside the difference between the two for each day of the week."
        pdf.set_xy(16, 161)
        pdf.cell(0, 0, desc2, ln=True, align="L")
        
        file_name = naming_pattern.replace('X', week_no)
        path = save_loc + "/" + file_name
        pdf.output(path)

        remove_temp_files(temp_paths)
        return "PDF report generated successfully!"

    except Exception as e: return(str(e))
