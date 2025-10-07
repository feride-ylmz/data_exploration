import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

class DataLoader:
    def __init__(self, file_path):
        self.file = file_path

    def load_data(self):
        """
        Lädt und bereitet die Einzelhandelsdaten auf.

        Ablauf:
        1. Liest die Tabellen "Transactions", "Customers", "Stores" und 
            "Products" aus einer Excel-Datei ein.
        2. Verknüpft die Tabellen über die jeweiligen IDs zu einem DataFrame.
        3. Berechnet zusätzliche Spalten:
            - Sale: Umsatz pro Transaktion (Quantity * UnitPrice * (1 - Discount))
            - Profit: Gewinn pro Transaktion (Sale - Kosten)
            - Age: Alter der Kunden in Jahren
            - Tenure: Mitgliedsdauer in Jahren
            - Year: Jahr der Transaktion
        4. Wandelt Datumsangaben in datetime-Objekte um.

        Zweck:
        Stellt einen vollständigen, berechneten DataFrame bereit, 
        der für Analysen, KPI-Berechnungen und Plots genutzt werden kann.
        """

    #file = "../data/retail_sales_dataset.xlsx"
        transactions = pd.read_excel(self.file, sheet_name="Transactions")
        customers = pd.read_excel(self.file, sheet_name="Customers")
        stores = pd.read_excel(self.file, sheet_name="Stores")
        products = pd.read_excel(self.file, sheet_name="Products")
    
        # Tabellen verbinden
        data = transactions.merge(customers, on="CustomerID")\
                           .merge(stores, on="StoreID")\
                           .merge(products, on="ProductID")

        today = pd.to_datetime("today")  # Aktueller Tag
        data["Sale"] = data["Quantity"] * data["UnitPrice"] * (1- data["Discount"])
        data["BirthDate"] = pd.to_datetime(data["BirthDate"])
        data["Age"] = (today - data["BirthDate"]).dt.days // 365
        data["JoinDate"] = pd.to_datetime(data["JoinDate"])
        data["Tenure"] = (today - data["JoinDate"]).dt.days // 365
        data['Date'] = pd.to_datetime(data['Date'])
        data['Profit'] = data['Sale'] - (data['CostPrice'] * data['Quantity'])
        data['Year'] = data['Date'].dt.year

        #print(data.columns.tolist())


        return data
