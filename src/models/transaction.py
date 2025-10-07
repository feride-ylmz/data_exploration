import pandas as pd

class Transaction:
    def __init__(self, transaction_id, date, customer_id, product_id, \
                 store_id, quantity, unit_price, cost_price, discount, \
                    payment_method):
        
        self.transaction_id = transaction_id
        self.date = pd.to_datetime(date)
        self.year = self.date.year  # Jahr extrahieren
        self.customer_id = customer_id
        self.product_id = product_id
        self.store_id = store_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.cost_price = cost_price
        self.discount = discount
        self.payment_method = payment_method

    @property
    def sale(self):
        return self.quantity * self.unit_price * (1 - self.discount)

        
    @property
    def profit(self, sale, cost_price):
        return self.sale() - (self.cost_price * self.quantity)
        
