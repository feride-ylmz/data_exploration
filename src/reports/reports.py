import os
import matplotlib.pyplot as plt
import pandas as pd
from kpi.kpi_ import KPI_Untermenu
from analysis import Analysis
from utils.input_utils import input_check
from utils.loop_utils import exit_check

class PlotMenu:
    """
    Menü für interaktive Datenvisualisierung.

    Funktionen:
        - Spalten auswählen
        - Daten aggregieren
        - Balkendiagramme erstellen
        - Plots speichern
    """
    def __init__(self, data):
        self.data = data
        self.analysis = Analysis(data)
        self.kpi_ = KPI_Untermenu(self.analysis)
        #self.mean_columns = ["Age", "Discount", "Tenure", "UnitPrice"]

    #-----------------------------------------------------------------------
    def save_plot(self, plot_figure, filename, output_dir="../plots"):
        """
        Speichert die erstellte Plot-Grafik als PNG-Datei.

        Eingabe:
            - plot_figure: Grafik
            - filename: Name der Datei
            - output_dir: Ordner, in dem gespeichert wird 
        """
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        plot_figure.savefig(filepath, dpi=300, bbox_inches="tight")
        print(f"Plot gespeichert unter: {filepath}")

    #-----------------------------------------------------------------------------
    def select_columns(self):
        """
        Fragt den Benutzer nach den Spalten für einen Plot.

        Ablauf:
            1. Zeigt die möglichen Y-Achsen-Spalten (numerisch) an.
            2. Fragt ab, welche Spalte auf die Y-Achse soll.
            3. Zeigt die möglichen X-Achsen-Spalten (Kategorie) an.
            4. Fragt ab, welche Spalte auf die X-Achse soll.
            5. Optional: Fragt, ob eine zweite Gruppierung hinzugefügt werden soll.
                Falls ja, wird die zweite Gruppierung ausgewählt.
    
        Rückgabe:
            y_ (str): Gewählte Y-Achse
            x_ (str): Gewählte X-Achse
            second_group (str oder None): Gewählte zweite Gruppierung oder None
        """
        y_option = ["Quantity", "Discount", "UnitPrice", "CostPrice", "Sale", "Age", "Tenure", "Profit"]
        x_option = ["TransactionID", "CustomerID", "StoreID", "PaymentMethod", "Gender", "City_x", "JoinDate",
                    "StoreName", "City_y", "Region", "ProductName", "Category", "SubCategory", "Year", "Age"]

        print("\nMögliche Y-Achsen:", ", ".join(y_option))
        y_ = input_check("Welche Spalte soll auf die Y-Achse (numerisch)? ", y_option)

        print("\nMögliche X-Achsen:", ", ".join(x_option))
        x_ = input_check("Welche Spalte soll auf die X-Achse (Kategorie)? ", x_option)

        # Optionale zweite Gruppierung
        second_group = None
        add_second = input_check("Zweite Gruppierung hinzufügen? (ja/nein): ", ["ja", "nein"])
        if add_second == "ja":
            # Zweite Gruppierung: alle Spalten außer der gewählten X-Achse
            print("Verfügbare Gruppierungsspalten:", ", ".join([c for c in x_option if c != x_]))
            second_group = input_check("Welche zweite Gruppierung soll verwendet werden? ",
                                                [c for c in x_option if c != x_])

        return y_, x_, second_group


    #---------------------------------------------------------------------------------------------------
    def aggregate_data(self, y_, x_, second_group=None):
        """
        Aggregiert die Daten nach der gewählten X-Achse und optional einer zweiten Gruppierung.

        - Mittelwert (mean) für Spalten wie Alter, Rabatt, Kundendauer, Stückpreis
        - Summe (sum) für monetäre Werte wie Umsatz, Kosten, Menge
        -Wenn eine zweite Gruppierung angegeben ist, wird ein Pivot erstellt (unstack).
        - Bei einer Gruppierung werden die Werte absteigend sortiert.

        Eingabe:
            - y_ (str): Spalte, die aggregiert werden soll (Y-Achse)
            - x_ (str): Spalte für die Hauptgruppierung (X-Achse)
            - second_group (str, optional): zweite Gruppierungsspalte

        Ausgabe:
            -Aggregierte Werte
        """

        mean_columns = ["Age", "Discount", "Tenure", "UnitPrice"]
        agg_func = "mean" if y_ in mean_columns else "sum"

        if second_group:
            grouped = self.data.groupby([x_, second_group])[y_]
            return grouped.agg(agg_func).unstack(fill_value=0)
        else:
            grouped = self.data.groupby(x_)[y_].agg(agg_func)
            return grouped


    #----------------------------------------------------------------------------
    def create_plot(self, grouped, y_, x_, second_group=None):
        """
        Erstellt und zeigt einen Balkendiagramm der aggregierten Daten.

        Ablauf:
            1. Erstellt Diagramm mit matplotlib.
            2. Zeichnet Balken (gestapelt, wenn second_group vorhanden).
            3. Setzt Titel, Achsenbeschriftungen und Drehung der X-Achse.
            4. Speichert die Grafik als PNG-Datei.
            5. Zeigt die Grafik und wartet auf Enter, um sie zu schließen.
        
        Eingabe:
            - "grouped": enthält die aggregierten Daten für den Plot.
            - "y_": Spalte für die Y-Achse (numerisch).
            - "x_": Spalte für die X-Achse (Kategorie).
            - "second_group": Optionale zweite Gruppierung für gestapelte Balken
        """

        plot_figure, ax = plt.subplots(figsize=(10, 6))
        if second_group:
            grouped.plot(kind="bar", ax=ax, edgecolor="black")
            ax.set_title(f"{y_} nach {x_} und {second_group}", fontsize=14, fontweight="bold")
        else:
            grouped.plot(kind="bar", ax=ax, color="black", edgecolor="black")
            ax.set_title(f"{y_} nach {x_}", fontsize=14, fontweight="bold")

        ax.set_xlabel(x_)
        ax.set_ylabel(y_)
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()

    
        filename = f"{y_}_by_{x_}" + (f"_and_{second_group}" if second_group else "") + ".png"
        self.save_plot(plot_figure, filename)
        plt.show(block=False)
        input("Drücke Enter, um den Plot zu schließen.")
        plt.close(plot_figure)

    #----------------------------------------------------------------------
    def interactive_plot(self):
        """
        Startet ein interaktives Menü zur Erstellung von Plots.

        Ablauf:
            1. Fragt den Benutzer nach Spalten für X-, Y-Achse und optionaler Gruppierung.
            2. Aggregiert die Daten je nach Auswahl.
            3. Erstellt und zeigt den Plot.
            4. Fragt, ob ein weiterer Plot erstellt werden soll.

        Rückgabe: Kehrt zum Hauptmenü zurück, 
        wenn keine weiteren Plots erstellt werden sollen.
        """

        while True:
            print("\n--- Interaktives Plot-Menü ---")

            y_, x_, second_group = self.select_columns()
            grouped = self.aggregate_data(y_, x_, second_group)
            self.create_plot(grouped, y_, x_, second_group)
            
            if not exit_check("Weitere Plots erstellen? (ja/nein): "):
                return "menu"
