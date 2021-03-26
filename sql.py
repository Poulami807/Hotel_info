
import sqlite3
def create(dbname):
    connec=sqlite3.connect("Oyo.db")
    connec.execute("CREATE TABLE IF NOT EXISTS OYO_HOTELS(NAME TEXT,ADDRESS TEXT,PRICE INT, AMENITIES TEXT,RATING TEXT)")
    print("Table succesfully created")
    connec.close()

def insert(dbname,values):
    connec=sqlite3.connect("Oyo.db")
    insert_data="INSERT INTO OYO_HOTELS(NAME,ADDRESS,PRICE,AMENITIES,RATING) VALUES(?,?,?,?,?)"
    connec.execute(insert_data,values)
    connec.commit()
    connec.close()
    
def get_info(dbname):
    connec=sqlite3.connect("Oyo.db")
    cur=connec.cursor()
    cur.execute("SELECT * FROM OYO_HOTELS")
    table_data=cur.fetchall()
    for record in table_data:
         print(record)
    connec.close()