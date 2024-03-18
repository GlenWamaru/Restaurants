class Restaurant:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def reviews(self, db):
        query = "SELECT * FROM reviews WHERE restaurant_id = ?"
        params = (self.id,)
        return db.execute_query(query, params)

    def customers(self, db):
        query = """
            SELECT DISTINCT c.*
            FROM customers c
            JOIN reviews rev ON c.id = rev.customer_id
            WHERE rev.restaurant_id = ?
        """
        params = (self.id,)
        return db.execute_query(query, params)

    @classmethod
    def fanciest(cls, db):
        query = "SELECT * FROM restaurants ORDER BY price DESC LIMIT 1"
        result = db.execute_query(query)
        if result:
            return result[0]
        else:
            return None

    def all_reviews(self, db):
        query = """
            SELECT CONCAT('Review for ', r.name, ' by ', c.first_name, ' ', c.last_name, ': ', rev.star_rating, ' stars.') AS full_review
            FROM reviews rev
            JOIN restaurants r ON rev.restaurant_id = r.id
            JOIN customers c ON rev.customer_id = c.id
            WHERE rev.restaurant_id = ?
        """
        params = (self.id,)
        return db.execute_query(query, params)
