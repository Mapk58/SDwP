import json
from datetime import datetime


class EdInstitution:
    def __init__(self, name, classrooms=None, lecture_auditoriums=None):
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
        return f'''{self.name}
        Classroom(s) : {len(self.classrooms)}
        Auditorium(s) : {len(self.lecture_auditoriums)}
        Status for today (now) : {len(self.get_available_classrooms())} available classroom(s) and {len(self.get_available_auditoriums())} available lecture auditorium(s)
        '''

    def get_available_classrooms(self):
        return set([room.number for room in self.classrooms if room.is_free_today()])

    def get_available_auditoriums(self):
        return set([room.number for room in self.lecture_auditoriums if room.is_free_today()])

    def __dict__(self):
        return {'name': self.name, 'classrooms': [i.__dict__ for i in self.classrooms],
                'lecture_auditoriums': [i.__dict__ for i in self.lecture_auditoriums]}

    def restore_from_dict(institution):
        return EdInstitution(institution['name'],
                             set([Classroom(i['capacity'], i['number'], i['conditioner'], i['activities']) for i in
                                  institution['classrooms']]),
                             set([LectureAuditorium(i['capacity'], i['number'], i['conditioner'], i['activities']) for i
                                  in institution['lecture_auditoriums']]))

    def add(self, room):
        if type(room).__name__ == 'Classroom':
            self.classrooms.add(room)
            return 'Classroom successfully added!'
        else:
            self.lecture_auditoriums.add(room)
            return 'Lecture auditorium successfully added!'

    def remove(self, room):
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

    def assign_activity_to_room(self, number, t_from, t_to, amount_of_people, type_of_room):
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
        return self.assign_activity_to_room(number, t_from, t_to, amount_of_people, 'Classroom')

    def assign_activity_to_auditorium(self, number, t_from, t_to, amount_of_people):
        return self.assign_activity_to_room(number, t_from, t_to, amount_of_people, 'Auditorium')


class Room:
    def __init__(self, capacity, number, conditioner, activities=None):
        self.capacity = capacity
        self.number = number
        self.conditioner = conditioner
        if activities is None:
            self.activities = []
        else:
            self.activities = activities

    def __str__(self):
        return f'''{type(self).__name__}
        Number: {self.number}
        Capacity: {self.capacity}
        Conditioner: {'Yes' if self.conditioner else 'No'}
        '''.replace('    ', '')

    def is_free_today(self):
        today = datetime.timestamp(datetime.now()) - datetime.timestamp(datetime.now()) % (60 * 60 * 24) -60*60*3
        t_from = today + 8 * 60 * 60
        t_to = today + 21 * 60 * 60
        print(t_from, t_to)
        return self.is_free(t_from, t_to)

    def is_free(self, t_from, t_to):
        not_intersected = 0
        for interval in self.activities:
            if interval[1] <= t_from or interval[0] >= t_to:
                not_intersected += 1
        if len(self.activities) == not_intersected:
            return True
        return False

    def assign_activity(self, t_from, t_to, amount_of_people):
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
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if not self.flag:
            with open('data/data.json') as json_file:
                institutions = json.load(json_file)
            self.institutions = [EdInstitution.restore_from_dict(i) for i in institutions]
            self.flag = True

    def add(self, institute):
        self.institutions.append(EdInstitution(institute))

    def save_to_file(self, filename='data/data.json'):
        with open(filename, "w") as outfile:
            json.dump([i.__dict__() for i in self.institutions], outfile)

    def __str__(self):
        return '\n'.join([str(i) for i in self.institutions])

    def get_institute_names(self):
        return [i.name for i in self.institutions]

    def institute(self, name):
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
