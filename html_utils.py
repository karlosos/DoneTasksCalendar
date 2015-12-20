import db_utils

def json_get_time_all(task = None, file = "html/data.json"):
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
    output = ""
    last = len(task_names)-1
    for i, name in enumerate(task_names):
        if i == 0:
            output += "{\r\n"

        if i == last:
            output += "\t" + name + "\r\n"
            output += "}"
        else:
            output += "\t" + name + ",\r\n"

    text_file = open("html/_task_list.json", "w")
    text_file.write(output)
    text_file.close()

def json_every_task():
    tasks = db_utils.get_tasks_info()
    task_names = []
    for task in tasks:
        id = task[0]
        name = task[1]
        short_name = task[2]
        file = "html/"+name+".json"

        task_names.append(name)
        json_get_time_all(name, file)

    json_list_tasks(task_names)
