from telebot import types


def create_markup(status):
    if status in ['confirmation', 'asked4name']: # list of states which don't have menu keys
        return types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if status == 'very_beginning':
        return _create_markup_by_list(["Let's start!"])
    elif status == 'choose_university':
        return _create_markup_by_list(['u1', 'u2'] + ["Create new university"])

    return markup

def _create_markup_by_list(buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in buttons:
        markup.add(types.KeyboardButton(i))
    return markup