from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.get_truck_info_in_pdf import truck_info_in_pdf_inline
from keyboards.options_menu import options
from secret import token
from states.make_scale_state import MakeScale

# configuration
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
users = set()

# test truck
current_truck = {
    'id': 1,
    'model_name': 'Ringo Fruit B 2134 XT',
    'user_id': 123456789,
    'weight_in_ton': '30',
    'last_scaled': '12/04/2020',
    'last_fueled': '02/12/2020',
    'cargo': 'fruit',
    'number': '(BG) B 2134 XT'
}


# for starting
@dp.message_handler(commands=['start'])
async def greeting(message: types.message.Message):
    await message.answer('Вітаю!')
    users.add(message.from_user.__str__())
    await message.answer('Виберіть опцію в меню: ', reply_markup=options)
    print(users)


@dp.message_handler(text='Інформація про трак')
async def truck_info(message: types.message.Message):
    await message.answer('Ось інформація про ваш трак: ')
    await message.answer(
        '*Модель*: \"' + current_truck['model_name'] + '\"' + '\n' +
        '*Вага*: ' + str(current_truck['weight_in_ton']) + ' тонн' + '\n' +
        '*Дата останнього скейлингу*: ' + current_truck['last_scaled'] + '\n' +
        '*Дата останньої заправки*: ' + current_truck['last_fueled'] + '\n' +
        '*Вантаж*: ' + current_truck['cargo'] + '\n' +
        '*Номер*: ' + current_truck['number'],
        reply_markup=truck_info_in_pdf_inline,
        parse_mode='Markdown'
    )


# will send pdf file with all truck info
@dp.callback_query_handler(lambda c: c.data == 'truck_info_to_pdf')
async def truck_info_to_pdf(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'розробка...')


# function to start scaling
@dp.message_handler(text='Make scale', state=None)
async def make_scale(message: types.message.Message):
    await message.answer('Розпочнімо!', reply_markup=ReplyKeyboardRemove())
    await message.answer('Приготуйте манометр та впевніться, що трак завантажено')
    await message.answer('Крок 1️⃣\n\n' + '*Введіть тиск на передніх осях траку*', parse_mode='Markdown')
    await MakeScale.first()


# 4 functions below are for collecting scale data (implemented using states)
@dp.message_handler(state=MakeScale.PRESSURE_IN_FRONT_AXIS_TRUCK)
async def enter_pressure_in_front_axis_truck(message: types.message.Message, state: FSMContext):
    try:
        pressure_in_front_axis_truck = float(message.text)
        async with state.proxy() as data:
            data['pressure_in_front_axis_truck'] = pressure_in_front_axis_truck
        await message.answer('Крок 2️⃣\n\n' + '*Введіть тиск на задніх осях траку*', parse_mode='Markdown')
    except:
        await message.answer('Введіть число, будь ласка')
        return

    await MakeScale.next()


@dp.message_handler(state=MakeScale.PRESSURE_IN_BACK_AXIS_TRUCK)
async def enter_pressure_in_back_axis_truck(message: types.message.Message, state: FSMContext):
    try:
        pressure_in_back_axis_truck = float(message.text)
        async with state.proxy() as data:
            data['pressure_in_back_axis_truck'] = pressure_in_back_axis_truck
        await message.answer('Крок 3️⃣\n\n' + '*Введіть тиск на передніх осях причепа*', parse_mode='Markdown')
    except:
        await message.answer('Введіть число, будь ласка')
        return
    await MakeScale.next()


@dp.message_handler(state=MakeScale.PRESSURE_IN_FRONT_AXIS_TRAILER)
async def enter_pressure_in_front_axis_trailer(message: types.message.Message, state: FSMContext):
    try:
        pressure_in_front_axis_trailer = float(message.text)
        async with state.proxy() as data:
            data['pressure_in_front_axis_trailer'] = pressure_in_front_axis_trailer
        await message.answer('Крок 4️⃣\n\n' + '*Введіть тиск на задніх осях причепа*', parse_mode='Markdown')
    except:
        await message.answer('Введіть число, будь ласка')
        return

    await MakeScale.next()


# this function is last so it shows scale results
@dp.message_handler(state=MakeScale.PRESSURE_IN_BACK_AXIS_TRAILER)
async def enter_pressure_in_back_axis_trailer(message: types.message.Message, state: FSMContext):
    try:
        pressure_in_back_axis_trailer = float(message.text)
        async with state.proxy() as data:
            data['pressure_in_back_axis_trailer'] = pressure_in_back_axis_trailer
    except:
        await message.answer('Введіть число, будь ласка')
        return
    data = await state.get_data()
    print(data.__str__())
    await message.answer('Results')
    await message.answer(data.__str__(), reply_markup=options)
    await state.finish()


# diesel calculator (will be implemented)
@dp.message_handler(text='Дизель калькулятор')
async def diesel_calculator(message: types.message.Message):
    await message.answer('розробка...')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
