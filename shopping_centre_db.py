import sqlite3
from sqlite3 import Error


def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)

   return conn

def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)

def add_shop(conn, shop):
   """
   Create a new shop into the shops table
   :param conn:
   :param shop:
   :return: shop id
   """
   sql = '''INSERT INTO shops(name, specialization, address)
             VALUES(?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, shop)
   conn.commit()
   return cur.lastrowid


def add_product(conn, product):
   """
   Create a new product into the products table
   :param conn:
   :param task:
   :return: task id
   """
   sql = '''INSERT INTO products(shop_id, name, description, number, price)
             VALUES(?,?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, product)
   conn.commit()
   return cur.lastrowid


def select_product_by_name(conn, name):
   """
   Query products by name
   :param conn: the Connection object
   :param name:
   :return:
   """
   cur = conn.cursor()
   cur.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + name + '%',))

   rows = cur.fetchall()
   return rows


def select_all(conn, table):
   """
   Query all rows in the table
   :param conn: the Connection object
   :return:
   """
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()

   return rows

def select_where(conn, table, **query):
   """
   Query tasks from table with data from **query dict
   :param conn: the Connection object
   :param table: table name
   :param query: dict of attributes and values
   :return:
   """
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows  

def update(conn, table, id, **kwargs):
   """
   update table
   :param conn:
   :param table: table name
   :param id: row id
   :return:
   """
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

def delete_where(conn, table, **kwargs):
   """
   Delete from table where attributes from
   :param conn:  Connection to the SQLite database
   :param table: table name
   :param kwargs: dict of attributes and values
   :return:
   """
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM {table} WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")

def delete_all(conn, table):
   """
   Delete all rows from table
   :param conn: Connection to the SQLite database
   :param table: table name
   :return:
   """
   sql = f'DELETE FROM {table}'
   cur = conn.cursor()
   cur.execute(sql)
   conn.commit()
   print("Deleted")


if __name__ == "__main__":

   create_shops_sql = """
   -- shops table
   CREATE TABLE IF NOT EXISTS shops (
      id integer PRIMARY KEY,
      name text NOT NULL,
      specialization text,
      address text
   );
   """

   create_products_sql = """
   -- zadanie table
   CREATE TABLE IF NOT EXISTS products (
      id integer PRIMARY KEY,
      shop_id integer NOT NULL,
      name VARCHAR(250) NOT NULL,
      description TEXT,
      number integer NOT NULL,
      price integer NOT NULL,
      FOREIGN KEY (shop_id) REFERENCES shops (id)
   );
   """

   db_file = "shoppin_centre.db"

   conn = create_connection(db_file)
   if conn is not None:
        execute_sql(conn, create_shops_sql)
        execute_sql(conn, create_products_sql)

        shop1 = ("LEGO","toys","2nd store")
        shop1_id = add_shop(conn, shop1)

        shop2 = ("Mercedes","cars","0 store")
        shop2_id = add_shop(conn, shop2)

        shop3 = ("Tesco","food","1st store")
        shop3_id = add_shop(conn, shop3)


        produt1 = (
            shop1_id,
            "LEGO1",
            "lsdkjlfdssfd",
            1000,
            200
        )

        product1_id = add_product(conn, produt1)

        produt2 = (
            shop1_id,
            "LEGO2",
            "lslfk;kfslfdssfd",
            2000,
            400
        )

        product2_id = add_product(conn, produt2)

        produt3 = (
            shop1_id,
            "LEGO3",
            "sdjlksfdl",
            1200,
            20
        )
        product3_id = add_product(conn, produt3)

 
        produt4 = (
            shop2_id,
            "Marcedes1",
            "sdfjisjdfjfsd",
            120000,
            10
        )
        product4_id = add_product(conn, produt4)       


        produt5 = (
            shop2_id,
            "bread",
            "jsdjsdkfsd",
            5,
            1000
        )
        product5_id = add_product(conn, produt5) 


        res = select_where(conn, "shops", id=1)
        print(f"Number of shops with id=1: {len(res)}")

        res = select_where(conn, "products",shop_id=1)
        print(f"Number of products in shop with id = 1: {len(res)}")

        update(conn, "products", 2, description="bestseller")

        res = select_product_by_name(conn,"LEGO")
        
        for product in res:
            print(product) 

        delete_all(conn,'products')
        delete_all(conn,'shops')
        
        conn.close()