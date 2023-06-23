# importowanie bibliotek
import tkinter as tk
import tkinter.messagebox as mbox

# definicja klasy do tworzenia okna
class Tinterface:
    
    # konstruktor z parametrem
    def __init__(self, master) -> None:
        # definicja i ustawienie pola
        self.master = master
    
    # definicja metody do tworzenia i wyswietlania widzetu napisu
    def create_label(self, text, column, row, columnspan=1, padx=0, pady=0, 
                     sticky = None, size=10, master = None):
        if master == None:
            master = self.master
        tk.Label(master, text=text, font = ("Arial", size)
                 ).grid(column=column, row=row, columnspan=columnspan, padx = padx, pady=pady, sticky=sticky)
    
    # definicja metody do zwracania umieszczonego napisu
    def ret_lab(self, text, column, row, columnspan=1, padx=0, pady=0, 
                     sticky = None, size=10, master = None):
        lab = self.return_label(text, size, master)
        lab.grid(column=column, row=row, columnspan=columnspan, padx = padx, pady=pady, sticky=sticky)
        return lab

    # definicja metody do tworzenia i zwracania widzetu napisu
    def return_label(self, text, size=10, master = None):
        if master == None:
            master = self.master
        return tk.Label(master, text=text, font = ("Arial", size))
    
    # definicja metody do tworzenia i wyswietlania widzetu przycisku
    def create_button(self, text, column, row, command, columnspan=1, padx=0, pady=0, 
                      sticky=None, width=None, height=None, size=10,  master = None):
        if master == None:
            master = self.master
        tk.Button(master, text=text, font = ("Arial", size), command=command, 
                  width=width, height=height).grid(column=column, row=row, columnspan=columnspan, 
                                                   padx=padx, pady=pady, sticky=sticky)

    # definicja metody do tworzenia i zwracania widzetu przycisku
    def return_button(self, text, command, master = None, width=None, height=None, size=10):
        if master == None:
            master = self.master
        return tk.Button(master, text=text, font = ("Arial", size), command=command, 
                         width=width, height=height)
    
    # definicja metody do tworzenia i zwracania widzetu do akceptowania jednowierszowego ciagu tekstowego od uzytkownika
    def create_entry(self, master = None):
        if master == None:
            master = self.master       
        return tk.Entry(master)
    
    # definicja metody do tworzenia i zwracania widzetu menu
    def create_menu(self, lst_option_variable, a, var = "", dictionary=None, master = None):
        if master == None:
            master = self.master
        option_variable = tk.StringVar(master)
        option_variable.set(var)
        lst_option_variable[a] = option_variable
        if dictionary!=None:
            return tk.OptionMenu(master, option_variable, *dictionary)
        else:
            return tk.OptionMenu(master, option_variable, '')
    
    # definicja metody do tworzenia i wyswitlania bledu
    def create_error(self, title, message):
        mbox.showerror(title, message)

    # definicja metody do tworzenia i wyswitlania komuniktatu z informacja
    def create_info(self, title, message):
        mbox.showinfo(title, message)

    # definicja metody do tworzenia i wyswitlania ostrzezenia
    def create_warning(self, title, message):
        mbox.showwarning(title, message)

    # definicja metody do tworzenia i wyswitlania propozycji
    def create_askokcancel(self, title, message):
        return mbox.askokcancel(title, message)   