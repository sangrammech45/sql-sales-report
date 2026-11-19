"""Builds sales.db with synthetic (made-up) data for the practice project."""
import random, sqlite3, datetime

random.seed(42)
con = sqlite3.connect("sales.db")
con.executescript("""
DROP TABLE IF EXISTS order_items; DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;    DROP TABLE IF EXISTS customers;
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, region TEXT);
CREATE TABLE products  (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL);
CREATE TABLE orders    (id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), order_date TEXT);
CREATE TABLE order_items (order_id INTEGER REFERENCES orders(id), product_id INTEGER REFERENCES products(id), quantity INTEGER);
""")
regions = ["North", "South", "East", "West"]
con.executemany("INSERT INTO customers VALUES (?,?,?)",
    [(i, f"Customer {i:03d}", random.choice(regions)) for i in range(1, 201)])
products = [("Notebook","Stationery",4.5),("Pen Set","Stationery",8),("Desk Lamp","Home Office",24),
            ("Monitor Stand","Home Office",39),("USB Hub","Electronics",19),("Keyboard","Electronics",49),
            ("Mouse","Electronics",22),("Webcam","Electronics",45),("Mug","Kitchen",9),
            ("Water Bottle","Kitchen",14),("Backpack","Accessories",59),("Phone Stand","Accessories",12)]
con.executemany("INSERT INTO products VALUES (?,?,?,?)", [(i+1,*p) for i,p in enumerate(products)])
start = datetime.date(2026,1,1)
for oid in range(1, 1501):
    d = start + datetime.timedelta(days=random.randint(0, 303))
    con.execute("INSERT INTO orders VALUES (?,?,?)", (oid, random.randint(1,200), d.isoformat()))
    for pid in random.sample(range(1,13), random.randint(1,3)):
        con.execute("INSERT INTO order_items VALUES (?,?,?)", (oid, pid, random.randint(1,4)))
con.commit()
