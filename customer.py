class Customer:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def reviews(self, db):
        query = "SELECT * FROM reviews WHERE customer_id = ?"
        params = (self.id,)
        return db.execute_query(query, params)

    def restaurants(self, db):
        query = """
            SELECT DISTINCT r.*
            FROM restaurants r
            JOIN reviews rev ON r.id = rev.restaurant_id
            WHERE rev.customer_id = ?
        """
        params = (self.id,)
        return db.execute_query(query, params)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self, db):
        query = """
            SELECT r.*
            FROM restaurants r
            JOIN reviews rev ON r.id = rev.restaurant_id
            WHERE rev.customer_id = ?
            ORDER BY rev.star_rating DESC
            LIMIT 1
        """
        params = (self.id,)
        result = db.execute_query(query, params)
        if result:
            return result[0]
        else:
            return None

    def add_review(self, db, restaurant, rating):
        query = "INSERT INTO reviews (restaurant_id, customer_id, star_rating) VALUES (?, ?, ?)"
        params = (restaurant.id, self.id, rating)
        db.execute_query(query, params)

    def delete_reviews(self, db, restaurant):
        query = "DELETE FROM reviews WHERE customer_id = ? AND restaurant_id = ?"
        params = (self.id, restaurant.id)
        db.execute_query(query, params)
