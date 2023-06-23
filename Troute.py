# import biblioteki i funkcji
import math
from geopy.geocoders import Nominatim

# definicja klasy
class Troute():

    # konstruktor domyslny
    def __init__(self) -> None:
        # inicjalizacja zmiennych
        self.start_lat = None
        self.start_lon = None
        self.end_lat = None
        self.end_lon = None
        self.points = None
        self.R=6371
        self.total_dist = 0
    
    #definicja metody do sprawdzenia czy uzytkownik podal poczatkowe i koncowe koordynaty
    def check(self):
        if self.start_lat != None and self.start_lon != None and self.end_lat != None and self.end_lon != None:
            return True
        else: return False
    # definicja metody do obliczenia dystancji
    def calc_distance(self, lat1, lon1, lat2, lon2):
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2- lon1)
        a = (math.sin(dlat / 2)) ** 2 + (math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (math.sin(dlon / 2)) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return self.R * c
    
    # definicja metody do obliczenia kata pomiedzy dwoma punktani koordynat
    def calc_bearing(self, lat1, lon1, lat2, lon2):
        a = math.sin(math.radians(lon2-lon1)) * math.cos(math.radians(lat2))
        b = math.cos(math.radians(lat1))*math.sin(math.radians(lat2)) - math.sin(math.radians(lat1))*math.cos(math.radians(lat2))*math.cos(math.radians(lon2-lon1))
        return math.atan2(a,b)

    # definicja metody do obliczenia punktow trasy
    def calc_points(self, fileVar):
        i = 0
        while i + 1 < len(self.points[0]):
            distance = self.calc_distance(self.points[1][i], self.points[0][i], self.points[1][i+1], self.points[0][i+1])
            self.total_dist+=distance
            initial_bearing = self.calc_bearing(self.points[1][i], self.points[0][i], self.points[1][i+1], self.points[0][i+1])
            segment_length = 0.5
            num_segments = math.ceil(distance / segment_length)
            lat1 = math.radians(self.points[1][i])
            lon1 = math.radians(self.points[0][i])
            
            insert_index = i + 1  # Initialize insert_index with i + 1
            # dopelnienie trasy
            for k in range(num_segments):
                d = k * segment_length
                lat = math.asin(math.sin(lat1) * math.cos(d/self.R) + math.cos(lat1) * math.sin(d/self.R) * math.cos(initial_bearing))
                lon = lon1 + math.atan2(math.sin(initial_bearing) * math.sin(d/self.R) * math.cos(lat1), math.cos(d/self.R) - math.sin(lat1) * math.sin(lat))
                self.points[0].insert(insert_index, math.degrees(lon))
                self.points[1].insert(insert_index, math.degrees(lat))
                fileVar.speed.insert(insert_index, fileVar.speed[i])
                fileVar.heading.insert(insert_index, fileVar.heading[i])
                fileVar.destination.insert(insert_index, fileVar.destination[i])
                fileVar.time.insert(insert_index, fileVar.time[i])
                insert_index += 1  # Increment insert_index by 1 for each segment insertion
            i = insert_index
    
    # definicja metody do zwracania f-stringa z adresem
    def get_address(self):
        return (f"{self.convert_address(self.start_lat, self.start_lon)} — {self.convert_address(self.end_lat, self.end_lon)}")

    # definicja metody do pobierania adresu
    def convert_address(self, latitude, longitude):
        # initialize Nominatim geocoder
        geolocator = Nominatim(user_agent="my_app")
        try:
            # load address by location poind and convert it to human-readable address
            location = geolocator.reverse(f"{latitude}, {longitude}").address
            # zwracanie pobranego adresu
            return location
        except:
            # zwracanie stringa z informacja w razie niepowdzenia pobrania adresu
            return "Address have not been determined"
        
    # metoda do usuniecia punktow w ktorych predkosc jest rowna 0
    def create_route(self, fileVar):
        non_zero_indices = [i for i in range(len(fileVar.speed)) if fileVar.speed[i] != "0" and fileVar.speed[i] != "0.1"]

        self.points[0] = [self.points[0][i] for i in non_zero_indices]
        self.points[1] = [self.points[1][i] for i in non_zero_indices]
        fileVar.speed = [fileVar.speed[i] for i in non_zero_indices]
        fileVar.heading = [fileVar.heading[i] for i in non_zero_indices]
        fileVar.destination = [fileVar.destination[i] for i in non_zero_indices]
        fileVar.time = [fileVar.time[i] for i in non_zero_indices]