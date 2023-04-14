from tkinter import *
import tkinter as tk
from tkinter import ttk

class DeleteScreen(tk.Frame):
    def __init__(self, parent, mananger):
        super().__init__(parent)
        self.mananger = mananger
        self.parent = parent
        parent.title("Busqueda") 
        parent.geometry("400x300+300+200") 
        self.grid()
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        #parent.resizable(False, False)

        self.eventName = tk.StringVar()

        ttk.Label(self, text="Buscar evento")
        ttk.Entry(self, textvariable=self.eventName).grid(pady=20)
        #falta buscar por etiquetas

        btn_delete = ttk.Button(self, text="Borrar", command=self.delete_event)
        btn_delete.grid(pady=20)

        parent.bind('<Return>', lambda e: btn_delete.invoke()) # para ejecutar el btn al presionar enter
    
    def delete_event(self):
        print(f"Guardados los datos: ") 
        self.parent.destroy()