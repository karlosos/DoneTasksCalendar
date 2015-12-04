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
                `name` int(11),
                `short_name` varchar(10),
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
                `color` varchar(7)
            );
        """
    )

    c.execute(
        """
            INSERT INTO colors (id_color, color) VALUES (1, "#99E3B6")
        """
    )
    c.close()

def create_task(task_name):

    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    values = (task_name, 1)
    c.execute("INSERT INTO task (name, color) VALUES (?,?)", values)

    c.close()


create_db()
create_task("programowanie")