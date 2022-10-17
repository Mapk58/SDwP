import json

class User:
    def __init__(self, state='very_beginning', input='', uni=''):
        """
        :param state: particular state in bot
        :param input: input, entered by user
        :param uni: name of the university
        """
        self.state = state
        self.input = input
        self.uni = uni

class Users:
    def __init__(self):
        """
        Reading information about user from json
        """
        with open('data/users.json') as json_file:
            _users = json.load(json_file)
        self._users = {i:User(_users[i]['state'], _users[i]['input']) for i in _users.keys()}
        # self._users = {}

    def save_to_file(f):
        """
        Decorator for functions for saving all alterations to file
        :return: wrapper
        """
        def wrapper(self, *args, **kwargs):
            f(self, *args, **kwargs)
            with open('data/users.json', "w") as outfile:
                json.dump({i:self._users[i].__dict__ for i in self._users.keys()}, outfile)
        
        return wrapper

    def get_state(self, id):
        """
        Function for getting the state of user in the beginning of the session with bot
        :param id: user's id
        :return: user's state
        """
        return self._users[str(id)].state

    @save_to_file
    def set_state(self, id, state):
        """
        Function for setting the state to user.
        :param id: user's id
        :param state: new user's state
        """
        self._users[str(id)].state = state
    
    @save_to_file
    def add_user(self, id):
        """
        Adding new user to the user's dict by id.
        :param id: user's id
        """
        self._users[str(id)] = User()

    def get_input(self, id):
        """
        Getting the user's input.
        :param id: user's id
        :return: user's input
        """
        return self._users[str(id)].input

    @save_to_file
    def add_input(self, id, to_add):
        """
        Adding the user's input.
        :param id: user's id
        :param to_add: input from user
        """
        self._users[str(id)].input += (str(to_add) + ' ')

    @save_to_file
    def clear_input(self, id):
        """
        Clearing the user's input.
        :param id: user's id
        """
        self._users[str(id)].input = ''

    def get_uni(self, id):
        """
        Getting the user's university.
        :param id: user's id
        :return: user's university
        """
        return self._users[str(id)].uni
    
    @save_to_file
    def set_uni(self, id, uni):
        """
        Setting the university to user.
        :param id: user's id
        """
        self._users[str(id)].uni = uni

users = Users()

if __name__=='__main__':
    a = Users()
    a.add_user(3)
    a.add_input(3, 12)
    a.add_input(3, '14.10')
    print(a.get_input(3))
    
    
