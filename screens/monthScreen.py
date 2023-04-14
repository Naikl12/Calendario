from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import *
import calendar

class MonthScreen(tk.Frame):
    def __init__(self, parent, mananger):
        super().__init__(parent)
        self.mananger = mananger
        self.parent = parent
        parent.title("Evento") 
        parent.geometry("1000x600+250+80") 
        self.grid()
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.es_calendar = calendar.LocaleTextCalendar(firstweekday=0, locale='es')
        
        frame_main = tk.Frame(self)
        frame_main.grid(sticky='news')

        month_show = self.es_calendar.formatmonthname(theyear= datetime.today().year, themonth= datetime.today().month, width=1)
        label_month_year = tk.Label(frame_main, text= month_show.upper())
        label_month_year.grid(row=0, column=0, pady=(5, 0), sticky=NSEW)

        frame_canvas = tk.Frame(frame_main)
        frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        frame_canvas.grid_propagate(False)

        canvas = tk.Canvas(frame_canvas)
        canvas.grid(row=0, column=0, sticky=NSEW)

        vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        frame_listbox = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_listbox, anchor='nw')

        calendar_month = self.es_calendar.monthdatescalendar(year= datetime.today().year, month= datetime.today().month)
        rows = len(calendar_month)
        columns = len(calendar_month[0])
        print('Calendario: ', calendar_month, 'rows', rows, 'columns', columns)
        day_box = [[Listbox() for j in range(columns)] for i in range(rows)]
        for week, week_dates in enumerate(calendar_month):
            for day, day_date in enumerate(week_dates):
                day_box[week][day] = Listbox(frame_listbox, selectmode=SINGLE, selectbackground = '#f15bb5',
                                       selectforeground = '#000000', selectborderwidth=0)
                day_box[week][day].config(width=20, height=11)
                day_box[week][day].grid(row=week, column=day, sticky='news')
                day_box[week][day].insert(0, day_date.day)
                day_box[week][day].itemconfig(0,{'bg':'#9b5de5'})

        frame_listbox.update_idletasks()

        first7columns_width = sum([day_box[0][j].winfo_width() for j in range(0, 7)])
        frame_canvas.config(width= first7columns_width + vsb.winfo_width(), height= 500)

        canvas.config(scrollregion=canvas.bbox("all"))
                

        


