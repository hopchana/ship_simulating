import csv
import tkinter as tk

# klasa do wczytywania pliku i operacji na nim

class TdealWithFile:
    def __init__(self) -> None:
        # inicjalizacja pol
        self.lines=self.readFile()
        self.ship_arr=[]
        self.detShips()
        self.date=[]
        self.detDates()
        self.years=[]
        self.detYears()  
        self.eDate = None
        self.sDate = None

    def readFile(self):
        lines_arr=[]
        wier=0
        a=""
        # Otwórz plik CSV do odczytu
        with open('baza_statki_cargo_wybrane.csv', 'r') as file:
            reader = csv.reader(file)
            # Iteruj przez wiersze w pliku
            for row in reader:
                line = row[0]
                # sprawdzenie czy linia sklada sie z dwoch elementow (czy jest posrod linii przecinek)
                try:
                    line+="."+row[1]
                except:
                    pass
                kol = 0
                # dodanie podlisty dla kolejnego wiersza danych
                lines_arr.append([])
                # dodanie zerowego elementu(pustego stringa) do listy
                # aby uniknac IndexError: list index out of range
                lines_arr[wier].append(a)
                # dodanie wiersza znak po znaku
                for sg in line:
                    # sprawdzenie czy nie jest to koniec kolumny
                    if not sg==";":
                        # dodanie kolejnego znaku
                        lines_arr[wier][kol]+=sg
                    else:
                        # dodanie nowego elementu w podliste z wierszem dla kolejnej kolumny
                        kol+=1
                        lines_arr[wier].append(a)
                wier+=1
        # usuniecie pierwszego elementu z naglowkami kolumn
        lines_arr.pop(0)
        return lines_arr

    def detShips(self):
        # choosing unique ships
        for i in self.lines:
            if not i[0] in self.ship_arr:
                self.ship_arr.append(i[0])
        count = 0
        arr=[]
        # rodzielenie linii roznych statkow na rozne listy
        for i in self.ship_arr:
            # dodanie podlisty dla danych kolejnego statku
            arr.append([])
            # iteracja po wszystkich liniach
            for k in self.lines:
                # sprawdzenie numeru statku
                if k[0]==i:
                    arr[count].append(k)
            count+=1
        self.lines=arr
    
    def takeData(self, i, k, lon_arr, lat_arr):
        self.time.append(self.lines[i][k][3])
        self.heading.append(self.lines[i][k][7])
        self.moveStatus.append(self.lines[i][k][6])
        try:
            self.speed.append(self.lines[i][k][9])
        except:
            try:
                self.speed.append([-1])
            except:
                self.speed.append("")
        try:
            self.destination.append(self.lines[i][k][10])
        except:
            try:
                self.destination.append(self.destination[-1])
            except:
                self.destination.append("")

        lon_arr.append(float(self.lines[i][k][5]))
        lat_arr.append(float(self.lines[i][k][4]))
        return k+1
        

    def define_points(self, startDay, startMonth, startYear, endDay, endMonth, endYear, shipInd):
        self.time=[]
        self.heading=[]
        self.moveStatus=[]
        self.speed = []
        self.destination = []
        lat_arr, lon_arr=[], []
        i=0
        # poszukiwanie numeru podlisty w ktorej znajduja sie dane statku
        while (self.ship_arr[i]!=shipInd):
                i+=1
        # ustawienie danych statku
        self.id = self.lines[i][0][0]
        self.name = self.lines[i][0][1]
        self.type = self.lines[i][0][2]
        self.draught = self.lines[i][0][8]
        # tworzenie stringa z data w zapisie jak w liniach
        self.sDate = startYear+"-"+startMonth+"-"+startDay
        self.eDate = endYear+"-"+endMonth+"-"+endDay
        # poszukiwanie indeku linii z poczatkowa data
        for k in range(len(self.lines[i])):
            if self.lines[i][k][3][0:10]==self.sDate:
                break
        # pobieranie danych od daty poczatku do daty konca
        while (self.lines[i][k][3][0:10]!=self.eDate):
            k = self.takeData(i, k, lon_arr, lat_arr)
        # pobieranie danych z daty konca
        while(self.lines[i][k][3][0:10]==self.eDate):
            k = self.takeData(i, k, lon_arr, lat_arr)
            # sprawdzenie czy nie jest to ostatni element w liscie
            if k==len(self.lines[i]):
                break

        # tworzenie listy z punktami dla wykresu
        points = []
        points.append(lon_arr)
        points.append(lat_arr)
        return points
    
    # funkcja do znajdowania wszystkich unikalnych dat
    def detDates(self):
        # choosing unique dates
        arr=[]
        count=0
        for i in self.lines:
            # tworzenie podlist dla roznych statkow
            arr.append([])
            for sg in i:
                # sprawdzenie czy taka data jeszcze nie wystapila
                if not sg[3][0:10] in arr[count]:
                    arr[count].append(sg[3][0:10])
            count+=1

        # Separating dates
        count=0
        for i in range(len(self.ship_arr)):
            self.date.append([])
            k=0
            for sg in arr[i]:
                # dzielenie daty na rok, miesiac, dzien
                self.date[count].append([])
                self.date[count][k].append(sg[0:4])
                self.date[count][k].append(sg[5:7])
                self.date[count][k].append(sg[8:10])
                k+=1
            count+=1
    # getting unique years
    def detYears(self):
        count=0
        for i in range(len(self.ship_arr)):
            self.years.append([])
            for j in self.date[i]:
                if not j[0] in self.years[count]:
                    self.years[count].append(j[0])
            count+=1


    def update_second_option_menu(self, lst_variable, second_option_menu):
        # pobieranie watosci numeru statku ustawionej w OptionMenu
        selected_option = lst_variable[0].get()
        # tworzenie listy z latami w zaleznosci od wybranego statku
        for i in range(len(self.ship_arr)):
            if self.ship_arr[i]==selected_option:
                second_options = self.years[i]
        # Ustawienie pierwszej opcji w liscie jako domyslnej
        lst_variable[1].set(second_options[0])  

        # Zaktualizuj opcje drugiego OptionMenu
        second_option_menu['menu'].delete(0, 'end')
        for option in second_options:
            second_option_menu['menu'].add_command(label=option, command=tk._setit(lst_variable[1], option))

    def update_third_option_menu(self, lst_variable, third_option_menu):
        # pobieranie watosci numeru statku ustawionej w OptionMenu
        selected_option1 = lst_variable[0].get()
        # pobieranie watosci roku ustawionej w OptionMenu
        selected_option2 = lst_variable[1].get()

        # poszukiwanie numeru podlisty w ktorej znajduja sie dane statku o tym numerze
        for i in range(len(self.ship_arr)):
            if self.ship_arr[i]==selected_option1:
                break
        third_options=[]
        # tworzenie listy z miesiacami w zaleznosci od wybranego roku
        for k in range(len(self.date[i])):
            if self.date[i][k][0]==selected_option2:
                if not self.date[i][k][1] in third_options:
                    third_options.append(self.date[i][k][1])

        lst_variable[2].set(third_options[0])  # Ustaw pierwszą opcję jako domyślną

        # Zaktualizuj opcje trzeciego OptionMenu
        third_option_menu['menu'].delete(0, 'end')
        for option in third_options:
            third_option_menu['menu'].add_command(label=option, command=tk._setit(lst_variable[2], option))

    def update_fourth_option_menu(self, lst_variable, fourth_option_menu):
        # ship
        selected_option1 = lst_variable[0].get()
        # year
        selected_option2 = lst_variable[1].get()
        # month
        selected_option3 = lst_variable[2].get()

        # poszukiwanie numeru podlisty w ktorej znajduja sie dane statku o tym numerze
        for i in range(len(self.ship_arr)):
            if self.ship_arr[i]==selected_option1:
                break
        fourth_options=[]

        # tworzenie listy z dniami w zaleznosci od wybranego roku i miesiaca
        for k in range(len(self.date[i])):
            if self.date[i][k][0]==selected_option2 and self.date[i][k][1]==selected_option3:
                if not self.date[i][k][2] in fourth_options:
                    fourth_options.append(self.date[i][k][2])

        lst_variable[3].set(fourth_options[0])  # Ustaw pierwszą opcję jako domyślną

        # Zaktualizuj opcje czwartego OptionMenu
        fourth_option_menu['menu'].delete(0, 'end')
        for option in fourth_options:
            fourth_option_menu['menu'].add_command(label=option, command=tk._setit(lst_variable[3], option))