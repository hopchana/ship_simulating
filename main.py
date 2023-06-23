# import bibliotek
import tkinter as tk

# import klas
# do wczytywania pliku i operacji na nim
from TdealWithFile import TdealWithFile
# tworzaca okno, zapisujaca mape
from Tsymulator import Tsymulator
# tworzaca droge
from Troute import Troute
# tworzaca wykres
from Tplot import Tplot

def quit_me():
    # destroy all widgets
    root.quit()
    # exit mainloop, end the application
    root.destroy()

# wywolanie metody do zapisania mapy
def load():
    app.load(route, plot_app)

def trace_callback1(*args):
    # wywolanie metod do zmiany variables w OptioMenus
    fileVar.update_second_option_menu(lst_variable, startYearMenu)
    fileVar.update_second_option_menu(Endlst_variable, endYearMenu)
    # ustawienie OptionMenus w normalny stan
    startYearMenu.configure(state='normal')
    endYearMenu.configure(state='normal')
    startMonthMenu.configure(state='normal')
    endMonthMenu.configure(state='normal')
    startDayMenu.configure(state='normal')
    endDayMenu.configure(state='normal')

def trace_callback2(*args):
    # wywolanie metody do zmiany variable w OptioMenu
    fileVar.update_third_option_menu(lst_variable, startMonthMenu)

def trace_callback3(*args):
    # wywolanie metody do zmiany variable w OptioMenu
    fileVar.update_fourth_option_menu(lst_variable, startDayMenu)

def trace_callback2e(*args):
    # wywolanie metody do zmiany variable w OptioMenu
    fileVar.update_third_option_menu(Endlst_variable, endMonthMenu)

def trace_callback3e(*args):
    # wywolanie metody do zmiany variable w OptioMenu
    fileVar.update_fourth_option_menu(Endlst_variable, endDayMenu)


#pobieranie danych od uzytkownika i ustawianie
def set_data():
    # wywolanie funkcji do pobierania i ustawiania danych
    set_date()
    # wywolanie funkcji do symulacji
    simulate()

# sprawdzenie czy sa w liscie predkosci statku niezerowe wartosci
def check_speed(speed):
    for value in speed:
        if value != "0" and value != "0.1":
            return True
    return False

# funkcja do symulacji ruchu statku
def simulate():
    # sprawdzenie czy wszystkie dane sa ustawione poprawnie
    if route.check() and len(fileVar.speed)>0:
        # jezeli statek nie stoi na jednym miejscu
        if (check_speed(fileVar.speed)):
            # wyrzucenie wszystkich nieruchomych(gdzie speed=0) koordynat
            route.create_route(fileVar)
            # dopelnienie drogi
            route.calc_points(fileVar)
        
        # create new window
        plot_master = tk.Tk()
        # nadanie tytulu oknu z wykresem
        plot_master.title(route.get_address())
        # podlaczenie do zmiennej poza funkcja
        global plot_app
        # tworzenie obiektu
        plot_app = Tsymulator(plot_master)
        
        # tworzenie obiektu
        plot = Tplot(plot_master, route.points)
        # metoda do ustawienia wygladu wykresu
        plot.create_plot("Longitude", "Latitude", 0, 1, 7, 5.5, 10)

        try:
            # ustawienie limitow wykresu
            plot.ax.set_xlim(min(plot.x)-0.5, max(plot.x)+0.5)
            plot.ax.set_ylim(min(plot.y)-0.5, max(plot.y)+0.5)
            # odznaczenie pierwszego punktu
            plot.ax.plot(plot.x[0], plot.y[0], 'bo', markersize=5)
            # iteracja po punktach
            for count in range(0, len(plot.x)):
                # ustawienie labels z informacja o statku
                l0 = plot_app.ret_lab(f"Speed: {fileVar.speed[count]}", 0, 0, 1, 10, 0, None, 14)
                l1 = plot_app.ret_lab(f"Heading: {fileVar.heading[count]} degrees", 0, 1, 1, 10, 0, None, 14)
                l2 = plot_app.ret_lab(f"Ship location: {route.points[1][count]:.2f}, {route.points[0][count]:.2f}", 0, 2, 1, 10, 0, None, 14)
                l4 = plot_app.ret_lab(f"Destination: \n{fileVar.destination[count]}", 0, 3, 1, 10, 0, None, 14)
                l5 = plot_app.ret_lab(f"Time:\n   {fileVar.time[count]}   ", 0, 4, 1, 10, 0, None, 14)
                
                # wywolanie metody dodajacej kolejne punkty do wykresy
                plot.update_plot(count)
                # method to show the plot in process
                plot_master.update()

                # markowanie punktow zmiany destination
                if fileVar.destination[count]!=fileVar.destination[count-1]:
                    plot.ax.plot(plot.x[count], plot.y[count], 'bo', markersize=5)

                # Destroy the labels so next will not be printed over and over created ones
                l0.destroy()
                l1.destroy()
                l2.destroy()
                l4.destroy()
                l5.destroy()
            # odznaczenie ostatniego punktu
            plot.ax.plot(plot.x[-1], plot.y[-1], 'bo', markersize=5)
            # Create labels with summary of the voyage
            plot_app.create_label(f"LRIMOShipNo: {fileVar.id}", 0, 0, 1, 10, 0, None, 14)
            plot_app.create_label(f"Ship name: {fileVar.name}", 0, 1, 1, 10, 0, None, 14)
            plot_app.create_label(f"Ship type: {fileVar.type}", 0, 2, 1, 10, 0, None, 14)
            plot_app.create_label(f"Total distance: {route.total_dist:.2f} km", 0, 3, 1, 10, 0, None, 14)
            plot_app.create_label(f"Start date: {fileVar.sDate}", 0, 4, 1, 10, 0, None, 14)
            plot_app.create_label(f"End date: {fileVar.eDate}", 0, 5, 1, 10, 0, None, 14)
            plot_app.create_button("Save as map", 0, 6, load, 1,0,0,None, None, None, 15)
        except:
            pass
    # wyswietlanie komunikatow o niewystarczajacych danych
    elif not route.check():
        app.create_warning("Warning", "Enter data correctly")


#ustawianie koordynat
def set_date():
    try:
        # proba ustawiania koordynat drogi
        points = fileVar.define_points(lst_variable[3].get(), lst_variable[2].get(), lst_variable[1].get(), Endlst_variable[3].get(), Endlst_variable[2].get(), Endlst_variable[1].get(), lst_variable[0].get())
        route.start_lon = points[0][0]
        route.start_lat = points[1][0]
        route.end_lon = points[0][-1]
        route.end_lat = points[1][-1]
        route.points = points
    except:
        pass

# tworzenie main window, nadanie mu tytulu
root = tk.Tk()
root.title("Symulator rejsów morskich")

# tworzenie obiektow
# klasa do tworzeia drogi
route = Troute()
# klasa do tworzenia okna oraz zapisywania mapy
app = Tsymulator(root)
# klasa do wczytywania pliku
fileVar = TdealWithFile()
# tworzenie zmiennej NoneType
plot_app = None

# create Frames to group items
chooseShipFrame = tk.Frame(app.master)
startDateFrame = tk.Frame(app.master)
endDateFrame = tk.Frame(app.master)

# create a list with variables for OptioMenus
lst_variable = [tk.StringVar(chooseShipFrame), tk.StringVar(chooseShipFrame), tk.StringVar(chooseShipFrame), tk.StringVar(chooseShipFrame)]

# create items and add them to the Frame
el1 = app.return_label("Choose ship:  ", 11, chooseShipFrame)
first_menu = app.create_menu(lst_variable, 0, "LRIMOShipNo", fileVar.ship_arr, chooseShipFrame)
el1.pack(side=tk.LEFT)
first_menu.pack(side=tk.LEFT)

# create items and add them to the Frame
el1 = app.return_label("Choose start date:  ", 11, startDateFrame)
startYearMenu = app.create_menu(lst_variable, 1, "Year", None, startDateFrame)
startMonthMenu = app.create_menu(lst_variable, 2, "Month", None, startDateFrame)
startDayMenu = app.create_menu(lst_variable, 3, "Day", None, startDateFrame)
# place items in the Frame
el1.pack(side=tk.LEFT)
startYearMenu.pack(side=tk.LEFT)
startMonthMenu.pack(side=tk.LEFT)
startDayMenu.pack(side=tk.LEFT)

# create a list with variables for OptioMenus
Endlst_variable = [lst_variable[0], tk.StringVar(chooseShipFrame), tk.StringVar(chooseShipFrame), tk.StringVar(chooseShipFrame)]

# create items and add them to the Frame
el1 = app.return_label("Choose end date:  ", 11, endDateFrame)
endYearMenu = app.create_menu(Endlst_variable, 1, "Year", None, endDateFrame)
endMonthMenu = app.create_menu(Endlst_variable, 2, "Month", None, endDateFrame)
endDayMenu = app.create_menu(Endlst_variable, 3, "Day", None, endDateFrame)
el1.pack(side=tk.LEFT)
endYearMenu.pack(side=tk.LEFT)
endMonthMenu.pack(side=tk.LEFT)
endDayMenu.pack(side=tk.LEFT)

# ustawienie OptionMenus w nieaktywny stan
startYearMenu.configure(state='disabled')
startMonthMenu.configure(state='disabled')
startDayMenu.configure(state='disabled')
endYearMenu.configure(state='disabled')
endMonthMenu.configure(state='disabled')
endDayMenu.configure(state='disabled')

# add Frames to the main Grid
chooseShipFrame.grid(row=0, column=0, columnspan=4, pady=5, padx=5)
startDateFrame.grid(row=1, column=0, columnspan=4, pady=5, padx=5)
endDateFrame.grid(row=2, column=0, columnspan=4, pady=5, padx=5)

# wywolanie metody klasy Tinterface, tworzacej przycisk
app.create_button("Simulate", 0, 12, set_data, 4, 0, 20, None, 20, None, 12)

# Bind the update function to the first OptionMenu
lst_variable[0].trace('w', trace_callback1)
lst_variable[1].trace('w', trace_callback2)
lst_variable[2].trace('w', trace_callback3)
Endlst_variable[1].trace('w', trace_callback2e)
Endlst_variable[2].trace('w', trace_callback3e)

# define what happens when the user explicitly closes a window using the window manager
root.protocol("WM_DELETE_WINDOW", quit_me)

# uruchomienie aplikacji
root.mainloop()