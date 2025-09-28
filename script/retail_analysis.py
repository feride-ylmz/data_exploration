import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

'''
Analyse der Einzelhandelsumsätze:
=========================================
Ziel: Analyse der Verkaufsdaten, um Trends, Top-Kunden,
Produktperformance und Verkäufe nach Regionen und Kundensegmente zu 
identifizieren.
'''


file = "../data/retail_sales_dataset.xlsx"
transactions = pd.read_excel(file, sheet_name="Transactions")
customers = pd.read_excel(file, sheet_name="Customers")
stores = pd.read_excel(file, sheet_name="Stores")
products = pd.read_excel(file, sheet_name="Products")

# Tabellen verbinden

data = pd.merge(transactions, customers, on="CustomerID")
data = pd.merge(data, stores, on="StoreID")
data = pd.merge(data, products, on="ProductID")


today = pd.to_datetime("today")  # Aktueller Tag
data["Sale"] = data["Quantity"] * data["UnitPrice"] * (1- data["Discount"])
data["BirthDate"] = pd.to_datetime(data["BirthDate"])
data["Age"] = (today - data["BirthDate"]).dt.days // 365
data["JoinDate"] = pd.to_datetime(data["JoinDate"])
data["Tenure"] = (today - data["JoinDate"]).dt.days // 365
data['Date'] = pd.to_datetime(data['Date'])
data['Profit'] = data['Sale'] - (data['CostPrice'] * data['Quantity'])
data['Year'] = data['Date'].dt.year

# Anzahl Kunden
customers_count = data["CustomerID"].nunique()
print("Customer:", customers_count)

# Maximale Anzahl Bestellungen
customer_order = data.groupby("CustomerID")["TransactionID"].nunique().max()
print("Maximum Orders by a Customer:", customer_order)

# Anzahl Kunden die mehr als 25 Bestellungen getätigt haben
loyal = data.groupby("CustomerID")["TransactionID"].nunique()
loyal_customer = (loyal > 25).sum()
print("Number of Loyal Customers (>25 orders):", loyal_customer)

# Durschnittlicher Umsatz pro Kunde
avg_customer_sale = data.groupby("CustomerID")["Sale"].sum().mean()
print("Average Sale per Customer:", avg_customer_sale)

# Umsatz pro Transaktion
total_sale = data["Sale"].sum()
max_sales = data["Sale"].max()
median_sales = data["Sale"].median()
std_sales = data["Sale"].std()

# Umsatz in 2025
sale_2025 = data[data["Date"].dt.year == 2025]
total_sale_2025 = sale_2025["Sale"].sum()
print("Sale in 2025:", total_sale_2025)

# Filtern nach Region
east_sales = data[data["Region"] == "East"]
print("Sale by Region = East:", east_sales)

# Gesamtumsatz in East berechnen
total_east_sales = east_sales["Sale"].sum()
print("Total Sale in Region East:", total_east_sales)

# Umsatz nach Kundenalter und city
gender_sales = data.groupby("Gender")["Sale"].sum()
city_sales = data.groupby("City_x")["Sale"].sum()
age_groups = pd.cut(data["Age"], bins=[0,25,35,50,65,100], labels=["<25","25-35","35-50","50-65","65+"])
age_group_sales = data.groupby(age_groups)["Sale"].sum()

# Gewinn pro Transaktion
total_profit = data["Profit"].sum()

# Durchschnittlicher Warenkorbwert
basket = data.groupby("TransactionID")["Sale"].sum().mean()
print("Average backet:",basket)

# Discount auswirkung
discount_impact = data.groupby("Discount")["Sale"].sum()
print("Discount:",discount_impact)


# TOP 10 Kunden nach Umsatz in 2025
customers_sale = sale_2025.groupby("CustomerID")["Sale"].sum()
top_ten_customer_2025 = customers_sale.sort_values(ascending=False).head(10)
print("Top 10 Customer by Sale: \n ", top_ten_customer_2025)

# Schlechtesten 10 Produkte Nach Verkaufsmenge
products_sale = data.groupby("ProductID")["Quantity"].sum()
worst_ten_prod = products_sale.sort_values(ascending=True).head(10)
print("Wosrt 10 Products by Quantity: \n", worst_ten_prod)

# Umsatz pro Filiale
store_sale = data.groupby("StoreName")["Sale"].sum()
print("Sales by Store: \n", store_sale)



#------------------------------------
# Ordner für Plots
def save_plot(fig, filename, output_dir="../plots"):
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
    plt.show()

#-------------------------------------
# Umsatz der Stores über die Jahre
store_sale_year = data.groupby(["StoreName","Year"])["Sale"].sum().unstack(fill_value=0)
years = store_sale_year.columns.astype(int)

fig, ax = plt.subplots(figsize=(12,6))
for store in store_sale_year.index:
    ax.plot(years, store_sale_year.loc[store], marker='o', label=store)

ax.set_title("Umsatz der Stores über die Jahre", fontsize=14, fontweight='bold')
ax.set_xlabel("Jahr")
ax.set_ylabel("Umsatz [€]")
ax.set_xticks(years)
ax.legend(title="Store", bbox_to_anchor=(1.05,1), loc='upper left')
ax.grid(True)
plt.tight_layout()
save_plot(fig, "store_sales_over_years.png")
#-------------------------------------------------
# Top 10 Kunden nach Umsatz 2025 
fig, ax = plt.subplots(figsize=(8,5))
top_ten_customer_2025.plot(kind="bar", color="black", edgecolor="black", ax=ax)
ax.set_title("Top 10 Kunden nach Umsatz 2025", fontsize=14, fontweight="bold")
ax.set_xlabel("CustomerID")
ax.set_ylabel("Umsatz [€]")
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
save_plot(fig, "top_ten_customers_2025.png")

# Umsatz nach Alter
fig, ax = plt.subplots(figsize=(8,5))
age_group_sales.plot(kind="bar", color="black", edgecolor="black", ax=ax)
ax.set_title("Umsatz nach Altersgruppe", fontsize=14, fontweight="bold")
ax.set_xlabel("Altersgruppe")
ax.set_ylabel("Umsatz [€]")
plt.tight_layout()
save_plot(fig, "sales_by_age_group.png")

#---------------------------------------------------------
# Umsatz nach Katagorie
category_sales = data.groupby("SubCategory")["Sale"].sum()
fig, ax = plt.subplots(figsize=(8,5))
category_sales.plot(kind="bar", color="black", edgecolor="black", ax=ax)
ax.set_title("Umsatz nach Produktkategorie", fontsize=14, fontweight="bold")
ax.set_xlabel("Kategorie")
ax.set_ylabel("Umsatz €")
plt.tight_layout()
save_plot(fig, "sales_by_category.png")


#--------------------------------------------------------
# Umsatz nach Produktkategorie über die Jahre
data["Year"] = data["Date"].dt.year
category_yearly_sales = data.groupby(["Category", "Year"])["Sale"].sum().unstack(fill_value=0)

years = store_sale_year.columns.astype(int)

fig, ax = plt.subplots(figsize=(12,6))
for cat in category_yearly_sales.index:
    ax.plot(category_yearly_sales.columns, category_yearly_sales.loc[cat], marker='o', label=cat)

ax.set_title("Umsatz nach Kategorie über die Jahre", fontsize=14, fontweight='bold')
ax.set_xlabel("Jahr")
ax.set_ylabel("Umsatz [€]")
ax.legend(title="Kategorie", bbox_to_anchor=(1.05,1), loc='upper left')
ax.set_xticks(years)
ax.grid(True)
plt.tight_layout()
save_plot(fig, "category_sales_over_years.png")

plt.show
#------------------------------------------------------
# Umsatz nach Rabatt
discount = data.groupby("Discount")["Sale"].sum()
fig, ax = plt.subplots(figsize=(8,5))
discount.plot(kind="bar", color="black", edgecolor="black", ax=ax)
ax.set_title("Umsatz nach Rabatt", fontsize=14, fontweight="bold")
ax.set_xlabel("Discount [%]")
ax.set_ylabel("Umsatz [€]")
plt.tight_layout()
save_plot(fig, "sales_by_discount.png")

#-----------------------------------------------------
# Schlechteste 10 Produkte nach Verkaufsmenge
fig, ax = plt.subplots(figsize=(8,5))
worst_ten_prod.plot(kind="bar", color="black", edgecolor="black", ax=ax)
ax.set_title("Schlechteste 10 Produkte nach Verkaufsmenge", fontsize=14, fontweight="bold")
ax.set_xlabel("ProductID")
ax.set_ylabel("# Menge")
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
save_plot(fig, "worst_ten_products.png")

