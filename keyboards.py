from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


button_hi = KeyboardButton('Привет! 👋')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)

greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)

greet_kb2 = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_hi)

button1 = KeyboardButton('Рассчитать калории ⚖')
button2 = KeyboardButton('Рассчитать воду 💦')
button3 = KeyboardButton('Техническая помощь 🔧')

markup3 = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button1).add(button2).add(button3)


