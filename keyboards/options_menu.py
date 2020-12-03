from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

truck_info_button = KeyboardButton('Інформація про трак')
scale_button = KeyboardButton('Make scale')
diesel_calculator_button = KeyboardButton('Дизель калькулятор')
options = ReplyKeyboardMarkup(resize_keyboard=True).row(truck_info_button).row(scale_button, diesel_calculator_button)
