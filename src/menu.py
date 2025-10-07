from kpi.kpi_ import KPI_Untermenu
from analysis import Analysis
from reports.reports import PlotMenu


class Menu:
    """
    Hauptmenü-Klasse für die Anwendung.
    """

    def __init__(self, data):
        self.analysis = Analysis(data)

    def show(self):
        while True:
            print("\n--- Hauptmenü ---")
            print("1. KPIs berechnen")
            print("2. Plots erstellen")
            print("0. Abmelden / Beenden")

            options = {
                "1": self.run_kpi_menu,
                "2": self.run_plot_menu,
                "0": self.exit_program
            }

            choice = input("Bitte wählen Sie eine Option: ").strip()
            func = options.get(choice)

            if func:
                func()
            else:
                print("Ungültige Eingabe. Bitte erneut versuchen.")

    

    def run_kpi_menu(self):
        """
        Öffnet das KPI-Untermenü, in dem der Benutzer 
        Kennzahlen berechnen und analysieren kann.
        """
        kpi_menu = KPI_Untermenu(self.analysis)
        kpi_menu.show()

    def run_plot_menu(self):
        """
        Öffnet das interaktive Plot-Menü zur Visualisierung der Daten.
        """
        plot_menu = PlotMenu(self.analysis.data)
        result = plot_menu.interactive_plot()
        if result == "menu":
            return
        else:
            print("Zurück zum Hauptmenü.")


    def exit_program(self):
        print("Abmelden. Auf Wiedersehen!")
        exit()