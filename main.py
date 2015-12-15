import db_utils
import html_utils

import json
__author__ = 'jupiter'

#Cleaning db
#db_utils.delete_db()

#Creating db - adding basic colors
db_utils.create_db()

#Creating task
#db_utils.create_task("dodawanie", "cosinnego")

#Doing task
db_utils.do_task("dodawanie")

output = html_utils.json_get_time()

print output

