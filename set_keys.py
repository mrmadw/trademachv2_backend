import sqlite3

c = sqlite3.connect("trademach.db")
c.execute("update products set image_key=? where id=?", ("00001-pc300-pom.jpeg", 1))
c.execute("update products set image_key=? where id=?", ("00002-pc210-lae.jpeg", 2))
c.commit()
print(c.execute("select id, name, image_key from products").fetchall())