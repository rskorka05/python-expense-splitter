import json

PLIK = "dziennik_lektury.json"
GATUNKI = ("popularnonaukowa", "podręcznik", "biografia", "historia", "filozofia", "inna")

def zapisz_plik(ksiazki, sesje, nazwa_pliku):
    dane = {
        "ksiazki": ksiazki,
        "sesje": sesje
    }

    with open(nazwa_pliku, "w", encoding="utf-8") as plik:
        json.dump(dane, plik, ensure_ascii=False, indent=4)

def wczytaj_plik(nazwa_pliku):
    try:
        with open(nazwa_pliku, "r", encoding="utf-8") as plik:
            dane = json.load(plik)
            return  dane["ksiazki"], dane["sesje"]
    except FileNotFoundError:
        print("Nie znaleziono pliku")
        return [], []

def dodaj_ksiazke(ksiazki, tytul, gatunek, stron_total):
    if gatunek not in GATUNKI:
        print("Niepoprawny gatunek książki.")
        print(f"Dostępne gatunki: {GATUNKI}")
        return

    ksiazka = {
        "tytul": tytul,
        "gatunek": gatunek,
        "stron_total": stron_total,
        "stron_przeczytanych": 0
    }

    ksiazki.append(ksiazka)
    print(f"Dodano książkę: {tytul}")

def dodaj_sesje(sesje, ksiazki, tytul, data, strony, notatka):
    znaleziona_ksiazka = None

    for ksiazka in ksiazki:
        if ksiazka["tytul"].lower() == tytul.lower():
            znaleziona_ksiazka = ksiazka

    if znaleziona_ksiazka is None:
        print("Nie znaleziono książki o takim tytule.")
        return

    sesja = {
        "tytul": tytul,
        "data": data,
        "strony_przeczytane": strony,
        "notatka": notatka
    }

    sesje.append(sesja)

    znaleziona_ksiazka["stron_przeczytanych"] += strony

    if znaleziona_ksiazka["stron_przeczytanych"] > znaleziona_ksiazka["stron_total"]:
        znaleziona_ksiazka["stron_przeczytanych"] = znaleziona_ksiazka["stron_total"]

    print(f"Dodano sesję czytania dla książki: {tytul}")

def postep_ksiazek(ksiazki):
    if len(ksiazki) == 0:
        print("Brak dodanych książek.")
        return

    print("\n=== POSTĘP CZYTANIA ===")

    for ksiazka in ksiazki:
        procent = ksiazka["stron_przeczytanych"] / ksiazka["stron_total"] * 100

        if procent >= 100:
            status = "[PRZECZYTANA]"
        else:
            status = ""

        print(
            f"Tytuł: {ksiazka['tytul']} | "
            f"Gatunek: {ksiazka['gatunek']} |"
            f"Postęp: {ksiazka['stron_przeczytanych']}/{ksiazka['stron_total']} stron "
            f"({procent:.2f}%) {status}"
        )

def main():
    ksiazki, sesje = wczytaj_plik(PLIK)

    while True:
        print("\n=== DZIENNIK LEKTURY ===")
        print("1. Dodaj książkę")
        print("2. Dodaj sesję czytania")
        print("3. Postęp czytania")
        print("0. Zapisz i wyjdź")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            tytul = input("Podaj tytuł książki: ")

            print(f"Dostępne gatunki: {GATUNKI}")
            gatunek = input("Podaj gatunek książki: ")

            try:
                stron_total = int(input("Podaj łączną liczbę stron: "))

                if stron_total <= 0:
                    print("liczba stron musi być większa od 0.")
                else:
                    dodaj_ksiazke(ksiazki, tytul, gatunek, stron_total)

            except ValueError:
                print("Błąd: liczba stron musi być liczbą całkowitą.")

        elif wybor == "2":
            tytul = input("Podaj tytuł książki: ")
            data = input("Podaj datę sesji, np. 2026-05-01: ")

            try:
                strony = int(input("Podaj liczbę przeczytanych stron: "))

                if strony <= 0:
                    print("Liczba przeczytanych stron musi być większa od 0.")
                else:
                    notatka = input("Podaj notatkę, opcjonalnie możesz zostawić puste: ")
                    dodaj_sesje(sesje, ksiazki, tytul, data, strony, notatka)

            except ValueError:
                print("Błąd: liczba stron musi być liczbą całkowitą.")

        elif wybor == "3":
            postep_ksiazek(ksiazki)

        elif wybor == "0":
            zapisz_plik(ksiazki, sesje, PLIK)
            print("Dane zostały zapisane. Koniec programu.")
            break

        else:
            print("Niepoprawna opcja menu.")

if __name__ == "__main__":
    main()