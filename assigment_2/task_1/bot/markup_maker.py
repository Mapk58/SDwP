from telebot import types
from task1 import manager


def create_markup(status):
    if status in ['confirmation', 'creating_university', 'create_classroom_number_of_room', 'create_auditorium_number_of_room',\
                  'enter_number_of_auditorium', 'enter_number_of_classroom']:  # list of states which don't have menu keys
        return types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if status == 'very_beginning':
        return _create_markup_by_list(["Let's start!"])

    elif status == 'choose_university':
        return _create_markup_by_list(manager.get_institute_names() + ["Create new university", "Save"])

    elif status == 'menu':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Add Classroom or Auditorium to institution'))
        markup.add(types.KeyboardButton('Print institution summary'))
        markup.row(types.KeyboardButton('Assign activity to classroom'),
                   types.KeyboardButton('Assign activity to LectureAuditorium'))
        markup.add(types.KeyboardButton('Return to universities'))

        return markup
    elif status == 'what_do_you_want_to_add':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Classroom'), types.KeyboardButton('Auditorium'))
        markup.add(types.KeyboardButton('Back to operations'))
        return markup

    elif status == 'do_you_want_air_conditioning_classroom':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Yes'), types.KeyboardButton('No'))
        return markup

    elif status == 'do_you_want_air_conditioning_auditorium':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Yes'), types.KeyboardButton('No'))
        return markup

    elif status == 'add_another_room_to_Innopolis_University':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Yes'), types.KeyboardButton('No'))
        return markup

    elif status == 'assign_acitivity_to_Classroom':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Yes'), types.KeyboardButton('No'))
        return markup

    return markup


def _create_markup_by_list(buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in buttons:
        markup.add(types.KeyboardButton(i))
    return markup


