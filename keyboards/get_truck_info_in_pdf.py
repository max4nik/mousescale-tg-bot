from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

truck_info_in_pdf_inline_button = InlineKeyboardButton('Отримати інформацію файлом', callback_data='truck_info_to_pdf')

truck_info_in_pdf_inline = InlineKeyboardMarkup().add(truck_info_in_pdf_inline_button)
