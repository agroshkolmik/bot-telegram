from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import StateFilter
from UserStates import UserStates
from aiogram import F
from keyboard_helper import keyboards
import pari_service as ps
from config import TOKEN

storage=MemoryStorage()
bot=Bot(token=TOKEN)
dp=Dispatcher(storage=storage)

@dp.message(Command("start"))
async def start(message: types.Message, state:FSMContext):
    kb=keyboards[UserStates.BASE]
    await message.answer("ku trup", reply_markup=kb)
    await state.set_state(UserStates.BASE)

@dp.message(F.text=="My paris", StateFilter(UserStates.BASE))
async def My_paris(message: types.Message):
    text="your paris"
    paris=ps.get_paris(message.from_user.id)
    for pari in paris:
        text+="\n"+pari
    await message.answer(text)
@dp.message(F.text=="Create pari", StateFilter(UserStates.BASE))
async def create_pari(message: types.Message):
    text=ps.add_pari(message.from_user.id,message.text)
    await message.answer(text)
async def main():
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())
