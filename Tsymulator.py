# import bibliotek
import folium
import os
import tkinter as tk

# import parent class
from Tinterface import Tinterface

# definicja klasy pochodnej, rozszerzenie o metody do zapisywania mapy
class Tsymulator(Tinterface):

    # konstruktor z parametrem
    def __init__(self, master) -> None:
        # wywolanie konstruktora klasy nadrzednej
        super().__init__(master)
    
    
    
    #Okienko do wprowadenia nazwy mapy
    def put_map_name(self):
        def save_name():
            # Pobieranie danych od uytkownika
            name = entr.get()
            # Zniszczenie okna do wprowadzenia danych
            map_save.destroy()
            # wywolanie funkcji
            self.load(name)
        # tworzenie okna oraz nadanie mu nazwy
        map_save = tk.Tk()
        map_save.title("Set map title")
        # tworzenie obiektu
        save_map = Tsymulator(map_save)
        # wywolanie metody do tworzenia widzetu napisu
        save_map.create_label("Set map title", 0,0, 1,0 , (12,0))
        # wywolanie metody do tworzenia widetu do wprowadzenia danych przez uzytkownika
        entr = save_map.create_entry()
        # ukladanie widzetu
        entr.grid(column=0,row=1, padx=20, pady=12)
        # wywolanie metody do tworzenia przycisku
        save_map.create_button("Condirm", 0, 2, save_name, 1,0,(0,18))

    # procedure to create and save the map
    def load(self, route, plot_app, name = None):
        # sprawdzenie czy zostal podany argument podczas wywolania funkcji
        if name == None:
            # wywolanie metody klasy Troute
            name = route.get_address()

        m, i, voyage = folium.Map(), 0, []
        # tworzenie z listy koordynat drogi listy z podlistami z pojedynczymi koordynatami
        for lat in route.points[1]:
            voyage.append([lat, route.points[0][i]])
            i+=1
        # Create a polyline object using the route coordinates
        line = folium.PolyLine(locations=voyage, weight=5)
        # Add the polyline object to the map
        line.add_to(m)
        # Zoom the map to fit the entire route
        m.fit_bounds(line.get_bounds())
        # Ustawienie nazwy pliku, zamiana niedozwolonych znakow
        filename = name + ".html"
        filename = filename.replace('*', '').replace('/', '').replace('\\', '').replace(':', '').replace('?', '').replace('<', '').replace('>', '').replace('"', '').replace('|', '')
        try:
            # Save the map
            m.save(filename)
        except:
            # Cleaning file name
            filename = os.path.basename(filename)
            try:
                # Try to save the map with cleaned map
                m.save(filename)
            except:
                # Propozycja uzytkownikowi ustawic nazwe mapy
                response = plot_app.create_askokcancel("Cannot use this name", "Would you like to enter the name for map?")
                if response == True:
                    # funkcja tworzaca okienko do wprowadzania nazwy pliku
                    self.put_map_name()
            else:
                # Komunikat w razie udanego zapisu pliku z mapa
                plot_app.create_info("Success", "Map saved")
        else:
                # Komunikat w razie udanego zapisu pliku z mapa
                plot_app.create_info("Success", "Map saved")
