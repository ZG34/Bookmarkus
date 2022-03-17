# holds export queries

import csv

from src.database import Database

db = Database()


def export_bookmarks(active_id):
    with open(f"export{active_id}.csv", 'w', newline='') as csvfile:
        db.cursor.execute("SELECT rowid, * FROM bookmarks WHERE OwnerID=(?)", (active_id,))
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
        raw = db.cursor.fetchall()
        writer.writerows(raw)
        csvfile.close()