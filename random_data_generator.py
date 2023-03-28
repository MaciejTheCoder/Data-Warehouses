from enum import unique
import numbers
from tracemalloc import start
import pyodbc
import random
import datetime
from datetime import time
from datetime import timedelta
from calendar import monthrange

server = 'MACIEJ'
database = 'DB_source'
conn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes') 
cursor = conn.cursor()

cursor.execute("SELECT @@version as version")

while True:
    row = cursor.fetchone()
    if not row:
        break
    print(row.version)

repairdate1 = datetime.datetime.strptime('2008-01-01', '%Y-%m-%d')
repairdate2 = datetime.datetime.strptime('2020-12-30', '%Y-%m-%d')
date1 = datetime.datetime.strptime('2020-01-01', '%Y-%m-%d')
date2 = datetime.datetime.strptime('2020-12-30', '%Y-%m-%d')
num_of_stops = [9, 12, 14, 10]
num_of_courses = [40, 50, 60, 45]
model_name = ['Swing', 'Jazz', 'Twist', 'Fokstrot']
NUMBER_OF_TRAMS = 80
NUMBER_OF_LINES = 4
NUMBER_OF_DRIVERS = 150
NUMBER_OF_TEAMS = 12
NUMBER_OF_REPAIRS = 100
NUMBER_OF_MODELS = 4
TOTAL_PASSENGERS = 10000
NUM_OF_COURSES = monthrange(2021, 3)[1] * (40 + 50 + 60 + 45)

def totalStopped():
    total = 0
    for i in range(NUMBER_OF_LINES):
       total += monthrange(2021, 3)[1] * num_of_stops[i] * num_of_courses[i]
    return total

TOTAL_STOPPED = totalStopped()

def getTram(prevTram):
    tram = random.randint(0, NUMBER_OF_TRAMS - 1)
    while(tram == prevTram):
        tram = random.randint(0, NUMBER_OF_TRAMS - 1)
    return tram

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)

# DONE
def InsertModels():
    num_of_seats = [55, 49, 52, 51]
    date = ['2010-01-01', '2013-11-02', '2017-04-25', '2003-12-12']
    for i in range(NUMBER_OF_MODELS):
        cursor.execute('''INSERT INTO model(ID_model, name, producer) values (?, ?, ?)''',
                       int(i + 1), model_name[i], 'PESA')
        cursor.commit()

# DONE
def InsertTram():
    ID = 0
    for i in range(NUMBER_OF_TRAMS):
        number_of_repairs = random.randint(0,5)
        year = random.randint(2001, 2019)
        side_number = 'T' + str(i + 1)
        cursor.execute('''INSERT INTO tram (ID, number_of_repairs, year_of_production, model, side_number) values (?, ?, ?, ?, ?)''',
              int(ID + 1), number_of_repairs, year, random.randint(1, NUMBER_OF_MODELS), side_number)
        cursor.commit()
        ID += 1

# DONE
def InsertLine():
    for i in range(NUMBER_OF_LINES):
        line_name = 'LINE' + str(i + 1)
        cursor.execute('''INSERT INTO line(line_id, line_name) values (?, ?)''',
                       int(i + 1), line_name)
        cursor.commit()

# DONE
# DONE
def InsertCourse():
    courseID = 0
    stoppedID = 0
    for i in range(NUMBER_OF_LINES):
        day = 1
        courseID_buf = courseID
        for j in range(monthrange(2021, 3)[1]):
            start_hour = datetime.datetime.strptime('07:00:00', "%H:%M:%S")
            for k in range(num_of_courses[i]):
                start_date = '2021-03-' + str(day)
                end_date = '2021-03-' + str(day)
                end_hour = start_hour + timedelta(minutes=(num_of_stops[i] - 1) * 2)
                full = start_date + ' ' + str(start_hour.strftime('%H:%M:%S'))
                full_end = end_date + ' ' + str(end_hour.strftime('%H:%M:%S'))
                start_date = random_date(date1, date2)
                start_hour_buf = start_hour
                start_hour = end_hour - timedelta(minutes=num_of_stops[i])
                cursor.execute('''INSERT INTO course (course_ID, start_date, start_time, end_time, tram, line, driver, course_total_time) values (?, ?, ?, ?, ?, ?, ?, ?)''',
                               courseID_buf, start_date, full, full_end, getTram(0), i + 1, random.randint(1, NUMBER_OF_DRIVERS), random.randint(15, 69))
                cursor.commit()
                stop_time = start_hour_buf
                for l in range(num_of_stops[i]):
                    # stopped_full = start_date + ' ' +  str(stop_time.strftime('%H:%M:%S'))
                    cursor.execute('''INSERT INTO stopped_at (ID, stop_date, stop_time, course, stop, num_of_passengers_entering, num_of_passengers_leaving, number_of_free_seats) values (?, ?, ?, ?, ?, ?, ?, ?)''',
                                stoppedID, start_date, stop_time, courseID_buf, 101 + i * 100 + l, random.randint(1, 10), random.randint(1, 10), random.randint(1, 220))
                    cursor.commit()
                    stop_time = stop_time + timedelta(minutes=2)
                    stoppedID += 1
                courseID_buf += NUMBER_OF_LINES
            day += 1
        courseID += 1

# DONE
def InsertStop():
    tramStopID = 101
    cities = ['Gdansk', 'Sopot', 'Gdynia']
    district = ['Wrzeszcz', 'Glowny', 'WielkiKack', 'Zabianka', 'Zaspa', 'Wyscigi', 'Orunia', 'Karczemki']
    residential = ['Lawendowe', 'Garnizon', 'Nowiec', 'Sokolka', 'WiszaceOgrody']
    stop_type = ['Single', 'Cross']
    for i in range(NUMBER_OF_LINES):
        for j in range(num_of_stops[i]):
            uniqueTramStopID = tramStopID + j
            print(type(uniqueTramStopID))
            print(type(random.choice(cities)))
            print(type('STOP' + str(uniqueTramStopID)))
            print(type(random.randint(1, TOTAL_PASSENGERS)))
            cursor.execute('''INSERT INTO tram_stop (ID, city, district, residential, single_stop, name, passenger) values (?, ?, ?, ?, ?, ?, ?)''',
                           int(uniqueTramStopID), random.choice(cities), random.choice(district), random.choice(residential), random.choice(stop_type), 'STOP' + str(uniqueTramStopID), random.randint(1, TOTAL_PASSENGERS))
            cursor.commit()
        tramStopID += 100

# DONE
def InsertPassenger():
    ticket_type = ['normal', 'reduced']
    name = ['Jan', 'Adam', 'Pawel', 'Antoni', 'Jozef', 'Maciej', 'Jakub',
            'Michal', 'Grzegorz', 'Wieslaw', 'Tomasz', 'Martyna', 'Zofia', 'Katarzyna',
            'Barbara', 'Malgorzata', 'Aleksandra', 'Karol']
    surname = ['Kowalski', 'Majewski', 'Szczygiel', 'Szemela', 'Amelesz', 'Ziemann', 'Maksymczuk',
               'Blawat', 'Brzeczyszczykiewicz', 'Nowak', 'Lewandowski', 'Pudzianowski', 'Malysz',
               'Wojtyla', 'Duda']
    ticket_number = 0
    for i in range(TOTAL_PASSENGERS):
        ticket = random.choice(ticket_type)
        course_num = random.randint(0, 4750)
        line = course_num % 4
        pesel = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, 11)])
        full = random.choice(name) + ' ' + random.choice(surname)
        start_stop = random.randint(line * 100 + 101, line * 100 + 101 +  num_of_stops[line] - 2)
        leave_stop = random.randint(start_stop + 1, line * 100 + 101 + num_of_stops[line] - 1)
        cursor.execute('''INSERT INTO passenger (person_id, pesel, name_surname) values (?, ?, ?)''',
                       i + 1, pesel, full)
        cursor.commit()
        ticket_number += 1

# DONE
def InsertDriver():
    driverID = 0
    name = ['Jan', 'Adam', 'Pawel', 'Antoni', 'Jozef', 'Maciej', 'Jakub',
            'Michal', 'Grzegorz', 'Wieslaw', 'Tomasz', 'Martyna', 'Zofia', 'Katarzyna',
            'Barbara', 'Malgorzata', 'Aleksandra', 'Karol']
    surname = ['Kowalski', 'Majewski', 'Szczygiel', 'Szemela', 'Amelesz', 'Ziemann', 'Maksymczuk',
               'Blawat', 'Brzeczyszczykiewicz', 'Nowak', 'Lewandowski', 'Pudzianowski', 'Malysz',
               'Wojtyla', 'Duda']

    for i in range(NUMBER_OF_DRIVERS):
        driver_name = random.choice(name)
        driver_surname = random.choice(surname)
        full = driver_name + ' ' + driver_surname
        type = ['Day', 'Night']
        tram = random.randint(1, NUMBER_OF_TRAMS - 1)
        cursor.execute('''INSERT INTO driver (ID, name_surname, type_of_driver) values (?, ?, ?)''',
                           int(i + 1), full, random.choice(type))
        cursor.commit()

# DONE
def InsertHangar():
    for i in range(5):
        num_of_total_plots = [2, 4, 2, 4, 3]
        cursor.execute('''INSERT INTO hangar (ID_hang, name, num_of_total_plots) values (?, ?, ?)''',
                        i + 1, 'HANG' + str(i + 1), num_of_total_plots[i])
        cursor.commit()

# DONE
def InsertService():
    index = random.randint(3, 7)
    being_serviced = []
    repairing = random.randint(1, NUMBER_OF_TRAMS - 1)
    hangar = 1
    for i in range(index):
        while(repairing in being_serviced):
            repairing = random.randint(1, NUMBER_OF_TRAMS - 1)
        being_serviced.append(repairing)
        cursor.execute('''INSERT INTO service_in (ID_service_in, tram, hangar) values (?, ?, ?)''',
              int(i + 1), being_serviced[i], hangar)
        cursor.commit()
        hangar += 1
        if hangar >= 6:
            hangar = 1

# DONE
def InsertWorkers():
    teamID = 0
    name = ['Jan', 'Adam', 'Pawel', 'Antoni', 'Jozef', 'Maciej', 'Jakub',
            'Michal', 'Grzegorz', 'Wieslaw', 'Tomasz', 'Martyna', 'Zofia', 'Katarzyna',
            'Barbara', 'Malgorzata', 'Aleksandra', 'Karol']
    surname = ['Kowalski', 'Majewski', 'Szczygiel', 'Szemela', 'Amelesz', 'Ziemann', 'Maksymczuk',
               'Blawat', 'Brzeczyszczykiewicz', 'Nowak', 'Lewandowski', 'Pudzianowski', 'Malysz',
               'Wojtyla', 'Duda']
    for i in range(NUMBER_OF_TEAMS):
        num_of_workers = random.randint(3, 7)
        manager = random.choice(name) + '_' + random.choice(surname)
        manager = str(manager)
        hangar = random.randint(1,5)
        cursor.execute('''INSERT INTO workers_team (team_ID, num_of_workers, manager, hangar) values (?, ?, ?, ?)''',
              i + 1, num_of_workers, manager, hangar)
        cursor.commit()

# DONE
def InsertRepair():
    repairID = 0
    for i in range(NUMBER_OF_REPAIRS):
        start_date = random_date(repairdate1, repairdate2)
        end_date = start_date + datetime.timedelta(days=random.randint(3, 30))
        complexity = random.randint(1, 10)
        tram = random.randint(1, NUMBER_OF_TRAMS - 1)
        team = random.randint(1, NUMBER_OF_TEAMS - 1)
        cursor.execute('''INSERT INTO repair (repair_ID, start_date, end_date, complexity, tram, team) values (?, ?, ?, ?, ?, ?)''',
              repairID, str(start_date.date()), str(end_date.date()), complexity, tram, team)
        cursor.commit()
        repairID += 1

InsertModels()
InsertTram()
InsertLine()
InsertPassenger()
InsertStop()
InsertDriver()
InsertCourse()
InsertHangar()
InsertService()
InsertWorkers()
InsertRepair()