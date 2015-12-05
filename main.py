from datetime import date, datetime
import random

__author__ = 'jupiter'

import sqlite3
import os

PATH = os.path.expanduser('~/.taskgraph/')
DB_PATH = PATH + "taskgraph.db"

def create_db():
    # If path not exist create one: ~/.taskgraph
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create database structure
    c.execute("""
            CREATE TABLE IF NOT EXISTS `task` (
                `id_task` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` int(11) UNIQUE,
                `short_name` varchar(10) UNIQUE,
                `color` int(11),
                FOREIGN KEY (`color`) REFERENCES `colors` (`id_color`)
            );
            """)
    c.execute(
        """
            CREATE TABLE IF NOT EXISTS `registry` (
                `id_registry` INTEGER PRIMARY KEY AUTOINCREMENT,
                `id_task` int(11),
                `date` date,
                FOREIGN KEY (`id_task`) REFERENCES `task` (`id_task`)
            );

        """
    )
    c.execute(
        """
            CREATE TABLE IF NOT EXISTS `colors` (
                `id_color` INTEGER PRIMARY KEY AUTOINCREMENT,
                `color` varchar(7) UNIQUE
            );
        """
    )
    #
    # c.execute(
    #     """
    #         INSERT INTO colors (color) VALUES ("#99E3B6")
    #     """
    # )

    conn.commit()
    c.close()

def create_task(task_name, short_name=None):

    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id_color FROM colors')
    result = c.fetchall()
    id_color = random.choice(result)
    id_color = id_color[0]
    values = (task_name, id_color,short_name)
    try:
        c.execute("INSERT INTO task (name, color, short_name) VALUES (?,?,?)", values)
    except ValueError:
        print "Taki task jest juz w bazie"
    # http://stackoverflow.com/questions/22488763/sqlite-insert-query-not-working-with-python
    conn.commit()
    c.close()

def do_task(task_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Do this instead
    t = (task_name,)
    c.execute('SELECT id_task FROM task WHERE name=?', t)
    result = c.fetchone()
    if result:
        task_id = result[0]
        print task_id
    else:
        c.execute('SELECT id_task FROM task WHERE short_name=?', t)
        result = c.fetchone()
        if result:
            task_id = result[0]
            print task_id
        else:
            c.execute('SELECT id_task FROM task WHERE id_task=?', t)
            result = c.fetchone()
            if result:
                task_id = result[0]
                print task_id
            else:
                print "Brak takiego taska"

    if 'task_id' in locals():
        today = datetime.now().strftime("%Y-%m-%d")
        values = (task_id, today)
        c.execute("INSERT INTO registry (id_task, date) VALUES (?,?)", values)

    conn.commit()
    c.close()

create_db()
#create_task("dodawanie7", "dodawaj")
#do_task("dodawanie")