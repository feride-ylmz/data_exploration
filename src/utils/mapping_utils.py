COLUMN_MAPPING = {
    "Transaction": "TransactionID",
    "Customer": "CustomerID",
    "Product": "ProductName",
    "Store": "StoreName",
    "Region": "Region",
    "Year": "Year",
    "City": "City_y",
    "Subcategory": "SubCategory",
    "Quantity": "Quantity",
    "CostPrice": "CostPrice",
    "UnitPrice": "UnitPrice",
    "Age": "Age",
    "PaymentMethod": "PaymentMethod"
}

def resolve_column(name):
    """
    Gibt den tatsächlichen Spaltennamen zurück basierend auf 
    vordefiniertem Mapping.
    Wenn der Name nicht im Mapping ist, wird er unverändert zurückgegeben.
    """
    return COLUMN_MAPPING.get(name, name)
