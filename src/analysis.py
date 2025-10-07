import pandas as pd
from utils.mapping_utils import resolve_column

class Analysis:
    def __init__(self, data: pd.DataFrame):
        self.data = data


    def kpi_by_group(self, value, group=None, operation=None):
        """
        Berechnet eine Kennzahl (KPI) flexibel nach Spalte, Gruppierung und Aggregation.

        Ablauf:
            1. Wandelt Spaltennamen in den tatsächlichen DataFrame-Namen um (resolve_column).
            2. Prüft, ob es sich bei der Spalte um eine ID handelt --> dann werden eindeutige Werte gezählt.
            3. Führt sonst die gewählte Aggregation aus.
            4. Gibt das aggregierte Ergebnis zurück.

        Eingabe:
            - value (str): Spalte, die berechnet werden soll 
            - group (str, optional): Gruppierungsspalte 
            - operation (str, optional): Aggregationsart 

        Rückgabe: Aggregiertes KPI-Ergebnis
        """

        value_col = resolve_column(value)
        group_col = resolve_column(group) if group else None

        data = self.data.copy()

        # ID-Spalten automatisch als eindeutige Werte zählen
        id = ['TransactionID', 'CustomerID', 'ProductName', 'StoreName']
        if value_col in id:
            if group_col:
                return data.groupby(group_col)[value_col].nunique()
            else:
                return data[value_col].nunique()

        # Wenn eine Gruppierung angegeben wurde:
        # Daten werden nach group_col gruppiert und die 
        # gewählte Operation pro Gruppe berechnet.
        if group_col:
            grouped = data.groupby(group_col)[value_col]
            result = getattr(grouped, operation)()
            return result
        else:
            result = getattr(data[value_col], operation)()
            return result


    def loyal_customers(self, min_transactions):
        """
        Ermittelt Kunden mit mindestens 'min_transactions' Transaktionen.
        """
        counts = self.data.groupby('CustomerID')['TransactionID'].nunique()
        return counts[counts >= min_transactions]
