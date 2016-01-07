#!/usr/bin/env

"""Taskagraph. Track your tasks.

Usage:
  main.py task new <name>...
  main.py task do <name> [--date=<date>]
  main.py task add <name>
  main.py task remove <name>
  main.py color add <color>
  main.py color remove <color>
  main.py last [--task=<name>][--limit=<limit>]
  main.py undo [--task=<name>][--limit=<limit>][--id=<id>]
  main.py clear
  main.py output
  main.py (-h | --help)

Options:
  -h --help     Show this screen.
  --date=<date> Date in format YYYY-MM-DD [default: None].
"""

import docopt
import db_utils

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    print(arguments)
    if arguments['task'] == True:
        name = arguments['<name>']

        if arguments['new'] == True:
            try:
                db_utils.create_task(name[0])
            except:
                print "Failed adding task"

        if arguments['do'] == True:
            try:
                db_utils.do_task(name[0])
            except:
                print "Failed doing task"

    if arguments['clear'] == True:
        try:
            db_utils.delete_db()
            db_utils.create_db()
        except:
            print "Failed cleaning db"
