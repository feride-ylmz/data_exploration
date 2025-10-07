import pandas as pd
import menu
from utils.input_utils import input_check
from utils.mapping_utils import resolve_column
from utils.loop_utils import exit_check
from utils.int_check_utils import input_positive_int



class KPI_Untermenu:
    def __init__(self, analysis):
        """
        Initialisiert das KPI-Untermenü.
        Eingabe: Analysis-Objekt 
        """
        self.analysis = analysis
        self.kpi = self.analysis.kpi_by_group

    def show(self):
        """
        Zeigt das KPI-Untermenü an und wartet auf Benutzerwahl.

        Ablauf:
        1. Anzeige der Menüoptionen.
        2. Benutzer wählt eine Option.
        3. Aufruf der entsprechenden Funktion basierend auf der Auswahl.
        """

        while True:
            print("\n--- KPI-Untermenü ---")
            print("1. Anzahl Kunden, Stores, Produkte und Transaktionen")
            print("2. KPIs flexibel berechnen")
            print("3. Top X nach KPI")
            print("4. Bottom X nach KPI")
            print("5. Loyal Customers anzeigen (mindestens X Transaktionen)")
            print("0. Zurück zum Hauptmenü")
            
            options = {
                "1": self.count_by_input,
                "2": self.interactive_kpi,
                "3" : self.top_x,
                "4" : self.bottom_x,
                "5": self.loyal_customers,
                "0" : lambda: menu.Menu(self.analysis.data).show()
            }
        
            choice = input("Bitte wählen Sie eine Option: ").strip()
            
            func = options.get(choice)
            if func:
                func()
            else:
                print("Ungültige Eingabe")


    #-----------------------------------------------------------------

    def count_by_input(self):
        """
        Zählt eindeutige Einträge in einer ausgewählten Kategorie.

        Ablauf:
            1. Zeigt dem Benutzer verfügbare Kategorien an.
            2. Fragt die Kategorie ab, für die die Anzahl der eindeutigen Werte berechnet werden soll.
            3. Ruft "self.kpi" auf, um die Anzahl zu berechnen.
            4. Gibt das Ergebnis aus.
            5. Fragt, ob der Benutzer weitere Kategorien zählen möchte, und wiederholt den Vorgang bei Bestätigung.

        Eingabe: Benutzer wählt eine Kategorie per Eingabe aus.

        Ausgabe: Anzahl eindeutiger Werte in der gewählten Kategorie.
        """

        options = ["Customer","Store","Transaction", "Product"]
        print("Verfügbare Kategorien:", ", ".join(options))       

        
        while True:
            user_input = input_check("Kategorie auswählen, deren Anzahl ermittelt werden soll: ", options)
            
            count = self.kpi(user_input, group=None, operation=None)

            print(f"Anzahl eindeutiger {user_input}: {count}")
        
            if not exit_check("Weitere Kategorien zählen? (ja/nein):  "):
                return
        
    #-------------------------------------------------------------------------
    
    def select_options(self, group_options, op_options=None):
        """
        Fragt den Benutzer nach KPI-Spalte, optionaler Gruppierung und Aggregation
        und überprüft die Eingaben auf Gültigkeit.

        Ablauf:
            1. Zeigt dem Benutzer verfügbare KPI-Spalten zur Auswahl.
            2. Fragt nach einer optionalen Gruppierungsspalte.
            3. Prüft, ob eine Aggregation notwendig ist (IDs benötigen keine Aggregation -> nunique).
            4. Fragt nach der gewünschten Aggregationsfunktion, falls mehrere Optionen verfügbar sind.
            5. Gibt die gewählten Werte zurück.

        Eingabe:
            - group_options (List[str]): Liste der möglichen Gruppierungsspalten
            - op_options (List[str], optional): Liste der möglichen Aggregationsfunktionen

        Ausgabe:
            - value (str): Ausgewählte KPI-Spalte
            - group (str oder None): Ausgewählte Gruppierungsspalte oder None
            - operation (str): Gewählte Aggregationsfunktion
        """
        # Spalte für KPI
        value_options = ["Sale", "Profit", "Quantity", "Discount", "CostPrice", 
                         "UnitPrice", "Tenure", "Transaction"]
        print("Verfügbare Berechnungen:", ", ".join(value_options))

        # Überprüft Gültigkeit
        value = input_check("Welche Berechnung soll ausgeführt werden?: ",
                                 value_options)
                
        # Gruppierung optional
        print("Verfügbare Gruppierungen:", ", ".join(group_options))
        group = input_check("Nach welcher Dimension gruppieren?: ",
                                 group_options)
        
        # Falls "keine" gewählt, keine Gruppierung durchführen
        if group == "keine":
            group = None
        
        # hier wird Aggragationsfunktion ausgewählt
        # Für ID-Spalten wird keine Aggregation ausgewählt, Standard: "nunique"
        if value not in ['Transaction', 'Customer', 'Product', 'Store']:
            if len(op_options) != 1:
                # Wenn mehrere Aggregationsoptionen vorhanden, Benutzer auswählen lassen
                print("Verfügbare Aggeationen:", ", ".join(op_options))
                operation = input_check("Welche Aggregation soll durchgeführt werden?: ", op_options)
            else:
                # Falls nur eine Aggregation übergeben wurde, wird diese automatisch ausgeführt
                operation = op_options[0]
        else:
            operation = "nunique"

        return value, group, operation
    

    #----------------------------------------------------------------------------------------
    
    def interactive_kpi(self):
        """
        Berechnet eine KPI nach Benutzerwahl.

        Ablauf:
            1. Fragt den Benutzer über "select_options" nach:
                - KPI-Spalte
                - Optionaler Gruppierung
                - Gewünschte Aggregation
            2. Führt die Berechnung mit der gewählten KPI, Gruppierung und Aggregation über "self.kpi" aus.
            3. Gibt das Ergebnis der Berechnung aus.
    
        Eingabe: Auswahl der KPI, Gruppierung und Aggregation durch den Benutzer.
        Ausgabe: Berechnetes KPI-Ergebnis wird angezeigt.
        """

        # Mögliche Gruppierungsspalten für die Berechnung
        group_options =["Store", "Product", "SubCategory", "Region", "City",
                        "Year", "Age", "PaymentMethod", "keine"]
        
        # Mögliche Aggregationsfunktionen
        op_options = ["sum", "mean", "max", "min"] 

        # Benutzer wählt Wert, Gruppierung und Aggregation
        value, group, operation = self.select_options(group_options, op_options)
        try:
            # hier wird die Berechnung durchgeführt
            result = self.kpi(value, group, operation)
            print("\nErgebnis:")
            print(result)
        except Exception as e:
            print(f"Fehler: {e}")


    #---------------------------------------------------------------------------------------------
    def top_bottom_x(self, order, top=False):
        """
        Zeigt die Top X/ Bottom X Werte einer KPI nach Benutzerwahl an.

        Ablauf:
            1. Fragt den Benutzer über "select_options" nach:
                - KPI-Spalte
                - Gruppierungsspalte
                - Aggregation (hier standardmäßig "sum")
            2. Berechnet die KPI über "self.kpi".
            3. Fragt den Benutzer, wie viele Top-Ergebnisse angezeigt werden sollen.
            4. Sortiert die Ergebnisse absteigend und zeigt die Top X Werte an.
            5. Fragt, ob weitere Top X berechnet werden sollen; bei 'nein' wird die Funktion beendet.

        Eingabe: Auswahl der KPI, Gruppierung, Aggregation und Anzahl X durch den Benutzer.
        Ausgabe: Top X Ergebnisse werden angezeigt.
        """


        group_options =["Customer","Store", "Product", "SubCategory", "Region", "City","Year", "Age", "PaymentMethod"]
        op_options = ["sum"]

        while True:
            # Benutzer wählt Wert, Gruppierung und Aggregation
            value, group, operation = self.select_options(group_options, op_options)
            try:
                # hier wird die Berechnung durchgeführt
                result = self.kpi(value, group, operation)
                # Top X auswählen und anzeigen
                x = input_positive_int(f"Wie viele {order}-Ergebnisse anzeigen?: ")
                subset = result.sort_values(ascending=top).head(x)
                print(f"\n{'Top' if not top else 'Bottom'} {x} nach {value}:")
                print(f"\nTop {subset}:")

                if not exit_check(f"Weitere {order}-Ergebnisse berechnen? (ja/nein): "):
                    return

            except Exception as e:
                print(f"Fehler: {e}")
    
    #-------------------------------------------------------------------------
    def top_x(self):
        self.top_bottom_x("TOP", top=False)

    #---------------------------------------------------------------------    
    def bottom_x(self):
        self.top_bottom_x("BOTTOM", top=True)
            
            
    #-------------------------------------------------------------------
    def loyal_customers(self):
        """
        Zeigt loyale Kunden basierend auf der Mindestanzahl an Transaktionen an.

        Ablauf:
            1. Fragt den Benutzer nach der minimalen Anzahl an Transaktionen.
            2. Ruft die Analysis-Funktion "loyal_customers" auf, um die Kunden zu ermitteln.
            3. Gibt die Ergebnisse aus oder informiert, wenn keine Kunden die Bedingung erfüllen.
            4. Fragt, ob weitere Abfragen durchgeführt werden sollen, und wiederholt bei Bestätigung.

        Eingabe: Benutzer gibt eine positive Ganzzahl für minimale Transaktionen ein.

        Ausgabe: Liste der Kunden, die die Mindestanzahl an Transaktionen erfüllt haben.
        """

        while True: 
            min = input_positive_int("Mindestens wie viele Transaktionen?: ")
            result = self.analysis.loyal_customers(min)
            if result.empty:
                print(f"Keine Kunden haben mindestens {min} Transaktionen getätigt.")
            else:
                print(result)

            if not exit_check("Weitere loyale Kunden anzeigen? (ja/nein): "):
                return
                
        
            
        
        