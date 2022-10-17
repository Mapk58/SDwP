import markup_maker as mm
import user_manager as um
import time
import re
from datetime import datetime
from task1 import manager, Classroom, LectureAuditorium


def check_time(text):
    """
    Function for checking time on validity.
    :param text: contains string of time range
    :return: results of conditions.
    """

    text = text.replace(' ', '')
    result0 = bool(re.search(
        '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', text))
    result1 = False
    result2 = False
    if result0:
        t_from, t_to = text.split("-")
        t_from_hour, t_from_minute = t_from.split(":")
        t_to_hour, t_to_minute = t_to.split(":")
        result1 = int(t_from_hour) == int(t_to_hour) and int(t_from_minute) < int(t_to_minute) \
            or int(t_from_hour) < int(t_to_hour)
        result2 = 8 <= int(t_from_hour) < 21 and 8 <= int(t_to_hour) < 21 or \
            8 <= int(t_from_hour) < 21 and int(
                t_to_hour) == 21 and int(t_to_minute) == 0
    return result0, result1, result2


def parameters_room(user_input):
    """
    Function for getting the parameters for creating Classroom/LectureAuditorium.
    :param user_input: contains params, which will be parsed to particular variables
    :return: parameters
    """

    user_input = user_input.split(' ')
    capacity = int(user_input[1])
    number = int(user_input[0])
    conditioner = user_input[2]

    return capacity, number, conditioner


def parameters_activity(user_input):
    """
    Function for getting the parameters of assign_activity_to... method.
    :param user_input: contains params, which will be parsed to particular variables
    :return: parameters
    """

    user_input = user_input.split(' ')
    number = int(user_input[0])
    day, month, year = user_input[1].split("/")
    t_from_hour, t_from_minute = user_input[2].split(":")
    t_to_hour, t_to_minute = user_input[3].split(":")
    t_from = datetime(int(year), int(month), int(
        day), int(t_from_hour), int(t_from_minute))
    t_to = datetime(int(year), int(month), int(
        day), int(t_to_hour), int(t_to_minute))
    t_from = time.mktime(t_from.timetuple())
    t_to = time.mktime(t_to.timetuple())
    capacity = int(user_input[4])

    return number, t_from, t_to, capacity


def handle_message(id, m):
    """
    Processing comands received from the user, based on their current status.
    :return: reply to user and markup according to his status.
    """

    text = m.text
    markup = None
    status = um.users.get_state(id)
    new_status = 'choose_university'
    reply = 'Wrong command, try again!'

    if status == 'very_beginning' and text == "Let's start!":
        reply = 'Choose one university from below or create a new one: \n' + \
            ('\n'.join(manager.get_institute_names()))
        new_status = 'choose_university'
    elif status == 'choose_university':
        if text == 'Create new university':
            reply = 'Enter the name of the university:'
            new_status = 'creating_university'
        elif text == 'Save':
            reply = 'Successfully saved!'
            new_status = 'choose_university'
            manager.save_to_file()
        else:
            reply = 'Choose one operation from below:'
            um.users.set_uni(id, text)
            new_status = 'menu'
    elif status == 'creating_university':
        if text not in manager.get_institute_names():
            reply = 'University successfully created!'
            new_status = 'choose_university'
            manager.add(text)
        else:
            reply = "University with such name already exists. Enter another name:"
            new_status = 'creating_university'
    elif status == 'menu':
        if text == "Add Classroom or Auditorium to institution":
            reply = "What do you want to add?"
            new_status = 'what_do_you_want_to_add'
        elif text == 'Print institution summary':
            reply = str(manager.institute(um.users.get_uni(id)))
            new_status = 'menu'
        elif text == 'Assign activity to classroom':
            all_classrooms = ''.join(manager.institute(
                um.users.get_uni(id)).all_classrooms())
            if all_classrooms == '':
                reply = '''There is no Classrooms yet. If you want to create it, \
                            choose the button "Add Classroom or Auditorium to institution"
                        '''
                new_status = 'menu'
            else:
                reply = all_classrooms + '\n Choose number of Classroom from the list above:'
                new_status = 'enter_number_of_classroom'
        elif text == 'Assign activity to LectureAuditorium':
            all_auditoriums = ''.join(manager.institute(
                um.users.get_uni(id)).all_auditoriums())
            if all_auditoriums == '':
                reply = '''There is no Auditoriums yet. If you want to create it, \
                            choose the button "Add Classroom or Auditorium to institution".
                        '''
                new_status = 'menu'
            else:
                reply = all_auditoriums + '\n Choose number of Auditorium from the list above:'
                new_status = 'enter_number_of_auditorium'
        elif text == 'Return to universities':
            reply = 'Choose one university from below or create a new one: \n' + (
                '\n'.join(manager.get_institute_names()))
            new_status = 'choose_university'
        elif text == 'Exit program':
            reply = (''.join(str(manager))) + \
                "Don't forget to Save information"
            new_status = 'choose_university'
        else:
            reply = 'Choose one operation from below:'
            new_status = 'menu'
    elif status == 'what_do_you_want_to_add':
        if text == 'Classroom':
            reply = 'Enter number of classroom:'
            new_status = 'create_classroom_number_of_room'
        elif text == 'Auditorium':
            reply = 'Enter number of auditorium:'
            new_status = 'create_auditorium_number_of_room'
        elif text == 'Back to operations':
            reply = 'Choose one operation from below:'
            new_status = 'menu'
        else:
            reply = 'Choose one option from below:'
            new_status = 'what_do_you_want_to_add'
    elif status == 'create_classroom_number_of_room':
        if text.isnumeric():
            um.users.add_input(id, text)
            reply = 'Enter classroom capacity:'
            new_status = 'create_classroom_capacity_of_room'
        else:
            reply = 'Please enter correct number of room:'
            new_status = 'create_classroom_number_of_room'
    elif status == 'create_classroom_capacity_of_room':
        if text.isnumeric():
            um.users.add_input(id, text)
            reply = 'Is there air conditioner?'
            new_status = 'do_you_want_air_conditioning_classroom'
        else:
            reply = 'Enter integer number'
            new_status = 'create_classroom_capacity_of_room'
    elif status == 'do_you_want_air_conditioning_classroom':
        if text == 'Yes' or text == 'No':
            um.users.add_input(id, text)
            capacity, number, conditioner = parameters_room(
                um.users.get_input(id))
            classroom = Classroom(capacity, number, conditioner)
            manager.institute(um.users.get_uni(id)).add(classroom)
            um.users.clear_input(id)

            reply = "Classroom successfully added! \n" + "Do you want to add another room?"
            new_status = 'add_another_room_to_Innopolis_University'
        else:
            reply = 'Choose one option from below:'
            new_status = 'do_you_want_air_conditioning_classroom'
    elif status == 'create_auditorium_number_of_room':
        if text.isnumeric():
            um.users.add_input(id, text)
            reply = 'Enter auditorium capacity:'
            new_status = 'create_auditorium_capacity_of_room'
        else:
            reply = 'Please enter correct number of room:'
            new_status = 'create_auditorium_number_of_room'
    elif status == 'create_auditorium_capacity_of_room':
        if text.isnumeric():
            um.users.add_input(id, text)
            reply = 'Is there air conditioner?'
            new_status = 'do_you_want_air_conditioning_auditorium'
        else:
            reply = 'Enter integer number'
            new_status = 'create_classroom_capacity_of_room'
    elif status == 'do_you_want_air_conditioning_auditorium':
        if text == 'Yes' or text == 'No':
            um.users.add_input(id, text)
            capacity, number, conditioner = parameters_room(
                um.users.get_input(id))
            auditorium = LectureAuditorium(capacity, number, conditioner)
            manager.institute(um.users.get_uni(id)).add(auditorium)
            um.users.clear_input(id)

            reply = "Auditorium successfully added! \n" + "Do you want to add another room?"
            new_status = 'add_another_room_to_Innopolis_University'
        else:
            reply = 'Choose one option from below:'
            new_status = 'do_you_want_air_conditioning_auditorium'
    elif status == 'add_another_room_to_Innopolis_University':
        if text == 'Yes':
            reply = 'Choose one option from below:'
            new_status = 'what_do_you_want_to_add'
        elif text == 'No':
            reply = 'Choose one operation from below:'
            new_status = 'menu'
        else:
            reply = 'Choose one option from below:'
            new_status = 'add_another_room_to_Innopolis_University'
    elif status == 'enter_number_of_classroom':
        if text.isnumeric():
            um.users.add_input(id, text)
            reply = 'Enter day to book (dd/mm/yyyy):'
            new_status = 'enter_date_classroom'
        else:
            reply = 'Enter integer number'
            new_status = 'enter_number_of_classroom'
    elif status == 'enter_date_classroom':
        try:
            if time.strptime(text, '%d/%m/%Y').tm_year <= 2024:
                # Checking that date for today or future
                today = datetime.today().date()
                valid_date = datetime.strptime(text, '%d/%m/%Y').date()
                if valid_date >= today:
                    um.users.add_input(id, text)
                    reply = 'Enter time interval to book (HH:MM-HH:MM). Time should be between 8:00 and 21:00 :'
                    new_status = 'enter_time_classroom'
                else:
                    reply = 'Enter today\'s date or future date:'
                    new_status = 'enter_date_classroom'
            else:
                reply = 'Year should be less than 2024. Enter valid year:'
                new_status = 'enter_date_classroom'
        except Exception as e:
            if str(e) == "day is out of range for month":
                reply = 'Enter existing date!'
            else:
                reply = 'Enter data according to format dd/mm/yyyy :'
            new_status = 'enter_date_classroom'
    elif status == 'enter_time_classroom':
        if0, if1, if2 = check_time(text)
        if if0:
            t_from, t_to = text.replace(' ', '').split("-")
            if if1:
                if if2:
                    um.users.add_input(id, t_from)
                    um.users.add_input(id, t_to)
                    reply = "How many people will participate?"
                    new_status = 'enter_capacity_classroom'
                else:
                    reply = "Enter time between 8:00 and 21:00 :"
                    new_status = 'enter_time_classroom'
            else:
                reply = "The start time should be less than the end time:"
                new_status = 'enter_time_classroom'
        else:
            reply = "Enter valid time according to format HH:MM :"
            new_status = 'enter_time_classroom'

    elif status == 'enter_capacity_classroom':
        if text.isnumeric():
            um.users.add_input(id, text)
            number, t_from, t_to, capacity = parameters_activity(
                um.users.get_input(id))

            result = manager.institute(um.users.get_uni(id)).assign_activity_to_classroom(number, t_from, t_to,
                                                                                          capacity)
            um.users.clear_input(id)
            if result == "Activity successfully added!":
                reply = result + '\nChoose one operation from below:'
                new_status = 'menu'
            else:
                reply = result + "\nTry from the beginning.\nEnter the number of classroom:"
                new_status = 'enter_number_of_classroom'
        else:
            reply = 'Enter integer number'
            new_status = 'enter_capacity_classroom'
    elif status == 'enter_number_of_auditorium':
        if text.isnumeric():
            um.users.add_input(id, text)
            reply = 'Enter day to book (dd/mm/yyyy):'
            new_status = 'enter_date_auditorium'
        else:
            reply = 'Enter integer number'
            new_status = 'enter_number_of_auditorium'
    elif status == 'enter_date_auditorium':
        try:
            if time.strptime(text, '%d/%m/%Y').tm_year <= 2024:
                # Checking that date for today or future
                today = datetime.today().date()
                valid_date = datetime.strptime(text, '%d/%m/%Y').date()
                if valid_date >= today:
                    um.users.add_input(id, text)
                    reply = 'Enter time interval to book (HH:MM-HH:MM). Time should be between 8:00 and 21:00 :'
                    new_status = 'enter_time_auditorium'
                else:
                    reply = 'Enter today\'s date or future date:'
                    new_status = 'enter_date_auditorium'
            else:
                reply = 'Year should be less than 2024. Enter valid year:'
                new_status = 'enter_date_classroom'

        except Exception as e:
            if str(e) == "day is out of range for month":
                reply = 'Enter existing date!'
            else:
                reply = 'Enter data according to format dd/mm/yyyy :'
            new_status = 'enter_date_auditorium'
    elif status == 'enter_time_auditorium':
        if0, if1, if2 = check_time(text)
        if if0:
            t_from, t_to = text.replace(' ', '').split("-")
            if if1:
                if if2:
                    um.users.add_input(id, t_from)
                    um.users.add_input(id, t_to)
                    reply = "How many people will participate?"
                    new_status = 'enter_capacity_auditorium'
                else:
                    reply = "Enter time between 8:00 and 21:00 :"
                    new_status = 'enter_time_auditorium'
            else:
                reply = "The start time should be less than the end time:"
                new_status = 'enter_time_auditorium'
        else:
            reply = "Enter valid time according to format HH:MM :"
            new_status = 'enter_time_auditorium'
    elif status == 'enter_capacity_auditorium':
        if text.isnumeric():
            um.users.add_input(id, text)
            number, t_from, t_to, capacity = parameters_activity(
                um.users.get_input(id))

            result = manager.institute(um.users.get_uni(id)).assign_activity_to_auditorium(number, t_from, t_to,
                                                                                           capacity)
            um.users.clear_input(id)
            if result == "Activity successfully added!":
                reply = result + '\nChoose one operation from below:'
                new_status = 'menu'
            else:
                reply = result + "\nTry from the beginning.\nEnter the number of auditorium:"
                new_status = 'enter_number_of_auditorium'
        else:
            reply = 'Enter integer number'
            new_status = 'enter_capacity_auditorium'

    markup = mm.create_markup(new_status)
    um.users.set_state(id, new_status)
    return reply, markup
