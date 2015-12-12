import db_utils
__author__ = 'jupiter'

db_utils.delete_db()

db_utils.create_db()
db_utils.create_task("dodawanie", "dodawaj")
db_utils.do_task("dodawaj")
#
db_utils.get_last()
print db_utils.get_time("dodawanie")
print "WSZYSTKIE"
print db_utils.get_time()

COLORS = ("#ECD078","#C02942", "#53777A", "#CFF09E", "#C7F464", "#556270")

