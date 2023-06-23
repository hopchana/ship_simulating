# import modulu i clasy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# definicja klasy tworzacej wykres
class Tplot():
    
    #konstruktor z parametrami 
    def __init__(self, master, points) -> None:
        # definicja pol
        self.x = points[0]
        self.y = points[1]
        self.count =0
        self.master = master

    # definicja metody do wyswielania wykresu w oknie Tk
    def create_plot(self, xlabel, ylabel, row, column, rowspan, height, width):
        # Create a Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(width, height))
        # ustawianie nazw osi
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        # wyswietlanie linii siatki
        self.ax.grid(True)
        self.line, = self.ax.plot([], [])

        # Create a canvas to display the figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = row, column = column, rowspan=rowspan)

    # definicja metody do aktualizacji wykresu
    def update_plot(self, count):
        # dodanie koordynat do wykresu
        self.line.set_data(self.x[:count], self.y[:count])
        
        # wyswietlanie wykresu w procesie tworzenia
        self.canvas.draw()