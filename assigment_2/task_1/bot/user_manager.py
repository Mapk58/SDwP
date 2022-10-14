import json

class User:
    def __init__(self, state='very_beginning', input=''):
        self.state = state
        self.input = input

class Users:
    def __init__(self):
        with open('data/users.json') as json_file:
            _users = json.load(json_file)
        self._users = {i:User(_users[i]['state'], _users[i]['input']) for i in _users.keys()}
        # self._users = {}

    def save_to_file(f):
        def wrapper(self, *args, **kwargs):
            f(self, *args, **kwargs)
            with open('data/users.json', "w") as outfile:
                json.dump({i:self._users[i].__dict__ for i in self._users.keys()}, outfile)
        
        return wrapper


    def get_state(self, id):
        return self._users[str(id)].state

    @save_to_file
    def set_state(self, id, state):
        self._users[str(id)].state = state
    
    @save_to_file
    def add_user(self, id):
        self._users[str(id)] = User()

    def get_input(self, id):
        return self._users[str(id)].input

    @save_to_file
    def add_input(self, id, to_add):
        self._users[str(id)].input += (str(to_add) + ' ')

    @save_to_file
    def clear_input(self, id):
        self._users[str(id)].input = ''

users = Users()

if __name__=='__main__':
    a = Users()
    a.add_user(3)
    a.add_input(3, 12)
    a.add_input(3, '14.10')
    print(a.get_input(3))
    
    
