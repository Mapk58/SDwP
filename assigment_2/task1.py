# TODO:
# wait for answers from Gcinizwe
# do all things connected with Activity assignment
# check if time intervals works with saving/loading
# think about possibility of file uploading-downloading in bot
# start making a bot


import json

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
        return set([room.number for room in self.classrooms if room.is_free()])

    def get_available_auditoriums(self):
        return set([room.number for room in self.lecture_auditoriums if room.is_free()])

    def saveToFile(self, filename='data.json'):
        with open(filename, "w") as outfile:
            json.dump({'name':self.name, 'classrooms':[i.__dict__ for i in self.classrooms], 'lecture_auditoriums':[i.__dict__ for i in self.lecture_auditoriums]}, outfile)
    
    def restoreFromFile(filename='data.json'):
        with open(filename) as json_file:
            institution = json.load(json_file)
        return EdInstitution(institution['name'], 
                             set([Classroom(i['capacity'], i['number'], i['conditioner'], i['activities']) for i in institution['classrooms']]), 
                             set([LectureAuditorium(i['capacity'], i['number'], i['conditioner'], i['activities']) for i in institution['lecture_auditoriums']]))
    
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

    def is_free(self):
        # TODO:
        # should we have real-time update?
        # make decision
        # realize it here
        return True

class Classroom(Room):
    pass

class LectureAuditorium(Room):
    pass


if __name__ == '__main__':
    innop = EdInstitution('Innopolis University', set([Classroom(100, 108, True), Classroom(20, 304, False)]))
    print(innop)
    innop.saveToFile('data.json')
    innop = EdInstitution.restoreFromFile('data.json')
    print(innop)

    qwe = LectureAuditorium(1, 1, True)
    print(innop.add(qwe))
    print(innop)
    # print(innop.remove(qwe))
    # print(innop)
    # print(innop.remove(qwe))
    # print(innop)

    print(innop.all_rooms())