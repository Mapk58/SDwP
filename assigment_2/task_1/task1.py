import json
from datetime import datetime


class EdInstitution:
    def __init__(self, name, classrooms=set(), lecture_auditoriums=set()):
        self.name = name
        self.classrooms = classrooms
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


class Room:
    def __init__(self, capacity, number, conditioner, activities=[]):
        self.capacity = capacity
        self.number = number
        self.conditioner = conditioner
        self.activities = activities

    def __str__(self):
        return f'''{type(self).__name__}
        Number: {self.number}
        Capacity: {self.capacity}
        Conditioner: {'Yes' if self.conditioner else 'No'}
        '''.replace('    ', '')

    def is_free_today(self):
        today = datetime.timestamp(datetime.now()) - datetime.timestamp(datetime.now()) % (60 * 60 * 24)  # -60*60*3
        t_from = today + 8 * 60 * 60
        t_to = today + 21 * 60 * 60
        return self.is_free(t_from, t_to)

    def is_free(self, t_from, t_to):
        print(self.activities)
        print(t_from)
        print(t_to)
        not_intersected = 0
        for interval in self.activities:
            if interval[1] <= t_from or interval[0] >= t_to:
                not_intersected += 1
        if len(self.activities) == not_intersected:
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


class InstituteManager:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, institutions=[]):
        self.institutions = institutions

    def add(self, institute):
        self.institutions.append(institute)

    def save_to_file(self, filename='data.json'):
        with open(filename, "w") as outfile:
            json.dump([i.__dict__ for i in self.institutions], outfile)

    def restore_from_file(filename='data.json'):
        with open(filename) as json_file:
            institutions = json.load(json_file)
        return InstituteManager([EdInstitution.restoreFromDict(i) for i in institutions])

    def __str__(self):
        return [str(i) for i in self.institutions]


if __name__ == '__main__':
    Innopolis = EdInstitution("Innopolis")
    qwe = LectureAuditorium(1, 1, True)
    Innopolis.add(qwe)
    qwe2 = LectureAuditorium(20, 1, True)
    Innopolis.add(qwe2)


    # qwe.assign_activity(datetime.timestamp(datetime.now()), datetime.timestamp(datetime.now()) + 1000, 1)
    # print('----')
    # print(qwe.is_free_today())
