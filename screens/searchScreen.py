from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from clases import *
from .eventScreen import *
from screens.createScreen import CreateEvent

class SearchScreen(tk.Frame):
    def __init__(self, parent, mananger):
        super().__init__(parent)
        self.mananger = mananger
        self.parent = parent
        parent.title("Busqueda") 
        parent.geometry("400x500+200+50") 
        self.grid()
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        self.event_title = tk.StringVar()

        self.frame_search = ttk.Frame(self)
        self.frame_search.grid(row=0, column=0, sticky=tk.NSEW)
        ttk.Label(self.frame_search, text="Ingresa el título de tu evento!").grid(row=0, column=1, pady=20)
        ttk.Entry(self.frame_search, textvariable=self.event_title).grid(row=1, column=1, pady=20)
        btn_search = ttk.Button(self.frame_search, text="Buscar", command= self.search_event)
        btn_search.grid(row=2, column=1, pady=5)

        parent.bind('<Return>', lambda e: btn_search.invoke())
    
    def search_event(self):
        show_list = controller.search_title_event(self.event_title.get())
        listbox_event = Listbox(self.frame_search, selectmode=SINGLE)
        listbox_event.config(width=40, height=10)
        listbox_event.grid(row=3, column=1, pady=20)
        btn_search = ttk.Button(self.frame_search, text="Ver evento", command= lambda: self.show_event(listbox_event, show_list))
        btn_search.grid(row=4, column=1, pady=5)
        btn_search = ttk.Button(self.frame_search, text="Eliminar", command= lambda: self.delete_event(listbox_event, show_list, self.mananger))
        btn_search.grid(row=5, column=1, pady=5)
        btn_search = ttk.Button(self.frame_search, text="Modificar", command= lambda: self.modify_event(listbox_event, show_list))
        btn_search.grid(row=6, column=1, pady=5)
        if show_list != False:
            for i, event in enumerate(show_list):
                listbox_event.insert(i, f'{event["title"]}, {event["date"]}, a hs {event["time"]}.')
        else:
            listbox_event.insert(0, 'No se encontraron eventos.')

    def show_event(self, listbox_e, list_e):
        i = int(listbox_e.curselection()[0])
        date_e = list_e[i]['date']
        time_e = list_e[i]['time']
        find_event = controller.get_event_index(controller.search_event_index(date_e, time_e))
        self.show_window(EventScreen, find_event)
        
    def delete_event(self, listbox_e, list_e, mananger):
        i = int(listbox_e.curselection()[0])
        date_e = list_e[i]['date']
        time_e = list_e[i]['time']
        controller.delete_event_index(controller.search_event_index(date_e, time_e))
        listbox_e.delete(i)
        mananger.live_week(datetime.strptime(mananger.week_being_watch, ('%d-%m-%Y')))

    def modify_event(self, listbox_e, list_e,):
        self.parent.geometry("550x500+200+50")
        frame_modify = Frame(self)
        frame_modify.grid(row=0, column=1, padx=15)
        i = int(listbox_e.curselection()[0])
        date_e = list_e[i]['date']
        time_e = list_e[i]['time']
        index_event = controller.search_event_index(date_e, time_e)
        event = controller.get_event_index(index_event)

        self.event_name = tk.StringVar()
        self.event_date = tk.StringVar()
        self.event_time = tk.StringVar()
        self.event_duration = tk.IntVar()
        self.description = tk.StringVar()
        self.is_important = tk.BooleanVar()

        ttk.Label(frame_modify, text="Nombre del evento", padding=3).grid(row=1, column=1, pady=10) 
        entry = ttk.Entry(frame_modify, textvariable=self.event_name)
        entry.delete(0, END)
        entry.insert(0, event['title'])
        entry.grid(row=1, column=2)
        ttk.Label(frame_modify, text="Fecha").grid(row=2, column=1, pady=10) 
        entry = ttk.Entry(frame_modify, textvariable=self.event_date)
        entry.delete(0, END)
        entry.insert(0, event['date'])
        entry.grid(row=2, column=2)
        ttk.Label(frame_modify, text="Hora", padding=3).grid(row=3, column=1, pady=10) 
        entry = ttk.Entry(frame_modify, textvariable=self.event_time)
        entry.delete(0, END)
        entry.insert(0, event['time'])
        entry.grid(row=3, column=2)
        entry = ttk.Label(frame_modify, text="Duración", padding=3).grid(row=4, column=1, pady=10) 
        entry = ttk.Entry(frame_modify, textvariable=self.event_duration)
        entry.delete(0, END)
        entry.insert(0, 1)
        entry.grid(row=4, column=2)
        ttk.Label(frame_modify, text="Descripción", padding=3).grid(row=5, column=1, pady=10) 
        entry = ttk.Entry(frame_modify, textvariable=self.description)
        entry.delete(0, END)
        entry.insert(0, event['description'])
        entry.grid(row=5, column=2)
        ttk.Label(frame_modify, text="Es importante", padding=3).grid(row=6, column=1, pady=10)
        ttk.Checkbutton(frame_modify, text="Si", variable=self.is_important).grid(row=6, column=2)   
        btn_save = ttk.Button(frame_modify, text="Guardar", padding=3, command= lambda: self.save_change(index_event))
        btn_save.grid(row=7, column=2)

    def save_change(self, i):
        new_event = MyEvent(self.event_date.get(), self.event_time.get(), self.event_name.get(),
                           self.description.get(), self.is_important.get())
        validation_event = CreateEvent.validate_title(new_event.title) and CreateEvent.validate_date(new_event.date) and CreateEvent.validate_time(new_event.time)
        if validation_event:
            res = controller.modify_event_index(i, new_event)
            if res == True:
                self.mananger.live_week(datetime.strptime(self.mananger.week_being_watch, ('%d-%m-%Y')))
                messagebox.showinfo('Evento modificado', message='El evento se ha modificado exitosamente.')
            else:
                messagebox.showerror("Evento No Guardado",message="Ya existe un evento en ese dia y horario.")
            self.parent.destroy()
        else:
            messagebox.showerror("Evento No Guardado",message="Datos invalidos.\nFormato: Título entre 1 y 10 carácteres,\nFecha: dd-mm-aaaa y\nHora: hh:00 (sin minutos)")
            self.parent.destroy()

    def show_window(self, window, event):
        '''Metodo que instancia y muestra una ventana secundaria pasada por parametro'''
        toplevel = tk.Toplevel(self.parent)
        window(toplevel, self, event).grid()