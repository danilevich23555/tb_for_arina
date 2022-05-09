from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


from config import TOKEN
import keyboards as kb

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

drive_dict = {'1': 1.2, '2': 1.375, '3': 1.55}
dict_procent = {'1': [15, 20],'2': [20, 25] }

class Form(StatesGroup):
    weight = State()
    tall = State()
    age = State()
    drive = State()
    level = State()


class Form_water(StatesGroup):
    weight_for_water = State()

##


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(f"Привет {message['from']['first_name']} это бот марафона PRO_тело от ARISHA_VESNA!\n"
                        f"С этого дня я активно буду с тобой на связи ❤❤\n"
                        f"Здесь ты можешь увидеть и получить следующие вещи\n"
                        f"✔ Расчет ккал\n"
                        f"✔ Расчет нормы воды\n"
                        f"✔ Файлик с основными заменами продуктов\n"
                        f"✔ Мотивационные ролики\n"
                        f"✔ Трекер полезных привычек\n"
                        f"\n"
                        f"В меню ниже ты можешь выбрать, с чего начать!", reply_markup=kb.markup3)








@dp.message_handler(content_types='text')
async def process_help_command(message: types.Message):
    count =2
    if message.text == "Рассчитать калории ⚖":
        await Form.weight.set()
        await message.reply(
            f'Для расчета мне понадобятся твои показатели\n'
            f'\n'
            f'В ответ на мои следующие сообщения пиши только число'
            )
        await message.reply('Введите свой вес.')

        @dp.message_handler(state=Form.weight)
        async def process_name(message: types.Message, state: FSMContext):
            """
            Process user name
            """
            async with state.proxy() as data:
                data['weight'] = message.text

            await Form.next()
            await message.reply("Какой у тебя рост(в сантиметрах)?")

        @dp.message_handler(lambda message: message.text.isdigit(), state=Form.tall)
        async def process_age(message: types.Message, state: FSMContext):
            # Update state and data
            await Form.next()
            await state.update_data(tall=int(message.text))
            await message.reply("Сколько тебе лет?")

        @dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
        async def process_gender(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['age'] = message.text

            await Form.next()
            await message.reply("Отлично! Теперь давай определим уровень твоей активности.\n"
                                    "\n"
                                    "1. Слабая 2-3 тренировки в неделю, менее 5000 шагов в день.\n"
                                    "\n"
                                    "2. Средняя: 3-4 полноценные тренеровки (если выполняешь все тренировки в марафоне,\n"
                                    "выбирай этот критерий).\n"
                                    "\n"
                                    "3. Высокая: 5-6 активных тренеровок в неделю, более 15000 шагов в день.\n"
                                    "\n"
                                    "Напиши только цифру, которая подходит тебе (1 или 2 или 3) без лишних знаков\n"
                                    "и символов.")


        @dp.message_handler( state=Form.drive)
        async def process_drive(message: types.Message, state: FSMContext):
            # Update state and data
            async with state.proxy() as data:
                data['drive'] = message.text

            await Form.next()
            norma = (((9.99*int(data['weight']))+(6.25*int(data['tall']))-(4.92*int(data['age'])))-161)*drive_dict[f'{data["drive"]}']
            await message.reply(f"{round(norma)}Ккал - это твой калораж для поддержания текущего веса\n"
                                f"\n"
                                f"‼️НАПОМИНАЮ, марафон не предусматривает массонабор‼️\n"
                                f"\n"
                                f"Выбери свою цель на марафон:\n"
                                f"1. Похудение до 6 кг и рельеф\n"
                                f"2. Похудение более чем на 7 кг")
            await message.reply(f'❗️Напиши только цифру, которая подходит тебе (1 или 2) без\n'
                                f'лишних знаков и символов.')

        @dp.message_handler(state=Form.level)
        async def process_drive(message: types.Message, state: FSMContext):
            # Update state and data
            async with state.proxy() as data:
                data['level'] = message.text
            print(drive_dict[f'{data["drive"]}'])
            print(data["drive"])
            await Form.next()
            norma = (((9.99 * int(data['weight'])) + (6.25 * int(data['tall'])) - (4.92 * int(data['age']))) - 161)*drive_dict[f'{data["drive"]}']
            start = norma - (round(norma*dict_procent[f"{data['level']}"][0])/100)
            stop = norma - (round(norma*dict_procent[f"{data['level']}"][1])/100)
            await message.reply(f"Твой коридор калорий от {round(stop)}Ккал до {round(start)}Ккал\n"
                                f"Коридор калорий - это диапазон калорий,\n"
                                f"которых нужно придерживаться для твоего результата✨\n"
                                f"\n")
            await message.reply(f"А вот распределение белков/углеводов/жиров на день\n"
                                f"Белки: \n"
                                f"от {round(1.6*int(data['weight']))} до {round(2.1*int(data['weight']))}\n"
                                f"\n"
                                f"Углеводы:\n"
                                f"от {round(2.2*int(data['weight']))} до {round(3*int(data['weight']))}\n"
                                f"\n"
                                f"Жиры:\n"
                                f"от {round(0.8*int(data['weight']))} до {round(1.3*int(data['weight']))}\n"
                                f"\n"
                                f"Сохрани это сообщение 👌🏽(сделай скриншот или перешли его \n"
                                f"в личные сообщения)")
            await message.reply(f'🧚🏽‍♀️Мы рассчитали калории, а теперь давайте немного скорректируем КАЖДЫЙ  день из меню.\n'
                                f'Итак, если Ваш дефицит ккал вышел в рамках:\n'
                                f'👉🏻 менее 1200-1300 ккал уберите один перекус из меню\n'
                                f'______\n'
                                f'👉🏻 1300-1400 ккал кушаете СТРОГО по меню, добавлять ккал нельзя!\n'
                                f'______\n'
                                f'👉🏻 1400-1500 ккал можете кушать по меню, если чувствуете, что не наедаетесь,\n'
                                f' добавьте к меню в любой приём пищи:\n'
                                f' • крупа 30 гр в сухом виде или хлебцы 2 шт\n'
                                f'ИЛИ\n'
                                f' • куриное филе, нежирная рыба или творог 2% 50 г\n'
                                f'______\n'
                                f'👉🏻 1500 - 1600 ккал\n'
                                f'к меню в любой приём пищи добавить:\n'
                                f'• куриное филе 50 гр, в сыром виде\n'
                                f'• масло оливковое 1 ч.л. (можно приправить салат)\n'
                                f'• 20 гр крупы в сухом виде, в любой приём пищи.\n'
                                f'______\n'
                                f'👉🏻 1600-1700 ккал к меню в любой приём пищи добавляем:\n'
                                f'• куриное филе 60 гр, в сыром виде\n'
                                f'• масло оливковое 1 ч.л. (можно приправить салат)\n'
                                f'• крупа 40 гр, в сухом виде или хлебцы 40 гр.\n' 
                                f'______\n'
                                f'👉🏻 1700-1800 ккал к меню в любой приём пищи добавляем:\n'
                                f'• куриное филе 80 г (в сыром виде)\n' 
                                f'• масло оливковое 1 ч.л.\n' 
                                f'• крупа 60 гр, в сухом виде.')



            await state.finish()

    elif message.text == "Рассчитать воду 💦":
        await Form_water.weight_for_water.set()
        await message.reply(
            f'Для расчета мне понадобятся твои показатели\n'
            f'\n'
            f'В ответ на мои следующие сообщения пиши только число'
            )
        await message.reply('Введите свой вес.')

        @dp.message_handler(state=Form_water.weight_for_water)
        async def process_name(message: types.Message, state: FSMContext):
            """
            Process user name
            """
            async with state.proxy() as data:
                data['weight_for_water'] = message.text
            await message.reply(f"Твоя суточная норма воды {int(data['weight_for_water'])*0.04} в литрах")
            await state.finish()
    elif message.text == "Техническая помощь 🔧":
        await message.reply(f'Если ты нажал эту кнопку, то у тебя возникли вопросы,\n'
                            f'напиши мне в теллеграмм @arishavesna, я отвечу, как только смогу❤.')


if __name__ == '__main__':
    executor.start_polling(dp)
