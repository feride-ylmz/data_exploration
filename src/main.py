#from data_loader import load_data
from data_loader import DataLoader
from login import Login
from menu import Menu

"""
Startpunkt des Programms für den Benutzer.

Ablauf:
1. Begrüßt den Benutzer.
2. Startet das Login-System mit Captcha-Prüfung.
3. Bei erfolgreichem Login:
    - Lädt die Retail-Daten aus einer Excel-Datei.
    - Startet das Hauptmenü für die Datenexploration.
4. Bei fehlgeschlagenem Login wird der Zugriff verweigert und erneut abgefragt.
"""

if __name__ == "__main__":
    print(f"Herzlich Willkommen!")
    login_manager = Login()
    while True: 
        if login_manager.captcha_check():
            print("Zugang gewährt")

            loader = DataLoader("../data/retail_sales_dataset.xlsx")
            data = loader.load_data()
            menu = Menu(data)
            menu.show()
            break
        else:
            print("Zugang verweigert! Versuchen Sie es nochmal \n")