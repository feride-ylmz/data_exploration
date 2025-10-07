def input_check(prompt, options):
    """
    Fragt den Benutzer solange nach Eingabe, bis eine gültige Option 
    gewählt wird. Gibt die gewählte Option zurück.
    """

    options_lower = [opt.lower() for opt in options]
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in options_lower:
            original_value = options[options_lower.index(user_input.lower())]
            return original_value
            
        print(f"Ungültige Eingabe! Erlaubt: {', '.join(options)}")
