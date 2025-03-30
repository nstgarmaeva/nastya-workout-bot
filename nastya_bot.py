import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

# Вставь сюда свой токен от BotFather
TOKEN = '8030992917:AAHeU2bMv823Z7FNUJQvY5aZB5ApFW3gjUg'
bot = telebot.TeleBot(TOKEN)

scheduler = BackgroundScheduler()

# Твой ID в Telegram (получишь, отправив боту команду /start)
MY_TELEGRAM_ID = None

# Программа тренировок
WORKOUTS = {
    "Вторник": ["Приседания — 3х15", "Выпады назад — 3х12", "Махи ногой назад — 3х20", "Планка — 3 подхода по 1 мин."],
    "Четверг": ["Отжимания — 3х10", "Упражнения с резинкой для рук — 3х15", "Подъём гантелей на плечи — 3х12", "Планка боковая — 3х30 сек."],
    "Суббота": ["Ягодичный мостик — 3х20", "Махи ногами в стороны — 3х15", "Упражнения для шеи — 3х20", "Велосипед на пресс — 3х30"]
}

# Функция отправки тренировки с чек-листом
def send_workout(day):
    if MY_TELEGRAM_ID:
        exercises = WORKOUTS[day]
        checklist = "\n".join([f"☐ {ex}" for ex in exercises])
        msg = f"💪 Тренировка на сегодня ({day}):\n\n{checklist}\n\nОтметь выполненные упражнения!"
        bot.send_message(MY_TELEGRAM_ID, msg)

# Настройка расписания
scheduler.add_job(lambda: send_workout("Вторник"), 'cron', day_of_week='tue', hour=16, minute=0)
scheduler.add_job(lambda: send_workout("Четверг"), 'cron', day_of_week='thu', hour=16, minute=0)
scheduler.add_job(lambda: send_workout("Суббота"), 'cron', day_of_week='sat', hour=16, minute=0)

scheduler.start()

@bot.message_handler(commands=['start'])
def start_command(message):
    global MY_TELEGRAM_ID
    MY_TELEGRAM_ID = message.chat.id
    bot.send_message(message.chat.id, "👋 Привет, Настя! Теперь ты будешь получать персональные напоминания о тренировках.")

bot.infinity_polling()
