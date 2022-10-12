# TODO:
# think about possibility of file uploading-downloading in bot

# Oleg:
# Task 2: we should be able to swap between institutions. Class Room should have instance to EdInstitution to
# get self.name
# Task 5: from my point of view function assign_activity should take string as parameter
# Task 6: function get_available_* need rework based possibility to assign multiple activities in a day


# ChangeLog:
# Oleg - Add docstrings and to do tasks

import json
from datetime import datetime

class EdInstitution:
    def __init__(self, name, classrooms=set(), lecture_auditoriums=set()):
        """
        Task 1 function:
        Get name of institution, set of classrooms and set of lecture auditoriums. Assign all params to Class
        :param name: name of institution we will work with
        :param classrooms: set of rooms that institution have as default
        :param lecture_auditoriums: -||-
        """
        self.name = name
        self.classrooms = classrooms
        self.lecture_auditoriums = lecture_auditoriums

    def __str__(self):
        """
        Task 4 function:
        Print operator overloading
        :return: Print all
        """
        return f'''{self.name}
        Classroom(s) : {len(self.classrooms)}
        Auditorium(s) : {len(self.lecture_auditoriums)}
        Status for today (now) : {len(self.get_available_classrooms())} available classroom(s) and {len(self.get_available_auditoriums())} available lecture auditorium(s)
        '''

    def get_available_classrooms(self):
        """
        Function for __str__ print operator overloading
        :return: List of rooms that aren't fully booked
        """
        return set([room.number for room in self.classrooms if room.is_free_today()])

    def get_available_auditoriums(self):
        """
        Function for __str__ print operator overloading
        :return: List of rooms that aren't fully booked
        """
        return set([room.number for room in self.lecture_auditoriums if room.is_free_today()])

    def saveToFile(self, filename='data.json'):
        """
        Task 7 and 8 function:
        Save class attributes to json file
        """
        with open(filename, "w") as outfile:
            json.dump({'name':self.name, 'classrooms':[i.__dict__ for i in self.classrooms], 'lecture_auditoriums':[i.__dict__ for i in self.lecture_auditoriums]}, outfile)
    
    def restoreFromFile(filename='data.json'):
        """
        Task 7 and 8 function:
        Load class attributes from json file
        """
        with open(filename) as json_file:
            institution = json.load(json_file)
        return EdInstitution(institution['name'], 
                             set([Classroom(i['capacity'], i['number'], i['conditioner'], i['activities']) for i in institution['classrooms']]), 
                             set([LectureAuditorium(i['capacity'], i['number'], i['conditioner'], i['activities']) for i in institution['lecture_auditoriums']]))
    
    def add(self, room):
        """
        Task 7 function:
        Add room to set in EdInstitution class attributes according to name of called class
        :param room: Class of room with params(capacity, number, conditioner, activities=[])
        """
        if type(room).__name__ == 'Classroom':
            self.classrooms.add(room)
            return 'Classroom successfully added!'
        else:
            self.lecture_auditoriums.add(room)
            return 'Lecture auditorium successfully added!'
    
    def remove(self, room):
        """
        Task 7 function:
        Remove room from set in EdInstitution class attributes according to name of called class
        :param room: Class of room with params(capacity, number, conditioner, activities=[])
        """
        if type(room).__name__ == 'Classroom':
            if room in self.classrooms:
                self.classrooms.remove(room)
                return 'Classroom successfully removed!'
            else:
                return 'There is no such classroom!'
        else:
            if room in self.lecture_auditoriums:
                self.lecture_auditoriums.remove(room)
                return 'Lecture auditorium successfully removed!'
            else:
                return 'There is no such auditorium!'

    def all_classrooms(self):
        return '\n'.join([str(i) for i in self.classrooms])
    
    def all_auditoriums(self):
        return '\n'.join([str(i) for i in self.lecture_auditoriums])

    def all_rooms(self):
        return self.all_classrooms() + '\n' + self.all_auditoriums()
    

class Room:
    def __init__(self, capacity, number, conditioner, activities=[]):
        """
        Task 3 function:
        Get params and assign them to Class attributes
        """
        self.capacity = capacity
        self.number = number
        self.conditioner = conditioner
        self.activities = activities
    
    def __str__(self):
        """
        Task 4 function:
        Print operator overloading. "All classes implemented should have a constructor"
        :return: Print all
        """
        return f'''{type(self).__name__}
        Number: {self.number}
        Capacity: {self.capacity}
        Conditioner: {'Yes' if self.conditioner else 'No'}
        '''.replace('    ', '')

    def is_free_today(self):
        today = datetime.timestamp(datetime.now()) - datetime.timestamp(datetime.now())%(60*60*24)#-60*60*3
        t_from = today + 8*60*60
        t_to = today + 21*60*60
        # print(datetime.fromtimestamp(t_from))
        # print(datetime.fromtimestamp(t_to))
        return self.is_free(t_from, t_to)

    def is_free(self, t_from, t_to):
        print(self.activities)
        print(t_from)
        print(t_to)
        not_intersected = 0
        for interval in self.activities:
            if (interval[1] <= t_from or interval[0] >= t_to):
                not_intersected += 1
        if (len(self.activities) == not_intersected):
            return True
        return False

    def assign_activity(self, t_from, t_to, amount_of_people):
        if self.is_free(t_from, t_to) and self.capacity >= amount_of_people:
            self.activities.append([t_from, t_to])
            return True
        else:
            return False

    

class Classroom(Room):
    pass

class LectureAuditorium(Room):
    pass


if __name__ == '__main__':
    qwe = LectureAuditorium(1, 1, True)
    qwe.assign_activity(datetime.timestamp(datetime.now()),datetime.timestamp(datetime.now())+1000,1)
    print('----')
    print(qwe.is_free_today())