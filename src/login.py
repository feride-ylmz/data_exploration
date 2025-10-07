import random


class Login:

    """
    Login-Klasse mit einfacher Captcha-Prüfung.

    Funktion captcha_check:
        1. Generiert zwei zufällige Zahlen zwischen 1 und 10.
        2. Fragt den Benutzer nach der Summe dieser Zahlen, um einen Roboter auszuschließen.
        3. Prüft, ob die Eingabe eine Zahl ist.
        4. Gibt True zurück, wenn die Eingabe korrekt ist, sonst False.

    Zweck:
    Verhindert automatisierten Zugriff und stellt sicher, 
    dass ein echter Benutzer interagiert.
    """

    def captcha_check(self):
        a, b = random.randint(1,10), random.randint(1,10)
        print(f"Bestätigen Sie, dass Sie kein Roboter sind")
        try: 
            user_input = int(input(f"Bitte geben Sie das Ergebnis an {a} + {b} = ?: "))
        except ValueError:
            print("Ungültige Eingabe! Bitte eine Zahl eingeben. \n")
            return False
        return user_input == a + b