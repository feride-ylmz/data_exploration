import pandas as pd
from datetime import datetime

class Customer:
    def __init__(self, customer_id, first_name, last_name, gender, \
                 birth_date, city, join_date):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_date = pd.to_datetime(birth_date)
        self.city = city
        self.join_date = pd.to_datetime(join_date)

        today = pd.to_datetime("today")
        self.age = (today - self.birth_date).days // 365
        self.tenure = (today - self.join_date).days // 365

    @property
    def age(self):
        today = pd.to_datetime("today")
        return (today - self.birth_date).days // 365
    
    @property
    def tenure(self):
        today = pd.to_datetime("today")
        return (today - self.join_date).days // 365
    

