import json

NAZWA_PLIKU = "podział_kosztow.json"
OSOBY_MAX = (2, 3, 4, 5, 6)

def wczytaj_plik(nazwa_pliku):
    try:
        with open(nazwa_pliku, "r", encoding="utf-8") as plik:
            return json.load(plik)
    except FileNotFoundError:
        print("Nie znaleziono pliku.")
        return []

def zapisz_plik(wydatki, nazwa_pliku):
    with open(nazwa_pliku, "w", encoding="utf-8") as plik:
        json.dump(wydatki, plik, indent=4)
    print(f"Dane zapisano do pliku {nazwa_pliku}.")

def dodaj_wydatek(wydatki, osoby, data, opis, kwota, platnik):
    if platnik not in osoby:
        print("Błąd: podany płatnik nie znajduje się na liście osób.")
        return

    if kwota <= 0:
        print("Błąd: kwota musi być większa od 0.")
        return

    wydatek = {
        "data": data,
        "opis": opis,
        "kwota": kwota,
        "platnik": platnik
    }

    wydatki.append(wydatek)
    print("Dodano wydatek.")

def wyswietl_wydatki(wydatki):
    if len(wydatki) == 0:
        print("Brak zapisanych wydatków.")
    else:
        print("Lista wydatków:")
        for wydatek in wydatki:
            print(f"{wydatek['data']} | {wydatek['opis']} | {wydatek['kwota']:.2f} zł | zapłacił/a: {wydatek['platnik']}")

def rozliczenie(wydatki, osoby):
    if len(wydatki) == 0:
        print("Brak wydatków do rozliczenia.")
        return
    suma = 0

    for wydatek in wydatki:
        suma += wydatek["kwota"]

    udzial = suma / len(osoby)

    print(f"Suma wydatków: {suma:.2f} zł")
    print(f"Udział każdej osoby: {udzial:.2f} zł")

    for osoba in osoby:
        zaplacone = 0

        for wydatek in wydatki:
            if wydatek["platnik"] == osoba:
                zaplacone += wydatek["kwota"]

        bilans = zaplacone - udzial

        if bilans > 0:
            print(f"{osoba} zapłacił/a {zaplacone:.2f} zł, czyli {bilans:.2f} zł za dużo.")
        elif bilans < 0:
            print(f"{osoba} zapłacił/a {zaplacone:.2f} zł, czyli {abs(bilans):.2f} zł za mało.")
        else:
            print(f"{osoba} zapłacił/a dokładnie tyle, ile trzeba.")

def main():
    wydatki = wczytaj_plik(NAZWA_PLIKU)

    osoby_input = input("Podaj imiona osób oddzielone przecinkami: ")
    osoby = [osoba.strip() for osoba in osoby_input.split(",")]

    if len(osoby) not in OSOBY_MAX:
        print("Nieprawidłowa liczba osób. Dozwolone są grupy od 2 do 6 osób.")
        return

    while True:
        print("=== PODZIAŁ KOSZTÓW ===")
        print("1. Dodaj wydatek")
        print("2. Lista wydatków")
        print("3. Rozliczenie grupy")
        print("0. Zapisz i wyjdź")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            data = input("Podaj datę, np. 2026-05-01: ")
            opis = input("Podaj opis wydatku: ")
            platnik = input("Podaj imię osoby, która zapłaciła: ")

            try:
                kwota = float(input("Podaj kwotę: "))
                dodaj_wydatek(wydatki, osoby, data, opis, kwota, platnik)
            except ValueError:
                print("Błąd: kwota musi być liczbą.")

        elif wybor == "2":
            wyswietl_wydatki(wydatki)

        elif wybor == "3":
            rozliczenie(wydatki, osoby)

        elif wybor == "0":
            zapisz_plik(wydatki, NAZWA_PLIKU)
            print("Zakończono program.")
            break

        else:
            print("Nieprawidłowa opcja. Wybierz ponownie.")

if __name__ == "__main__":
    main()