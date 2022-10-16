from telebot import types
from task1 import manager

def create_markup(status):
    if status in ['confirmation', 'creating_university']: # list of states which don't have menu keys
        return types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if status == 'very_beginning':
        return _create_markup_by_list(["Let's start!"])
    elif status == 'choose_university':
        return _create_markup_by_list(manager.get_institute_names() + ["Create new university", "Save"])
    elif status == 'menu':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Add classroom or Auditorium to institution'))
        markup.add(types.KeyboardButton('Print institution summary'))
        markup.row(types.KeyboardButton('Assign activity to classroom'), types.KeyboardButton('Assign activity to LectureAuditorium'))
        markup.add(types.KeyboardButton('Return to universities'))
        
        return markup
    return markup

def _create_markup_by_list(buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in buttons:
        markup.add(types.KeyboardButton(i))
    return markup


