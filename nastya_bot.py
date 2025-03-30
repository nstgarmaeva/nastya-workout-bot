import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

# Вставь сюда свой токен от BotFather
TOKEN = '8030992917:AAHeU2bMv823Z7FNUJQvY5aZB5ApFW3gjUg'
bot = telebot.TeleBot(TOKEN)

scheduler = BackgroundScheduler()

# Твой ID в Telegram
MY_TELEGRAM_ID = 962622524

user_data = {}

# Программа тренировок с ссылками
WORKOUTS = {
    "Вторник": [
        ("Приседания — 3х15", "https://youtu.be/aclHkVaku9U"),
        ("Выпады назад — 3х12", "https://youtu.be/QOVaHwm-Q6U"),
        ("Махи ногой назад — 3х20", "https://youtu.be/VM-hJCpZWWU"),
        ("Планка — 3 подхода по 1 мин.", "https://youtu.be/pvIjsG5Svck")
    ],
    "Четверг": [
        ("Отжимания — 3х10", "https://youtu.be/IODxDxX7oi4"),
        ("Упражнения с резинкой для рук — 3х15", "https://youtu.be/F1ybEwEHplc"),
        ("Подъём гантелей на плечи — 3х12", "https://youtu.be/6z8Rl5CqZRk"),
        ("Планка боковая — 3х30 сек.", "https://youtu.be/9Q0D6xAyrOI")
    ],
    "Суббота": [
        ("Ягодичный мостик — 3х20", "https://youtu.be/U-tb4_lAhnM"),
        ("Махи ногами в стороны — 3х15", "https://youtu.be/oBpqYHzT7PY"),
        ("Упражнения для шеи — 3х20", "https://youtu.be/ZcsGbo8ppFc"),
        ("Велосипед на пресс — 3х30", "https://youtu.be/Iwyvozckjak")
    ]
}

# Функция отправки тренировки с чек-листом и ссылками
def send_workout(day):
    if MY_TELEGRAM_ID:
        exercises = WORKOUTS[day]
        checklist = "\n\n".join([f"☐ {ex}\n📹 {url}" for ex, url in exercises])
        msg = f"💪 Тренировка на сегодня ({day}):\n\n{checklist}\n\nОтметь выполненные упражнения!"
        bot.send_message(MY_TELEGRAM_ID, msg)

# Настройка расписания
scheduler.add_job(lambda: send_workout("Вторник"), 'cron', day_of_week='tue', hour=16, minute=0)
scheduler.add_job(lambda: send_workout("Четверг"), 'cron', day_of_week='thu', hour=16, minute=0)
scheduler.add_job(lambda: send_workout("Суббота"), 'cron', day_of_week='sat', hour=16, minute=0)

scheduler.start()

@bot.message_handler(commands=['start'])
def start_command(message):
    user_data[MY_TELEGRAM_ID] = {}
    bot.send_message(message.chat.id, "👋 Привет, Настя! Теперь ты будешь получать персональные напоминания о тренировках с видео-примерами.\n\nОтправляй мне свой вес и параметры командой /data (например: /data вес 60 талия 70 бедра 90).")

@bot.message_handler(commands=['data'])
def save_data(message):
    global user_data
    data_parts = message.text.split()[1:]
    user_data[message.chat.id] = {}
    for i in range(0, len(data_parts), 2):
        user_data[message.chat.id][data_parts[i]] = data_parts[i+1]
    bot.send_message(message.chat.id, f"✅ Твои параметры сохранены: {user_data[message.chat.id]}")

bot.infinity_polling()
