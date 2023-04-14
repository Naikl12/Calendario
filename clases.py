import datetime
import json
from datetime import datetime
from datetime import timedelta

class Controller():

    def __init__(self, rute):
        '''Instancia Controller'''
        self.rute = rute

    def add_event(self, data):
        '''Agrega un evento al archivo json'''
        with open(self.rute, 'r') as archive:
            data_json = json.load(archive)
        list_calendar = data_json['calendar']
        my_calendar = Ecalendar(list_calendar)
        if not my_calendar.event_already_create(data.date, data.time):
            my_calendar.add_event(data.__dict__)
            data_json['calendar'] = my_calendar.list_event
            with open(self.rute, 'w') as archive:
                json.dump(data_json, archive)
            print(f'Se agrego el evento a la lista {data_json["calendar"]}')
            return True
        else:
            print(f'No se agrego el evento a la lista {data_json["calendar"]}')
            return False
            
    def search_title_event(self, title):
        '''Devuelve la lista de eventos de un archivo que tienen determinado título'''
        with open(self.rute, 'r') as archive:
            data_json = json.load(archive)
            list_calendar = data_json['calendar']
            my_calendar = Ecalendar(list_calendar)
            return my_calendar.search_event(title)
        
    def search_event_index(self, date_event, time_event):
        '''Devuelve el indice que corresponde a la fecha y hora'''
        with open(self.rute, 'r') as archive:
            data_json = json.load(archive)
            list_calendar = data_json['calendar']
            my_calendar = Ecalendar(list_calendar)
            return my_calendar.search_event_date_hour(date_event, time_event)
        
    def search_event(self, date_event, time_event):
        '''Devuelve un evento que corresponda con la fecha y hora'''
        with open(self.rute, 'r') as archive:
            data_json = json.load(archive)
            list_calendar = data_json['calendar']
            my_calendar = Ecalendar(list_calendar)
            event_exist = my_calendar.event_already_create(date_event, time_event)
            if event_exist:
                event_index = self.search_event_index(date_event, time_event)
                return self.get_event_index(event_index)
            else:
                return False
            
    def get_event_index(self, i):
        '''Devuelve el elemento con el índice del archivo'''
        with open(self.rute, 'r') as archive:
            data_json = json.load(archive)
            list_calendar = data_json['calendar']
            my_calendar = Ecalendar(list_calendar)
            return my_calendar.get_event_index(i)
        
    def delete_event_index(self, i):
        '''Elimina el elemento con el índice del archivo'''
        with open(self.rute, 'r') as archive:
            data_json = json.load(archive)
            list_calendar = data_json['calendar']
            my_calendar = Ecalendar(list_calendar)
            my_calendar.delete_event(i)
            data_json['calendar'] = my_calendar.list_event
        with open(self.rute, 'w') as archive:
                json.dump(data_json, archive)

    def modify_event_index(self, i, event_modified):
        '''Elimina el elemento con el índice del archivo y agrega el nuevo'''
        aux = MyEvent(self.get_event_index(i))
        self.delete_event_index(i)
        if self.add_event(event_modified):
            return True
        else:
            self.add_event(aux)
            return False


class MyEvent():
    ''' Representa un evento con fecha y hora'''

    def __init__(self, *args):
        '''Instancia un evento'''
        if len(args) > 1:
            self.date = args[0]
            self.time = args[1]
            self.title = args[2]
            self.description = args[3]
            self.is_important = args[4]
        else:
            event_dict = args[0]
            self.date = event_dict['date']
            self.time = event_dict['time']
            self.title = event_dict['title']
            self.description = event_dict['description']
            self.is_important = event_dict['is_important']
        
    def modify_event(self, e_date = None, e_time = None, 
                     title = None, description = None, is_important = None):
        ''' Modifica uno o varios atributos del evento, son opcionales'''
        if e_date != None:
            self.date = e_date
        if e_time != None:
            self.time = e_time
        if title != None:
            self.time = title
        if description != None:
            self.description = description
        if is_important != None:
            self.is_important = is_important

    def get_event_description(self):
        return self.description

    def get_event_importancy(self):
        return self.is_important
    
    def get_event_title(self):
        return self.title

    def get_event_date(self):
        return self.date
    
    def get_event_time(self):
        '''Devuelve la hora en formato timedelta'''
        time_event_format = datetime.strptime(self.time, '%H:%M').time()
        hours_time = datetime.strptime(self.time, '%H:%M').time().hour
        minutes_time = datetime.strptime(self.time, '%H:%M').time().minute
        return timedelta(hours=hours_time, minutes=minutes_time)

    def __str__(self):
        return f'Fecha: {self.date}\nHora: {self.time}\nTítulo: {self.title}\nDescripción: {self.description}\nImportante: {self.is_important}'


class Ecalendar():
    '''Calendario de eventos, lista de diccionarios'''

    def __init__(self, list_event):
        self.list_event = list_event

    def add_event(self, event):
        '''Agrega un evento a la lista y ordena, recibe un objeto Event'''
        self.list_event.append(event)
        if self.list_event != []:
            print(self.list_event)
            self.list_event.sort(key = lambda x: datetime.strptime(x['date'], '%d-%m-%Y'))
        
    def delete_event(self, i):
        '''Elimina un evento de la lista'''
        self.list_event.pop(i)

    def search_event(self, title):
        '''Devuelve una lista de eventos con el título'''
        exist_event = list(e for e in self.list_event if e['title']  == title)
        if exist_event != []:
            return exist_event
        else:
            return False

    def search_event_index(self, date_e, time_e):
        '''Devuelve el indice de un evento determinado en la lista'''
        for i, my_event in enumerate(self.list_event):
            if my_event['date']  == date_e and my_event['time'] == time_e:
                return i
        return False
    
    def search_event_date_hour(self, date_e, time_e):
        '''Devuelve el indice de un evento determinado en la lista'''
        for i, my_event in enumerate(self.list_event):
            time_event = str(datetime.strptime(my_event['time'], '%H:%M').hour)
            time2 = str(datetime.strptime(time_e, '%H:%M').hour)
            if my_event['date']  == date_e and time_event == time2:
                return i
        return False
    
    def event_already_create(self, date_to_search, time_event):
        '''
        Determina si un evento ya fue creado en esa fecha y hora
        date_to_search: str
        time_event: str
        '''
        hour_to_search = str(datetime.strptime(time_event, '%H:%M').time().hour)
        exist_event = list(e for e in self.list_event if e['date']  == date_to_search and hour_to_search == str(datetime.strptime(e['time'], '%H:%M').time().hour))
        if exist_event != []:
            return True
        else:
            return False
        
    def get_event_index(self, i):
        '''Devuelve un evento de la lista'''
        return self.list_event[i]

#Instancia de Controller 
controller = Controller('events.json')