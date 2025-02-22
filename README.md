Visualization of Ship Movement Based on GPS Data from a File

The program allows users to select a specific ship (LRIMOShipNo) and choose the days for which the route should be displayed.

main.py – Main program file

TdealWithFile – Class for loading data from a file and performing operations on it

Tinterface – Class for creating objects in the window

Tsymulator – Derived class from Tinterface, adding methods for saving the map

Tplot – Class for generating charts

Troute – Class for filtering and completing coordinates, as well as retrieving addresses

baza_statki_cargo_wybrane.csv – File containing the data
