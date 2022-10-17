import json
from datetime import datetime


class EdInstitution:
    def __init__(self, name, classrooms=None, lecture_auditoriums=None):
        """
        Task 1 function:
        Get name of institution, set of classrooms and set of lecture auditoriums. Assign all params to Class
        :param name: name of institution we will work with
        :param classrooms: set of rooms that institution have as default
        :param lecture_auditoriums: set of rooms that institution have as default
        """
        self.name = name
        if classrooms is None:
            self.classrooms = set()
        else:
            self.classrooms = classrooms

        if lecture_auditoriums is None:
            self.lecture_auditoriums = set()
        else:
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

    def __dict__(self):
        """
        Function to return institution attributes: name, classrooms and lecture auditoriums
        used for json
        """
        return {'name': self.name, 'classrooms': [i.__dict__ for i in self.classrooms],
                'lecture_auditoriums': [i.__dict__ for i in self.lecture_auditoriums]}

    def restore_from_dict(institution):
        """
        Function for creating institution instance based on institution dictionary
        :return: all necessary attributes
        """
        return EdInstitution(institution['name'],
                             set([Classroom(i['capacity'], i['number'], i['conditioner'], i['activities']) for i in
                                  institution['classrooms']]),
                             set([LectureAuditorium(i['capacity'], i['number'], i['conditioner'], i['activities']) for i
                                  in institution['lecture_auditoriums']]))

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
        """
        :return: list of all classrooms assigned to institution
        """
        return '\n'.join([str(i) for i in self.classrooms])

    def all_auditoriums(self):
        """
        :return: list of all lecture auditoriums assigned to institution
        """
        return '\n'.join([str(i) for i in self.lecture_auditoriums])

    def all_rooms(self):
        """
        :return: list of all classrooms and lecture auditoriums assigned to institution
        """
        return self.all_classrooms() + '\n' + self.all_auditoriums()

    def assign_activity_to_room(self, number, t_from, t_to, amount_of_people, type_of_room):
        """
        Append room activity list if all criterias satisfied:
        Time has no intersection with room activity list
        Amount of people is lower than room capacity
        Room number is present in list of classrooms and lecture auditoriums
        :param number: number of room
        :param t_from: starting time of activity assignment
        :param t_to: final time of activity assignment
        :param amount_of_people: amount of people assigning to room
        :param type_of_room: classroom or lecture auditorium
        """
        rooms = set()
        if type_of_room == 'Classroom':
            rooms = self.classrooms
        elif type_of_room == 'Auditorium':
            rooms = self.lecture_auditoriums

        for i in rooms:
            if i.number == number:
                return i.assign_activity(t_from, t_to, amount_of_people)
        return 'Please insert valid number of the room!'

    def assign_activity_to_classroom(self, number, t_from, t_to, amount_of_people):
        """
        Append room activity list if all criterias satisfied:
        Time has no intersection with room activity list
        Amount of people is lower than room capacity
        Room number is present in list of classrooms
        :param number: number of room
        :param t_from: starting time of activity assignment
        :param t_to: final time of activity assignment
        :param amount_of_people: amount of people assigning to room
        """
        return self.assign_activity_to_room(number, t_from, t_to, amount_of_people, 'Classroom')

    def assign_activity_to_auditorium(self, number, t_from, t_to, amount_of_people):
        """
        Append room activity list if all criterias satisfied:
        Time has no intersection with room activity list
        Amount of people is lower than room capacity
        Room number is present in list of lecture auditoriums
        :param number: number of room
        :param t_from: starting time of activity assignment
        :param t_to: final time of activity assignment
        :param amount_of_people: amount of people assigning to room
        """
        return self.assign_activity_to_room(number, t_from, t_to, amount_of_people, 'Auditorium')


class Room:
    def __init__(self, capacity, number, conditioner, activities=None):
        """
        Assigning parameters to class instance
        :param capacity: amount of people that is possible to place in room
        :param number: Number of room in university
        :param conditioner: Is there conditioner or not
        :param activities: list of activities already assigned to room
        """
        self.capacity = capacity
        self.number = number
        self.conditioner = conditioner
        if activities is None:
            self.activities = []
        else:
            self.activities = activities

    def __str__(self):
        """
        __str__ print operator overloading
        :return:
        """
        return f'''{type(self).__name__}
        Number: {self.number}
        Capacity: {self.capacity}
        Conditioner: {'Yes' if self.conditioner else 'No'}
        '''.replace('    ', '')

    def is_free_today(self):
        """
        Search of assigned activities today
        :return: True if there is no assigned activities
        """
        today = datetime.timestamp(datetime.now()) - datetime.timestamp(datetime.now()) % (60 * 60 * 24) -60*60*3
        t_from = today + 8 * 60 * 60
        t_to = today + 21 * 60 * 60
        print(t_from, t_to)
        return self.is_free(t_from, t_to)

    def is_free(self, t_from, t_to):
        """
        Search of intersection with already assigned activities
        :param t_from: activity assigning starting time
        :param t_to: activity assigning final time
        :return True if there is no intersection
        """
        not_intersected = 0
        for interval in self.activities:
            if interval[1] <= t_from or interval[0] >= t_to:
                not_intersected += 1
        if len(self.activities) == not_intersected:
            return True
        return False

    def assign_activity(self, t_from, t_to, amount_of_people):
        """
        Append room activity list if all criterias satisfied:
        Time has no intersection with room activity list
        Amount of people is lower than room capacity
        :param t_from: activity assigning starting time
        :param t_to: activity assigning final time
        :param amount_of_people:
        """
        print(f'Adding activity to room {self.number}')
        if not self.is_free(t_from, t_to):
            return "This time is occupied."

        if self.capacity < amount_of_people:
            return "Choose less number of people."

        self.activities.append([t_from, t_to])
        return "Activity successfully added!"


class Classroom(Room):
    pass


class LectureAuditorium(Room):
    pass


class InstituteManager:
    flag = False

    def __new__(cls):
        """
        Manager to work with university instances
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        """
        Extract institution data from json
        """
        if not self.flag:
            with open('data/data.json') as json_file:
                institutions = json.load(json_file)
            self.institutions = [EdInstitution.restore_from_dict(i) for i in institutions]
            self.flag = True

    def add(self, institute):
        """
        Creates instance of institute and append it to existing array of institutes
        """
        self.institutions.append(EdInstitution(institute))

    def save_to_file(self, filename='data/data.json'):
        """
        Saves all institutions to json file
        """
        with open(filename, "w") as outfile:
            json.dump([i.__dict__() for i in self.institutions], outfile)

    def __str__(self):
        """
        Makes institute instance string value
        """
        return '\n'.join([str(i) for i in self.institutions])

    def get_institute_names(self):
        """
        Gets name of institute instance
        """
        return [i.name for i in self.institutions]

    def institute(self, name):
        """
        :return institute by name
        """
        return [i for i in self.institutions if i.name == name][0]


manager = InstituteManager()


if __name__ == '__main__':
    # Innopolis = EdInstitution("Innopolis")
    # Innopolis.add(LectureAuditorium(10, 108, True))
    # Innopolis.add(LectureAuditorium(20, 304, True))
    #
    # print(Innopolis.assign_activity_to_auditorium(108, 10, 20, 1))

    # print(i.is_free_today() for i in manager[1].classrooms)
    print([i.is_free_today() for i in manager.institutions[1].classrooms])

    # B = EdInstitution("B")
    # B.add(qwe2)
    #
    # a = InstituteManager()
    # a.add(Innopolis)
    # a.add(B)
    #
    # a.save_to_file()
    # k = InstituteManager.restore_from_file()
    # print(k)

    # qwe.assign_activity(datetime.timestamp(datetime.now()), datetime.timestamp(datetime.now()) + 1000, 1)
    # print('----')
    # print(qwe.is_free_today())
