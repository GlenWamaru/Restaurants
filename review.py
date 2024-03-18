class Review:
    def __init__(self, id, restaurant_id, customer_id, star_rating):
        self.id = id
        self.restaurant_id = restaurant_id
        self.customer_id = customer_id
        self.star_rating = star_rating

    def customer(self, db):
        query = "SELECT * FROM customers WHERE id = ?"
        params = (self.customer_id,)
        result = db.execute_query(query, params)
        if result:
            return result[0]
        else:
            return None

    def restaurant(self, db):
        query = "SELECT * FROM restaurants WHERE id = ?"
        params = (self.restaurant_id,)
        result = db.execute_query(query, params)
        if result:
            return result[0]
        else:
            return None

    def full_review(self, db):
        customer = self.customer(db)
        restaurant = self.restaurant(db)
        return f"Review for {restaurant.name} by {customer.first_name} {customer.last_name}: {self.star_rating} stars."
