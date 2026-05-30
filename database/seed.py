import sqlite3, random
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "sales.db"
if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.executescript("""
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT, country TEXT, region TEXT, signup_date TEXT);
CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, unit_price REAL, stock INTEGER);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT);
CREATE TABLE order_items (item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, quantity INTEGER);
""")

countries = {"United States":"North America","Canada":"North America","United Kingdom":"Europe",
             "Germany":"Europe","France":"Europe","India":"Asia","Japan":"Asia",
             "Australia":"Oceania","Brazil":"South America"}
first = ["Maya","James","Aisha","Carlos","Wei","Olivia","Raj","Sofia","Liam","Yuki",
         "Hannah","Diego","Priya","Noah","Emma","Omar","Grace","Lucas","Ananya","Ethan"]
last = ["Rodriguez","Smith","Khan","Mueller","Tanaka","Brown","Patel","Garcia","Wilson",
        "Nakamura","Lee","Silva","Johnson","Chen","Davis","Kumar","Martin","Nguyen"]
products = [("Wireless Mouse","Electronics",25.99,340),("Mechanical Keyboard","Electronics",89.99,120),
            ("USB-C Cable","Accessories",12.50,800),("Laptop Stand","Accessories",34.00,210),
            ("Noise-Cancelling Headphones","Electronics",199.99,75),("Webcam HD","Electronics",59.99,150),
            ("Desk Lamp","Home Office",29.99,260),("Ergonomic Chair","Furniture",249.00,40),
            ("Standing Desk","Furniture",399.00,25),("Notebook Pack","Stationery",9.99,1200),
            ("Gel Pen Set","Stationery",7.49,900),("Monitor 27 inch","Electronics",279.00,60),
            ("Phone Charger","Accessories",15.99,500),("Coffee Mug","Home Office",11.99,430),
            ("Backpack","Accessories",49.99,180)]
statuses = ["completed","completed","completed","pending","cancelled","shipped"]

clist = list(countries)
for cid in range(1,201):
    name = f"{random.choice(first)} {random.choice(last)}"
    country = random.choice(clist)
    signup = datetime(2023,1,1)+timedelta(days=random.randint(0,700))
    cur.execute("INSERT INTO customers VALUES (?,?,?,?,?)",(cid,name,country,countries[country],signup.strftime("%Y-%m-%d")))

for pid,(n,c,p,s) in enumerate(products,1):
    cur.execute("INSERT INTO products VALUES (?,?,?,?,?)",(pid,n,c,p,s))

oid=iid=1
for _ in range(1000):
    od = datetime(2024,1,1)+timedelta(days=random.randint(0,510))
    cur.execute("INSERT INTO orders VALUES (?,?,?,?)",(oid,random.randint(1,200),od.strftime("%Y-%m-%d"),random.choice(statuses)))
    for _ in range(random.randint(1,4)):
        cur.execute("INSERT INTO order_items VALUES (?,?,?,?)",(iid,oid,random.randint(1,len(products)),random.randint(1,5)))
        iid+=1
    oid+=1

conn.commit()
for t in ["customers","products","orders","order_items"]:
    print(f"{t:15s}: {cur.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]:,} rows")
conn.close()
print(f"\nDatabase created at {DB_PATH}")
