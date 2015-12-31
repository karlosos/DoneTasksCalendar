import db_utils
import subprocess

"""
JSON FUNCTIONS
"""
def json_get_time_all(task = None, file = "html/_data.json"):
    """
    Write json output of specified task to specified file
    Get output for last 365 days
    If no parameters are given then it get output for all tasks and save it to default location
    :param task: name, shortname or id of task
    :param file: path to output file
    :return: return json output aswell
    """
    json_rows = []
    if task is None:
        db_result = db_utils.get_time()
    else:
        db_result = db_utils.get_time(task)
    for row in db_result:
        timestamp = str(row[0])
        count = str(row[1])
        json_row = '"' + timestamp + '"' + ":" + count
        json_rows.append(json_row)

    last = len(json_rows)-1
    output = ""
    for i, json_row in enumerate(json_rows):
        if i == 0:
            output += "{\r\n"

        if i == last:
            output += "\t" + json_row + "\r\n"
            output += "}"
        else:
            output += "\t" + json_row + ",\r\n"

    text_file = open(file, "w")
    text_file.write(output)
    text_file.close()
    return output

def json_list_tasks(task_names):
    """
    Write json list of tasks to file. Must have given array of tasks names
    :param task_names: array of tasksnames
    :return:
    """
    output = ""
    output += "{\r\n\t\"tasks\": [\r\n"
    output += "\t\t\"" + "data" + "\",\r\n"
    last = len(task_names)-1
    for i, name in enumerate(task_names):

        if i == last:
            output += "\t\t\"" + name + "\"\r\n"
            output += "\t] \r\n}"

        else:
            output += "\t\t\"" + name + "\",\r\n"

    text_file = open("html/_task_list.json", "w")
    text_file.write(output)
    text_file.close()

def json_every_task():
    """
    Write json output of all tasks to individual files
    :return:
    """
    tasks = db_utils.get_tasks_info()
    task_names = []
    for task in tasks:
        name = task[1]
        file = "html/_"+name+".json"

        task_names.append(name)
        json_get_time_all(name, file)

    json_get_time_all()     # Create _data.json file
    json_list_tasks(task_names)

"""
HTML FUNCTIONS
"""
def html_every_task():
    """
    Iterate through every tasks and use html_task(task) to create html output
    :return:
    """
    tasks = db_utils.get_tasks_info()
    task_names = []
    for task in tasks:
        name = task[1]
        color_id = task[3]
        color = db_utils.get_color(color_id)
        print color
        task_names.append(name)
        html_task(name, color)

    html_task("data")

def html_task(task, color=None):
    """
    Write html output for specified task
    :param task: it must be a name of a task. NOT short_name of id!
    :return:
    """
    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <script src="src/d3.min.js"></script>
        <link rel="stylesheet" href="src/cal-heatmap.css" />
        <script type="text/javascript" src="src/cal-heatmap.min.js"></script>
        <script type="text/javascript" src="jquery-2.1.4.min.js"></script>
      </head>
      <body>
    """
    html += "<h2>"+task+"</h2><div id='"+task+"'></div>"
    html += "<script>"
    if color is None:
        html +=  """
        var date = new Date(new Date().setYear(new Date().getFullYear() - 1));
        new CalHeatMap().init({
                 start: date,
                 itemSelector: \"#"""+task+"""\",
                 range: 13,
                 data: \"_"""+task+""".json",
                 dataType: \"json\",
                 domain: \"month\",
                 subDomain: \"day\"
               }); """
        html += "</script>"
        html += """
        </body>
        </html>
        """
    else:
        html +=  """
        var date = new Date(new Date().setYear(new Date().getFullYear() - 1));
        new CalHeatMap().init({
                 start: date,
                 itemSelector: \"#"""+task+"""\",
                 range: 13,
                 data: \"_"""+task+""".json",
                 dataType: \"json\",
                 domain: \"month\",
                 subDomain: \"day\",
                 legendColors: [\""""+color+"""\", \""""+color+"""\"]
               }); """
        html += "</script>"
        html += """
        </body>
        </html>
        """
    text_file = open("html/_"+task+".html", "w")
    text_file.write(html)
    text_file.close()

def update_output():
    # Init
    db_utils.create_db()

    #db_utils.get_tasks_info()
    json_every_task()
    html_every_task()

    # Render to image http://stackoverflow.com/questions/2192799/html-to-image-in-javascript-or-python
    subprocess.check_call(['phantomjs', 'generate_image.js', 'html/'])