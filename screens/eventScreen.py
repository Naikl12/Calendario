from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import timedelta
from clases import *

class EventScreen(tk.Frame):
    '''Ventana que muestra un evento, recibe un evento    '''
    def __init__(self, parent, mananger, event_to_show):
        super().__init__(parent)
        self.mananger = mananger
        self.parent = parent
        parent.title("Evento")
        parent.geometry("400x300+300+200") 
        self.grid()
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.resizable(False, False)

        my_event = MyEvent(event_to_show)

        event_name = ttk.Label(self, text =f'Título: {my_event.title}')
        event_name.grid(pady=20)
        datetime_event = ttk.Label(self, text= f'{my_event.date}, {my_event.time} - {my_event.get_event_time() + timedelta(hours=1)}')
        datetime_event.grid(pady=20)
        event_duration = ttk.Label(self, text= "Duración: 1 hora")
        event_duration.grid(pady=20)
        event_description = ttk.Label(self, text=f'Descripción: {my_event.description}')
        event_description.grid(pady=20)
        if my_event.is_important:
            res = 'Si'
        else:
            res = 'No'
        event_importancy = ttk.Label(self, text=f'Es importante: {res}')
        event_importancy.grid(pady=20)

        btn_close = ttk.Button(self, text="Cerrar", command=parent.destroy)
        btn_close.grid(pady=20)