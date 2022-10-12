import markup_maker as mm

def handle_message(id, status, m):
    text = m.text
    markup = None
    reply = 'Wrong command, try again!'

    if status == 'very_beginning' and text == "Let's start!":
        reply = 'okeeey lesgooo'
        markup = mm.create_markup(status)
    return reply, markup