Wizualizacja ruchu statków na podstawie danych GPS z pliku. Program daje możliwość wyboru jaki statek (LRIMOShipNo) oraz dni, z których powinna byc wyświetlona trasa.

main.py - plik główny programu;

TdealWithFile - klasa do wczytywania danych z pliku i wykonania operacji na nich;

Tinterface - klasa do tworzenia obiektów w oknie;

Tsymulator - klasa pochodna od klasy Tinterface, dodanie metod do zapisywania mapy;

Tplot - klasa tworząca wykres;

Troute - klasa do filtrowania i dopełniania koordynat oraz pobierania adresu;

baza_statki_cargo_wybrane.csv - plik z danymi.
