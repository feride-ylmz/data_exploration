class Product:
    def __init__(self, product_id, name, category, subcategory, unit_price, cost_price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.unit_price = unit_price
        self.cost_price = cost_price

    @property
    def profit(self):
        return self.unit_price - self.cost_price
