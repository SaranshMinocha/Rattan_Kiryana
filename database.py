# import sqlite3
#
# connection = sqlite3.connect("store.db")
# mycursor = connection.cursor()
# # mycursor.execute("""
# # CREATE TABLE IF NOT EXISTS Products(
# #     ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
# #     Category TEXT,
# #     Brand TEXT,
# #     SizeValue INTEGER,
# #     SizeUnit TEXT,
# #     Price INTEGER,
# #     Stock INTEGER
# # )
# # """)
# connection.execute("PRAGMA foreign_keys = ON;")
# mycursor.execute("""
#     CREATE TABLE IF NOT EXISTS Sales(
#         SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
#         ProductID INTEGER,
#         Quantity INTEGER,
#         TotalAmount REAL,
#         SaleTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY (ProductID) REFERENCES Products (ProductID)
#     );
# """)
# connection.close()
import sqlite3

conn = sqlite3.connect("store.db")
try:
    conn.execute("ALTER TABLE Products ADD COLUMN image_url TEXT DEFAULT 'https://placehold.co/150x150?text=No+Image'")
    conn.commit()
    print("Added image_url column.")
except Exception as e:
    print("Column might already exist:", e)
conn.close()