from utils import db
conn = db.connect()
db.purge_table(conn)
