import sqlite3

c = sqlite3.connect("trademach.db")
c.execute("ALTER TABLE products ADD COLUMN image_key VARCHAR(500)")
c.commit()
print(c.execute("select id, name, image_key from products").fetchall())