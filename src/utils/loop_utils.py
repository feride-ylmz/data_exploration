from utils.input_utils import input_check

def exit_check(prompt):
    """
    Fragt den Benutzer, ob er weitermachen möchte.
    Gibt True zurück, wenn "ja", False wenn "nein".
    """

    weiter = input_check(prompt, ["ja", "nein"])
    if weiter == "nein":
        return False
    return True