import db_utils
__author__ = 'jupiter'

db_utils.create_db()
#create_task("dodawanie7", "dodawaj")
db_utils.do_task("dodawanie")
#add_colors(COLORS)
db_utils.get_last()
print db_utils.get_time("dodawanie")
print "WSZYSTKIE"
print db_utils.get_time()