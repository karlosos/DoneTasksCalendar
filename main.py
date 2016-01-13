#!/usr/bin/env

"""Taskagraph. Track your tasks.

Usage:
  main.py <task_name> [--date=<date>]
  main.py task do <task_name>... [--date=<date>]
  main.py task add <task_name>...
  main.py task remove <task_name>...
  main.py color add <color>
  main.py color remove <color>
  main.py last [--task=<task_name>]...[--limit=<limit>]
  main.py undo [--task=<task_name>][--limit=<limit>][--id=<registry_id>]
  main.py clear
  main.py output
  main.py (-h | --help)

Options:
  -h --help     Show this screen.
  --date=<date>         Date in format YYYY-MM-DD [default: None].
  --task=<task_name>    Task name, task shortname or task id
  --limit=<limit>       Options to limit [default: 1]
  --id=<registry_id>    Id of record in registry table
"""

import docopt
import db_utils

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    #print(arguments)
    #print("-----")

    # task command
    if arguments['task'] == True:
        name = arguments['<task_name>']

        if arguments['add'] == True:
            try:
                name_s = name[0]
                #db_utils.create_task(name[0])
                db_utils.create_task(name_s)
            except:
                print "Failed adding task"

        elif arguments['do'] == True:
            try:
                db_utils.do_task(name[0])
            except:
                print "Failed doing task"

        elif arguments['remove'] == True:
            todo = 1

    # color command
    elif  arguments['color'] == True:
        if arguments['add'] == True:
            try:
                todo = 1
            except:
                print "Failed adding task"

        elif arguments['do'] == True:
            try:
                todo = 1
            except:
                print "Failed doing task"

        elif arguments['remove'] == True:
            todo = 1

    # last command
    elif  arguments['last'] == True:
        task = arguments['--task']
        limit = arguments['--limit']

        if len(task) <= 0:
            task = None

        # Validate limit
        try:
            limit = int(limit)
            print limit
        except:
            print "Limit is not a number"
            limit = 3
            print "Limit set to default " + str(limit)

        if task is None:
            # GET ALL TASKS WITH LIMIT
            todo = 1
        else:
            # GET TASKS WITH SPECIFIED TASKIDENTYFICATOR (IT CAN BE TASKNAME, SHORTNAME or ID)
            todo = 1

    # undo command
    elif  arguments['undo'] == True:
        task = arguments['--task']
        limit = arguments['--limit']
        id = arguments['--id']

        if len(task) <= 0:
            task = None

        # Validate limit
        try:
            limit = int(limit)
            print limit
        except:
            print "Limit is not a number"
            limit = 1
            print "Limit set to default " + str(limit)

        if id is None and task is None:
            # Undo tasks (limited) with the newest date
            todo = 1
        elif id is not None:
            # Undo registry with specified id
            todo = 1
        elif task is not None:
            # Undo tasks (limited) with specified name with the newest date
            todo = 1

    # clear command
    elif  arguments['clear'] == True:
        try:
            db_utils.delete_db()
            db_utils.create_db()
        except:
            print "Failed cleaning db"

    # output command
    elif  arguments['output'] == True:
        todo = 1
