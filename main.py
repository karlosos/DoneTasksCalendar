#!/usr/bin/python

import db_utils
import html_utils
import sys

# Init
db_utils.create_db()
output = html_utils.json_get_time_all()

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
