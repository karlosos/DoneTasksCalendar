import db_utils

import json
__author__ = 'jupiter'


#db_utils.delete_db()

db_utils.create_db()
#db_utils.create_task("dodawanie", "cosinnego")
db_utils.do_task("dodawanie")
#
#db_utils.get_last()
#print db_utils.get_time()
#print "WSZYSTKIE"
#print db_utils.get_time()

db_utils.get_time()

# JSON DUMP
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
        output += "{"

    if i == last:
        output += json_row
        output += "}"
    else:
        output += json_row + ","

print output
text_file = open("data.json", "w")
text_file.write(output)
text_file.close()
