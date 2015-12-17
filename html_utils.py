import db_utils

def json_get_time_all():
    json_rows = []
    for row in db_utils.get_time():
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
    text_file = open("html/data.json", "w")
    text_file.write(output)
    text_file.close()
    return output