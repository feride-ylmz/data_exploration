
def input_positive_int(prompt):
    """
    Fragt solange nach, bis der Benutzer eine positive ganze Zahl eingibt.
    Gibt diese Zahl zurück.
    """
    
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Bitte eine positive Zahl eingeben.")
        except ValueError:
            print("Ungültige Eingabe! Bitte eine Ganzzahl eingeben.")
