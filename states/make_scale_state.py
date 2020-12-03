from aiogram.dispatcher.filters.state import StatesGroup, State


class MakeScale(StatesGroup):
    PRESSURE_IN_FRONT_AXIS_TRUCK = State()
    PRESSURE_IN_BACK_AXIS_TRUCK = State()
    PRESSURE_IN_FRONT_AXIS_TRAILER = State()
    PRESSURE_IN_BACK_AXIS_TRAILER = State()
