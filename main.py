#!/usr/bin/python

import db_utils
import html_utils
import sys
import subprocess

# Init
db_utils.create_db()
output = html_utils.json_get_time_all()

#db_utils.get_tasks_info()
html_utils.json_every_task()
html_utils.html_every_task()

# Render to image http://stackoverflow.com/questions/2192799/html-to-image-in-javascript-or-python
subprocess.check_call(['phantomjs', 'generate_image.js', 'html/'])

# Switch
arguments = sys.argv
print arguments
if len(sys.argv) > 1:
    flag = arguments[1]
    print "Flag:" + flag

    if flag == "clear":
        try:
            db_utils.delete_db()
            db_utils.create_db()
        except:
            print "Failed cleaning db"

    elif flag == "add":
        try:
            name = arguments[2]
            db_utils.create_task(name)
        except:
            print "Failed adding task"

    elif flag == "do":
        try:
            name = arguments[2]
            db_utils.do_task(name)
        except:
            print "Failed doing task"

    elif flag == "getlast":
        try:
            if len(sys.argv) > 2:
                name = arguments[2]
                print db_utils.get_last(name)
            else:
                print db_utils.get_last()
        except:
            print "Failed receiving data"
