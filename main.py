import telebot
import random
import sqlite3
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем соединение с базой данных
conn = sqlite3.connect('questions_actions.db')

# Создаем курсор
cursor = conn.cursor()

# Создаем таблицу, если ее не
cursor.execute("""CREATE TABLE IF NOT EXISTS questions_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    type TEXT NOT NULL
                )""")

# Добавляем вопросы и действия в таблицу
cursor.execute("INSERT INTO questions_actions (text, type) VALUES (?, ?)", ("Какое ваше любимое блюдо?", "truth"))
cursor.execute("INSERT INTO questions_actions (text, type) VALUES (?, ?)", ("Опишите свой худший опыт в ресторане.", "truth"))
cursor.execute("INSERT INTO questions_actions (text, type) VALUES (?, ?)", ("Какая ваша любимая книга?", "truth"))
cursor.execute("INSERT INTO questions_actions (text, type) VALUES (?, ?)", ("Опишите свой худший опыт на работе.", "truth"))
cursor.execute("INSERT INTO questions_actions (text, type) VALUES (?, ?)", ("Попросите у прохожего 10 рублей.", "action"))
cursor.execute("INSERT INTO questions_actions (text, type) VALUES (?, ?)", ("Съешьте половину лимона.", "action"))
cursor.execute("INSERT INTO questions_actions (text, type) VALUES (?, ?)", ("Поцелуйте в щеку случайного человека на улице.", "action"))
cursor.execute("INSERT INTO questions_actions (text, type) VALUES (?, ?)", ("Сходите в магазин и купите конфеты за свой счет.", "action"))
cursor.execute("INSERT INTO questions_actions (text, type) VALUES (?, ?)", ("Забегите на месте 1 минуту.", "action"))

# Сохраняем изменения в базе данных
conn.commit()

# Закрываем соединение
conn.close()


bot = telebot.TeleBot('5770545685:AAHCbhMgND_CIPy2Ru0rfFrevYWXmIFOFDU')


def get_random_question():
    cursor.execute('SELECT truth FROM questions_actions ORDER BY RANDOM() LIMIT 1')
    question = cursor.fetchone()
    return question[0]

def get_random_action():
    cursor.execute('SELECT action FROM questions_actions ORDER BY RANDOM() LIMIT 1')
    action = cursor.fetchone()
    return action[0]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для игры в \"Правда или Действие\". Напиши /game, чтобы начать игру.")

@bot.message_handler(commands=['game'])
def game(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    truth_button = KeyboardButton('Правда')
    action_button = KeyboardButton('Действие')
    markup.add(truth_button, action_button)
    bot.send_message(message.chat.id, "Выбери категорию:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def process_game(message):
    if message.text == 'Правда':
        question = get_random_question()
        bot.send_message(message.chat.id, "Вопрос: " + question)
    elif message.text == 'Действие':
        action = get_random_action()
        bot.send_message(message.chat.id, "Действие: " + action)

bot.polling()
