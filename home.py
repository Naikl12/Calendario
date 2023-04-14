from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import *
import calendar
from tkinter import messagebox
from screens.eventScreen import EventScreen
from screens.createScreen import CreateEvent
from screens.searchScreen import SearchScreen
from screens.monthScreen import MonthScreen
from clases import *

class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        parent.title("Calendario")
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=5)
        self.rowconfigure(1, weight=1)
        stl = ttk.Style()
        stl.configure('Wild.TButton', foreground='#f72585', width=10)
        stl.map('Wild.TButton', foreground = [('active', '#2d00f7')])
        stl.configure('Black.TButton', foreground='black', width=10)
        stl.map('Black.TButton', foreground = [('active', 'black')])
        #contiene los dias de la semana con su fecha
        self.labels_week = []
        #contiene las horas de los dias de la semana
        self.btn_hours = []
        #primer día de la vista de la semana, inicia con el día actual
        self.week_being_watch = datetime.today().date().strftime('%d-%m-%Y')
        self.es_calendar = calendar.LocaleTextCalendar(firstweekday=0, locale='es')

        #Seccion del menu
        frame_menu = ttk.Frame(self)
        frame_menu.grid(row=1, column=1,padx=10, pady=20, sticky=tk.NSEW)
        frame_menu.columnconfigure(0, weight=1)
        for i in range(0, 5):
            frame_menu.rowconfigure(i, weight=1)

        ttk.Button(
            frame_menu, text="+ Nuevo evento",
            command = lambda: self.show_window(CreateEvent),
            ).grid()
        ttk.Button(
            frame_menu, text="Buscar evento",
            command = lambda: self.show_window(SearchScreen)
            ).grid()
        ttk.Button(
            frame_menu, text="Mostrar mes",
            command = lambda: self.show_window(MonthScreen)
            ).grid()
    
        #Seccion de los eventos semanales
        frame_section_events = ttk.Frame(self)
        frame_section_events.grid(row=1, column=2, sticky=tk.NSEW)
        frame_section_events.columnconfigure(1, weight=1)
        frame_section_events.rowconfigure(1, weight=1) # espacio para nombre del mes
        frame_section_events.rowconfigure(2, weight=20) #espacio para los eventos

        # Seccion botones y fecha, mes y año actual
        frame_month = ttk.Frame(frame_section_events)
        frame_month.columnconfigure(1, weight=1) 
        frame_month.columnconfigure(2, weight=2)
        frame_month.columnconfigure(3, weight=1)
        frame_month.rowconfigure(1, weight=1)
        frame_month.grid(row=1, column=1, sticky=tk.NSEW)
        #  Nombre del mes actual
        self.label_month = ttk.Label(frame_month, text="Marzo 2023")
        self.label_month.grid(row=1, column=2, sticky=tk.NSEW)
        self.label_month.config(anchor="center")
        #  Boton semana anterior
        button_back = ttk.Button(frame_month, text="Semana anterior", command= self.back_week)
        button_back.grid(row=1, column=1, sticky=tk.NSEW)
        #  Boton semana siguiente
        button_next = ttk.Button(frame_month, text="Semana siguiente", command= self.next_week)
        button_next.grid(row=1, column=3, sticky=tk.NSEW)

        #Seccion muestra la semana
        frame_week = ttk.Frame(frame_section_events)
        frame_week.grid(row=2, column=1, sticky=tk.NSEW)
        for i in range(1,8):
            frame_week.columnconfigure(i, weight=1)
        frame_hours = ttk.Frame(frame_week)
        frame_hours.grid(row=1, column=0, sticky=tk.NSEW)
        frame_hours.rowconfigure(1, weight=1)
        for j in range (0, 24):
            btn_hour = ttk.Button(frame_hours, text=j)
            btn_hour.grid(row=j+2, column=1, sticky=tk.NSEW)
        self.week = {"Monday": "lunes", "Tuesday":"martes", "Wednesday":"miércoles", "Thursday":"jueves", "Friday":"viernes", "Saturday":"sábado", "Sunday":"domingo"}
        
        for i, day_label in enumerate(self.week, start=1):
            frame_days = ttk.Frame(frame_week)
            frame_days.grid(row=1, column=i, sticky=tk.NSEW)
            frame_days.columnconfigure(1, weight=1)
            day_label = ttk.Label(frame_days, text=f'{self.week.get(day_label)}\n{i}')
            day_label.grid(row=1, column=1, sticky=tk.NSEW)
            hours = [] #contiene una lista de horas de un dia
            for j in range (0, 24):
                btn_hour = ttk.Button(frame_days, text=" ")
                btn_hour['command'] = lambda hour = j, day = i: self.show_event(day, hour, EventScreen)
                btn_hour.grid(row=j+2, column=1, sticky=tk.NSEW)
                hours.append(btn_hour)
            self.btn_hours.append(hours) 
            self.labels_week.append(day_label)

        self.live_week(datetime.today())

    def live_week(self, tuday):
        '''Actualiza los eventos que se muestran en la semana'''
        month_show = self.es_calendar.formatmonthname(theyear= tuday.year, themonth= tuday.month, width=1)
        self.label_month['text'] = month_show.upper()
        td = timedelta(1)
        for i, day_label in enumerate(self.labels_week):
            day_label['text'] = f'{self.week[tuday.strftime("%A")]}\n{tuday.day}'
            for hour, btn in enumerate(self.btn_hours[i]):
                btn['text'] = ' '
                event_find = controller.search_event(str(tuday.date().strftime('%d-%m-%Y')), str(hour)+ ':00')
                if event_find:
                    btn['text'] = event_find['title']
                    if event_find['is_important'] == True:
                        btn['style'] = 'Wild.TButton'
                    else:
                        btn['style'] = 'Black.TButton'
            tuday+=td

    def next_week(self):
        '''Muestra la siguiente semana'''
        week_to_show = datetime.strptime(self.week_being_watch, '%d-%m-%Y') + timedelta(7)
        self.live_week(week_to_show)
        self.week_being_watch = week_to_show.strftime('%d-%m-%Y')

    def back_week(self):
        '''Muestra la semana anterior'''
        week_to_show = datetime.strptime(self.week_being_watch, '%d-%m-%Y') - timedelta(7)
        self.live_week(week_to_show)
        self.week_being_watch = week_to_show.strftime('%d-%m-%Y')

    def show_window(self, window):
        '''Metodo que instancia y muestra una ventana secundaria pasada por parametro'''
        toplevel = tk.Toplevel(self.parent)
        window(toplevel, self).grid()

    def show_event(self, day_week, hour, window):
        '''Abre una ventana y muestra el evento'''
        find_day = datetime.strptime(self.week_being_watch, '%d-%m-%Y') + timedelta(day_week-1)
        res = controller.search_event_index(str(find_day.date().strftime('%d-%m-%Y')), str(hour)+ ':00')
        if res:
            find_event = controller.get_event_index(res)
            toplevel = tk.Toplevel(self.parent)
            window(toplevel, self, find_event).grid()
        else:
            messagebox.showinfo('Sin evento', message='Hora libre')

root = tk.Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
App(root).grid(sticky=tk.NSEW)
root.geometry('1200x650+100+10')
root.minsize(800, 700)
root.iconbitmap('./calendar_icon.ico')

root.mainloop()