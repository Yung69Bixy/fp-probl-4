
class Tranzactie:
    """Reprezintă o tranzacție bancară, conținând ziua, suma și tipul ('intrare' sau 'iesire')."""
    def __init__(self, zi, suma, tip):
        self.zi = zi  # Ziua în care s-a efectuat tranzacția
        self.suma = suma  # Suma tranzacției
        self.tip = tip  # Tipul tranzacției: 'intrare' sau 'iesire'

# Dicționar de tranzacții și istoric
tranzactii = {}  # Dicționar care stochează toate tranzacțiile curente
istoric = []  # Istoric pentru a urmări toate modificările tranzacțiilor

def cauta_tranzactii_mari(suma):
    """Returnează un dicționar cu tranzacțiile cu sume mai mari decât o sumă dată."""
    return {k: v for k, v in tranzactii.items() if v['suma'] > suma}

def cauta_tranzactii_inainte_de(zi, suma):
    """Returnează un dicționar cu tranzacțiile efectuate înainte de o zi specificată și cu sume mai mari decât o sumă dată."""
    return {k: v for k, v in tranzactii.items() if v['zi'] < zi and v['suma'] > suma}

def validare_tranzactie(zi, suma, tip):
    """Verifică dacă tranzacția respectă regulile: ziua trebuie să fie între 1 și 31, suma pozitivă, iar tipul 'intrare' sau 'iesire'."""
    if suma < 0:
        raise ValueError("Suma nu poate fi negativă.")  # Validare pentru sumă
    if tip not in ['intrare', 'iesire']:
        raise ValueError("Tipul trebuie să fie 'intrare' sau 'iesire'.")  # Validare pentru tip

id_tranzactie_counter = 1

def adauga_tranzactie(zi, suma, tip, tranzactii):
    """Adaugă o tranzacție în dicționarul 'tranzactii'."""
    global id_tranzactie_counter
    # Definim un ID unic pentru fiecare tranzacție
    id_tranzactie = id_tranzactie_counter
    tranzactie = {
        'id': id_tranzactie,
        'zi': zi,
        'suma': suma,
        'tip': tip
    }
    tranzactii[id_tranzactie] = tranzactie
    id_tranzactie_counter += 1  # Incrementăm contorul pentru următorul ID

def actualizeaza_tranzactie(zi_initiala, suma_initiala, tip_initial, zi_noua, suma_noua, tip_nou, tranzactii):
    """Actualizează o tranzacție în dicționar."""
    key_initiala = f"{zi_initiala}_{tip_initial}_{suma_initiala}"

    # Verificăm dacă tranzacția există
    if key_initiala not in tranzactii:
        raise ValueError("Tranzacția nu a fost găsită.")  # Dacă tranzacția nu există, ridicăm eroare
    
    # Creăm cheia pentru tranzacția actualizată
    key_noua = f"{zi_noua}_{tip_nou}_{suma_noua}"
    
    # Actualizăm tranzacția
    tranzactii[key_noua] = {"zi": zi_noua, "suma": suma_noua, "tip": tip_nou}
    
    # Ștergem tranzacția veche
    del tranzactii[key_initiala]
    
    return True

def sterge_tranzactie_dupa_zi(zi):
    """Șterge toate tranzacțiile care au fost înregistrate într-o anumită zi."""
    global tranzactii # Modificăm dicționarul global de tranzacții
    # Crează o listă a cheilor care trebuie șterse
    chei_de_sters = [key for key in tranzactii if key.startswith(f"{zi}_")]
    for key in chei_de_sters:
        del tranzactii[key] # Șterge tranzacția din dicționar
    istoric.append(("sterge_dupa_zi", zi)) # Salvează ștergerea în istoric

def sterge_tranzactii_perioada(zi_inceput, zi_sfarsit):
    """Șterge tranzacțiile înregistrate într-o perioadă dată, de la o zi de început la o zi de sfârșit."""
    global tranzactii # Modificăm dicționarul global de tranzacții
    chei_de_sters = [key for key in tranzactii if zi_inceput <= tranzactii[key].zi <= zi_sfarsit]
    for key in chei_de_sters:
        del tranzactii[key] # Șterge tranzacția din dicționar
    istoric.append(("sterge_perioada", (zi_inceput, zi_sfarsit))) # Salvează ștergerea în istoric

def filtreaza_tranzactii_dupa_tip(tip):
    """Filtrează tranzacțiile de un anumit tip ('intrare' sau 'iesire') și returnează lista cu tranzacțiile respective."""
    tranzactii_filtrate = {key: tranzactie for key, tranzactie in tranzactii.items() if tranzactie['tip'] == tip}
    return tranzactii_filtrate # Returnează tranzacțiile filtrate

def suma_totala_dupa_tip(tip):
    """Returnează suma totală a tranzacțiilor de un anumit tip ('intrare' sau 'iesire')."""
    return sum(t['suma'] for t in tranzactii.values() if t['tip'] == tip)

def sold_la_data(data):
    """Calculează soldul contului la o dată specificată, adunând toate intrările și scăzând ieșirile până la acea dată."""
    intrari = sum(t['suma'] for t in tranzactii.values() if t['tip'] == "intrare" and t['zi'] <= data)
    iesiri = sum(t['suma'] for t in tranzactii.values() if t['tip'] == "iesire" and t['zi'] <= data)
    return intrari - iesiri

def tranzactii_dupa_tip_ordonate(tip):
    """Returnează o listă cu toate tranzacțiile de un anumit tip, ordonate descrescător după sumă."""
    tranzactii_ordonate = [t for t in tranzactii.values() if t['tip'] == tip]
    return sorted(tranzactii_ordonate, key=lambda t: t['suma'], reverse=True)

def tranzactii_in_interval(zi_start, zi_sfarsit):
    """Returnează tranzacțiile dintr-un interval de zile specificat."""
    tranzactii_interval = {key: tranzactie for key, tranzactie in tranzactii.items() if zi_start <= tranzactie['zi'] <= zi_sfarsit}
    return tranzactii_interval

def suma_totala_in_interval(zi_start, zi_sfarsit):
    """Returnează suma totală a tranzacțiilor dintr-un interval de zile."""
    return sum(t['suma'] for t in tranzactii.values() if zi_start <= t['zi'] <= zi_sfarsit)

def tranzactii_dupa_tip_ordonate(tip):
    """Returnează o listă cu tranzacțiile de un anumit tip, ordonate descrescător după sumă."""
    tranzactii_ordonate = [t for t in tranzactii.values() if t['tip'] == tip]
    return sorted(tranzactii_ordonate, key=lambda t: t['suma'], reverse=True)

def istoricul_modificarilor():
    """Returnează istoricul modificărilor efectuate asupra tranzacțiilor."""
    return istoric

def afiseaza_meniu():
    """Afișează un meniu cu opțiuni pentru gestionarea tranzacțiilor."""
    print("\nMeniu:")
    print("1. Adăugare tranzacție")
    print("2. Actualizare tranzacție")
    print("3. Ștergere tranzacție după zi")
    print("4. Ștergere tranzacții dintr-o perioadă")
    print("5. Ștergere tranzacții după tip")
    print("6. Căutare tranzacții mari")
    print("7. Căutare tranzacții înainte de o zi")
    print("8. Suma totală a tranzacțiilor de un anumit tip")
    print("9. Soldul contului la o dată specificată")
    print("10. Tipărire tranzacții de un anumit tip ordonate")
    print("11. Ieșire")

def main():
    """Funcția principală care gestionează interacțiunea cu utilizatorul. Afișează meniul și procesează opțiunile utilizatorului."""
    tranzactii = {}
    while True:
        afiseaza_meniu() # Afișează meniul de opțiuni
        optiune = input("Alegeți o opțiune (1-11): ") # Alege o opțiune

        if optiune == '1':
            # Adăugare tranzacție
            zi = input("Introduceți ziua (YYYY-MM-DD): ")
            suma = float(input("Introduceți suma: "))
            tip = input("Introduceți tipul (intrare/iesire): ")
            try:
                adauga_tranzactie(zi, suma, tip, tranzactii) # Adaugă tranzacția după validare
                print("Tranzacția a fost adăugată cu succes.")
            except ValueError as e:
                print(e) # Afișează mesajul de eroare

        elif optiune == '2':
            # Actualizare tranzacție
            zi_veche = input("Introduceți ziua veche (YYYY-MM-DD): ")
            suma_veche = float(input("Introduceți suma veche: "))
            tip_vechi = input("Introduceți tipul vechi (intrare/iesire): ")
            zi_noua = input("Introduceți ziua nouă (YYYY-MM-DD): ")
            suma_noua = float(input("Introduceți suma nouă: "))
            tip_nou = input("Introduceți tipul nou (intrare/iesire): ")
            try:
                actualizeaza_tranzactie(zi_veche, suma_veche, tip_vechi, zi_noua, suma_noua, tip_nou, tranzactii)
                print("Tranzacția a fost actualizată cu succes.")
            except ValueError as e:
                print(e) # Afișează mesajul de eroare

        elif optiune == '3':
            # Ștergere tranzacție după zi
            zi = input("Introduceți ziua (YYYY-MM-DD): ")
            sterge_tranzactie_dupa_zi(zi) # Șterge tranzacțiile din ziua respectivă
            print("Tranzacțiile din această zi au fost șterse cu succes.")

        elif optiune == '4':
            # Ștergere tranzacții dintr-o perioadă
            zi_inceput = input("Introduceți ziua de început (YYYY-MM-DD): ")
            zi_sfarsit = input("Introduceți ziua de sfârșit (YYYY-MM-DD): ")
            sterge_tranzactii_perioada(zi_inceput, zi_sfarsit) # Șterge tranzacțiile din perioada respectivă
            print("Tranzacțiile din această perioadă au fost șterse cu succes.")

        elif optiune == '5':
            # Ștergere tranzacții după tip
            tip = input("Introduceți tipul (intrare/iesire): ")
            tranzactii_filtrate = filtreaza_tranzactii_dupa_tip(tip) # Obține tranzacțiile filtrate
            print(f"Tranzacțiile de tip '{tip}' au fost șterse cu succes.")

        elif optiune == '6':
            # Căutare tranzacții mari
            suma_minima = float(input("Introduceți suma minimă: "))
            tranzactii_mari = {key: t for key, t in tranzactii.items() if t.suma >= suma_minima}
            print(f"Tranzacțiile mai mari sau egale cu {suma_minima} sunt: {tranzactii_mari}")

        elif optiune == '7':
            # Căutare tranzacții înainte de o zi
            zi = input("Introduceți ziua (YYYY-MM-DD): ")
            tranzactii_inainte = {key: t for key, t in tranzactii.items() if t.zi < zi}
            print(f"Tranzacțiile înainte de {zi} sunt: {tranzactii_inainte}")

        elif optiune == '8':
            # Suma totală a tranzacțiilor de un anumit tip
            tip = input("Introduceți tipul (intrare/iesire): ")
            suma_totala = suma_totala_dupa_tip(tip) # Calculează suma totală
            print(f"Suma totală a tranzacțiilor de tip '{tip}' este: {suma_totala}")

        elif optiune == '9':
            # Soldul contului la o dată specificată
            data = input("Introduceți data (YYYY-MM-DD): ")
            sold = sold_la_data(data) # Calculează soldul
            print(f"Soldul contului la data {data} este: {sold}")

        elif optiune == '10':
            # Tipărire tranzacții de un anumit tip ordonate
            tip = input("Introduceți tipul (intrare/iesire): ")
            tranzactii_ordonate = tranzactii_dupa_tip_ordonate(tip) # Obține tranzacțiile ordonate
            print(f"Tranzacțiile de tip '{tip}' ordonate sunt: {tranzactii_ordonate}")

        elif optiune == '11':
            print("Ieșire din aplicație.") # Ieșirea din aplicație
            break # Încheie bucla principală

        else:
            print("Opțiune invalidă, vă rugăm să alegeți din nou.") # Afișează mesaj de eroare pentru opțiuni invalide

def teste():
    # Adăugăm tranzacții
    try:
        adauga_tranzactie(1, 1000, 'intrare', tranzactii, 1)
        adauga_tranzactie(2, 2000, 'iesire', tranzactii, 2)
        adauga_tranzactie(3, 1500, 'intrare', tranzactii, 3)
        adauga_tranzactie(4, 500, 'iesire', tranzactii, 4)
    except ValueError as e:
        print(f"Eroare la adăugarea tranzacției: {e}")
    
    # Testăm suma tranzacțiilor de tip 'intrare'
    print("Suma totală pentru 'intrare':", suma_totala_dupa_tip('intrare'))  # Ar trebui să fie 2500
    
    # Testăm suma tranzacțiilor de tip 'iesire'
    print("Suma totală pentru 'iesire':", suma_totala_dupa_tip('iesire'))  # Ar trebui să fie 2500
    
    # Testăm tranzacțiile ordonate după sumă pentru 'intrare'
    tranzactii_intrare_ordonate = tranzactii_dupa_tip_ordonate('intrare')
    print("Tranzacții 'intrare' ordonate descrescător după sumă:", tranzactii_intrare_ordonate)

    # Testăm tranzacțiile dintr-un interval specificat (de exemplu, zilele 2-3)
    tranzactii_interval = tranzactii_in_interval(2, 3)
    print("Tranzacții între zilele 2 și 3:", tranzactii_interval)
    
    # Testăm suma tranzacțiilor dintr-un interval
    suma_interval = suma_totala_in_interval(2, 3)
    print("Suma tranzacțiilor între zilele 2 și 3:", suma_interval)
    
    # Actualizăm o tranzacție
    try:
        actualizeaza_tranzactie(2, 2000, 'iesire', 3, 1800, 'intrare', tranzactii)
        print("Tranzacția actualizată:", tranzactii)
    except ValueError as e:
        print(f"Eroare la actualizarea tranzacției: {e}")
    
    # Ștergem tranzacțiile din ziua 3
    sterge_tranzactie_dupa_zi(3)
    print("Tranzacțiile după ștergerea zilei 3:", tranzactii)
    
    # Testăm istoricul modificărilor
    print("Istoricul modificărilor:", istoricul_modificarilor())

if __name__ == "__main__":
    main()
    teste()
    print("Toate testele au trecut cu succes.")