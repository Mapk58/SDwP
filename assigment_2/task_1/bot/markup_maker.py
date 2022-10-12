from telebot import types

def create_markup(status):
    if status in ['confirmation', 'asked4name']: # list of statuses which don't have menu keys
        return types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if status == 'very_beginning':
        return _create_markup_by_list(["Let's start!"])
    elif status == 'message2student':
        item1 = types.KeyboardButton("Вернуться в меню")
        markup.add(item1)
    elif status == 'message2group':
        item1 = types.KeyboardButton("Вернуться в меню")
        markup.add(item1)
    elif status == 'message2all':
        item1 = types.KeyboardButton("Вернуться в меню")
        markup.add(item1)

    return markup

def _create_markup_by_list(buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in buttons:
        markup.add(types.KeyboardButton(i))
    return markup