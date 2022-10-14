from telebot import types
from task1 import manager

def create_markup(status):
    if status in ['confirmation', 'creating_university']: # list of states which don't have menu keys
        return types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if status == 'very_beginning':
        return _create_markup_by_list(["Let's start!"])
    elif status == 'choose_university':
        return _create_markup_by_list(manager.get_institute_names() + ["Create new university"])
    elif status == 'menu':
        return _create_markup_by_list(['Add classroom or Auditorium to institution','Print institution summary','Assign activity to classroom','Assign activity to LectureAuditorium','Return to universities'])
    return markup

def _create_markup_by_list(buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in buttons:
        markup.add(types.KeyboardButton(i))
    return markup


