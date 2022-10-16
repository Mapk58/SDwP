import markup_maker as mm
import user_manager as um
from task1 import manager

def handle_message(id, m):
    text = m.text
    markup = None
    status = um.users.get_state(id)
    new_status = 'choose_university'
    reply = 'Wrong command, try again!'

    if status == 'very_beginning' and text == "Let's start!":
        reply = 'Choose one university from below or create a new one: \n' + ('\n'.join(manager.get_institute_names()))
        new_status = 'choose_university'
    elif status == 'choose_university':
        if text=='Create new university':
            reply = 'Enter the name of the university:'
            new_status = 'creating_university'
        elif text=='Save':
            reply = 'Successfully saved!'
            new_status = 'choose_university'
            manager.save_to_file()
        else:
            reply = 'Choose one operation from below:' # add existance check 
            um.users.set_uni(id, text)
            new_status = 'menu'
    elif status == 'creating_university':
        reply = 'University successfully created!' # add existance check
        new_status = 'choose_university'
        manager.add(text)
    elif status == 'menu':
        if text=='Return to universities':
            reply = 'Choose one university from below or create a new one: \n' + ('\n'.join(manager.get_institute_names()))
            new_status = 'choose_university'
        elif text=='Print institution summary':
            reply = str(manager.institute(um.users.get_uni(id)))
            new_status = 'menu'
        else:
            reply = 'Still under construction :('
            new_status = 'menu'
    

    markup = mm.create_markup(new_status)
    um.users.set_state(id, new_status)
    return reply, markup