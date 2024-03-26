import sqlite3

class Restaurant_db:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def disconnect(self):
        self.connection.close()

    def create_tables(self):
        self.connect()
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INTEGER
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                restaurant_id INTEGER,
                customer_id INTEGER,
                rating INTEGER,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        self.connection.commit()
        self.disconnect()

    def add_restaurant(self, name, price):
        self.connect()
        self.cursor = self.connection.cursor()

        self.cursor.execute("INSERT INTO restaurants (name, price) VALUES (?, ?)", (name, price))

        self.connection.commit()
        self.disconnect()

    def add_customer(self, first_name, last_name):
        self.connect()
        self.cursor = self.connection.cursor()

        self.cursor.execute("INSERT INTO customers (first_name, last_name) VALUES (?, ?)", (first_name, last_name))

        self.connection.commit()
        self.disconnect()

    def get_restaurant(self, restaurant_id):
        self.connect()
        self.cursor = self.connection.cursor()

        self.cursor.execute("SELECT * FROM restaurants WHERE id = ?", (restaurant_id,))

        result = self.cursor.fetchone()

        self.disconnect()

        return result

    def get_customer(self, customer_id):
        self.connect()
        self.cursor = self.connection.cursor()

        self.cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))

        result = self.cursor.fetchone()

        self.disconnect()

        return result

    def add_review(self, restaurant, customer_id, rating):
        self.connect()
        self.cursor = self.connection.cursor()

        self.cursor.execute("INSERT INTO reviews (restaurant_id, customer_id, rating) VALUES (?, ?, ?)", (restaurant.id, customer_id, rating))

        self.connection.commit()
        self.disconnect()

    def get_reviews(self, restaurant):
        self.connect()
        self.cursor = self.connection.cursor()

        self.cursor.execute("SELECT * FROM reviews WHERE restaurant_id = ?", (restaurant.id,))

        results = self.cursor.fetchall()

        self.disconnect()

        return results

    def get_restaurants_for_customer(self, customer):
        self.connect()
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            SELECT DISTINCT r.*
            FROM restaurants r
            JOIN reviews rev ON r.id = rev.restaurant_id
            WHERE rev.customer_id = ?
        """, (customer.id,))

        results = self.cursor.fetchall()

        self.disconnect()

        return results
