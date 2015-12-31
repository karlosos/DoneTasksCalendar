from datetime import date, datetime, timedelta
import random
import sqlite3
import os
import html_utils

PATH = os.path.expanduser('~/.taskgraph/')
DB_PATH = PATH + "taskgraph.db"
#ECD078 - zloto
#C02942 - czerwien
#53777A - niebieski
#CFF09E - morski
#C7F464 - zielony
#556270 - granatowy
COLORS = ("#ECD078","#C02942", "#53777A", "#CFF09E", "#C7F464", "#556270")

def create_db():
    """
    Init database with schema and basic colors
    :return:
    """
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

    try:
        add_colors(COLORS)
    except:
        None

    conn.commit()
    c.close()

def add_colors(colors):
    """
    Add color do db
    :param colors:
    :return:
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for color in colors:
        values = (color,)
        c.execute("INSERT INTO colors (color) VALUES (?)", values)
    conn.commit()
    c.close()

def create_task(task_name, short_name=None):
    """
    Create task with given name and optional short_name
    :param task_name:
    :param short_name:
    :return:
    """
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
    html_utils.update_output()

def do_task(task_name):
    """
    "DO" tasks with current date.
    :param task_name:
    :return:
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Do this instead
    t = (task_name,)
    c.execute('SELECT id_task FROM task WHERE name=?', t)
    result = c.fetchone()
    if result:
        task_id = result[0]
        #print task_id
    else:
        c.execute('SELECT id_task FROM task WHERE short_name=?', t)
        result = c.fetchone()
        if result:
            task_id = result[0]
            #print task_id
        else:
            c.execute('SELECT id_task FROM task WHERE id_task=?', t)
            result = c.fetchone()
            if result:
                task_id = result[0]
                #print task_id
            else:
                print "Brak takiego taska"

    if 'task_id' in locals():
        #today = datetime.now().strftime("%Y-%m-%d")
        today = datetime.now()
        values = (task_id, today)
        c.execute("INSERT INTO registry (id_task, date) VALUES (?,?)", values)

    conn.commit()
    c.close()
    html_utils.update_output()

def get_last(task=None, limit=5):
    """
    Return last done tasks with name and date for given task
    If task is not passed then return all tasks
    :param task: tak.name, task.short_name, or task.id_task
    :param limit: number of limited rows. ATTENTION! THESE ARE NOT DAYS
    :return:
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    t = (limit, )
    if task == None:
        c.execute('SELECT name, date FROM task INNER JOIN registry ON task.id_task = registry.id_task ORDER BY registry.date DESC LIMIT ?', t)
    else:
        t = (task, task, task, limit)
        c.execute('SELECT name, date FROM task INNER JOIN registry ON task.id_task = registry.id_task WHERE task.name = ? OR task.short_name = ? OR task.id_task = ? ORDER BY registry.date DESC LIMIT ?', t)

    results = c.fetchall()

    r_result = []
    for row in results:
        r_result.append(row)

    return r_result


def get_time(task=None, days=365):
    """
    Return last done tasks with name and date for given task and limited by days
    If task is not passed then return all tasks
    :param task: task: tak.name, task.short_name, or task.id_task
    :param days:
    :return:
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now()-timedelta(days=days)
    today = today.strftime("%Y-%m-%d")
    t = (today, )

    if task == None:
        c.execute('SELECT name, date FROM task INNER JOIN registry ON task.id_task = registry.id_task WHERE registry.date >= ? ORDER BY registry.date', t)
    else:
        t = (today, task, task, task)
        c.execute('SELECT name, date FROM task INNER JOIN registry ON task.id_task = registry.id_task WHERE registry.date >= ? AND (task.short_name = ? OR task.name = ? or task.id_task = ?)ORDER BY registry.date', t)
    db_results = c.fetchall()
    results = []
    previous_date = None
    day_counter = 1

    last = len(db_results) - 1
    for i, row in enumerate(db_results):
        try:
            date = datetime.strptime(row[1], "%Y-%m-%d")
        except:
            date = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
        #date = row[1]
        if date == previous_date or previous_date == None:
            day_counter += 1
        else:
            timestamp = (date - datetime(1970, 1, 1)).total_seconds()
            result_row = (timestamp, day_counter)
            results.append(result_row)
            day_counter = 1

        if i == last:
            timestamp = (date - datetime(1970, 1, 1)).total_seconds()
            result_row = (timestamp, day_counter)
            results.append(result_row)
            day_counter = 1

        previous_date = date
    return results

def get_tasks_info():
    """
    Return info of all tasks
    :return:
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM task')
    db_results = c.fetchall()
    print db_results
    return db_results

def delete_db():
    """
    Remove, clear database
    :return:
    """
    os.remove(DB_PATH)

def get_color(id):
    """
    Return info of all colors
    :return:
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    t = (id, )
    c.execute('SELECT * FROM colors WHERE id_color = ?', t)
    db_results = c.fetchall()
    print db_results[0][1]
    return db_results[0][1]