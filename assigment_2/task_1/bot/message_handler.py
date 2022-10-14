import markup_maker as mm
import user_manager as um

def handle_message(id, m):
    text = m.text
    markup = None
    status = um.users.get_state(id)
    new_status = 'choose_university'
    reply = 'Wrong command, try again!'

    if status == 'very_beginning' and text == "Let's start!":
        reply = 'okeeey lesgooo'
        new_status = 'choose_university'
    elif status == 'choose_university':
        reply = 'Sorry, menu is still under construction! :c'

    markup = mm.create_markup(new_status)
    um.users.set_state(id, new_status)
    return reply, markup