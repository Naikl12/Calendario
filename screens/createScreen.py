from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from clases import *
from .eventScreen import *

class CreateEvent(tk.Frame):
    '''Ventana para crear un nuevo evento'''
    def __init__(self, parent, mananger):
        super().__init__(parent)
        self.mananger = mananger
        self.parent = parent
        parent.title("Evento") 
        parent.geometry("400x500+300+100") 
        self.grid()
        parent.resizable(False, False)
        parent.columnconfigure(0, weight=1) 
        parent.rowconfigure(0, weight=1)

        self.event_name = tk.StringVar()
        self.event_date = tk.StringVar()
        self.event_time = tk.StringVar()
        self.event_duration = tk.IntVar()
        self.description = tk.StringVar()
        self.is_important = tk.BooleanVar()

        ttk.Label(self, text="Nombre del evento", padding=3).grid(row=1, column=1, pady=10) 
        ttk.Entry(self, textvariable=self.event_name).grid(row=1, column=2)
        ttk.Label(self, text="Fecha").grid(row=2, column=1, pady=10) 
        entry = ttk.Entry(self, textvariable=self.event_date)
        entry.delete(0, END)
        entry.insert(0, datetime.today().date().strftime('%d-%m-%Y'))        
        entry.grid(row=2, column=2)
        ttk.Label(self, text="Hora", padding=3).grid(row=3, column=1, pady=10) 
        entry = ttk.Entry(self, textvariable=self.event_time)
        entry.delete(0, END)
        time_now = datetime.today()-timedelta(minutes=datetime.today().minute)
        entry.insert(0, time_now.strftime('%H:%M'))
        entry.grid(row=3, column=2)
        ttk.Label(self, text="Duración", padding=3).grid(row=4, column=1, pady=10) 
        entry = ttk.Entry(self, textvariable=self.event_duration)
        entry.delete(0, END)
        entry.insert(0, 1)
        entry.grid(row=4, column=2)
        ttk.Label(self, text="Descripción", padding=3).grid(row=5, column=1, pady=10) 
        ttk.Entry(self, textvariable=self.description).grid(row=5, column=2)
        ttk.Label(self, text="Es importante", padding=3).grid(row=6, column=1, pady=10)
        ttk.Checkbutton(self, text="Si", variable=self.is_important).grid(row=6, column=2)

        btn_save = ttk.Button(self, text="Guardar", padding=3, command=lambda: self.save_event(mananger))
        btn_save.grid(row=7, column=2)

        parent.bind('<Return>', lambda e: btn_save.invoke()) # para ejecutar el btn al presionar enter

    @classmethod
    def validate_date(cls, test_str):
        '''Valida el formato de la fecha ingresada'''
        format = '%d-%m-%Y'
        res = True
        try:
            res = bool(datetime.strptime(test_str, format))
        except ValueError:
            res = False
        return res
    
    @classmethod
    def validate_time(cls, test_str):
        '''Valida el formato de la hora ingresada'''
        format = '%H:%M'
        res = True
        try:
            res = bool(datetime.strptime(test_str, format))
            if datetime.strptime(test_str, format).minute != 0:
                res = False
        except ValueError:
            res = False
        return res
    
    @classmethod
    def validate_title(cls, title):
        if 0<len(title)<=10:
            return True
        else:
            return False
    
    def validate_event(self):
        '''Verifica los datos ingresados sean correctos o envia un mensaje de error'''
        if not self.validate_title(self.event_name.get()) or not self.validate_date(self.event_date.get()) or not self.validate_time(self.event_time.get()):
            messagebox.showerror("Evento No Guardado",message="Datos invalidos.\nFormato: Título entre 1 y 10 carácteres,\nFecha: dd-mm-aaaa y\nHora: hh:00 (sin minutos)")
            self.parent.destroy()
            return False
        else:
            return True

    def save_event(self, mananger):
        '''Guarda un evento y verifica que no exista otro en el mismo horario'''
        if self.validate_event():
            new_event = MyEvent(self.event_date.get(), self.event_time.get(), self.event_name.get(),
                            self.description.get(), self.is_important.get())
            res = controller.add_event(new_event)
            
            if res == True:
                self.refresh_btn(mananger)
                self.mananger.live_week(datetime.strptime(self.mananger.week_being_watch, ('%d-%m-%Y')))
            else:
                messagebox.showerror("Evento No Guardado",message="Ya existe un evento en ese dia y horario.")
            self.parent.destroy()

    def refresh_btn(self, mananger):
        date_start = datetime.strptime(mananger.week_being_watch, '%d-%m-%Y')
        date_end = datetime.strptime(mananger.week_being_watch, '%d-%m-%Y') + timedelta(days=7)
        date_event = datetime.strptime(self.event_date.get(), '%d-%m-%Y')
        time_event = datetime.strptime(self.event_time.get(), '%H:%M')
        if date_start <=  date_event <= date_end:
            day_today = date_start.weekday()
            day= date_event.weekday()
            hour = time_event.hour
            btn = mananger.btn_hours[day-day_today][hour]
            btn['text'] = self.event_name.get()
            if self.is_important == True:
                btn['style'] = 'Wild.TButton'
            else:
                btn['style'] = 'Black.TButton'

    def show_window(self, window, event):
        '''Metodo que instancia y muestra una ventana secundaria pasada por parametro'''
        toplevel = tk.Toplevel(self.parent)
        window(toplevel, self, event).grid()