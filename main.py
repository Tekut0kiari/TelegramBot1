import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import db_utils

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the states of the conversation
SELECT = range(1)

# Define the buttons for the main menu
menu_buttons = [
    [InlineKeyboardButton("Правда", callback_data='truth')],
    [InlineKeyboardButton("Действие", callback_data='action')],
]

# Define the buttons for the truth and action menus
truth_buttons = [
    [InlineKeyboardButton("Так", callback_data='true')],
    [InlineKeyboardButton("Нет", callback_data='false')],
    [InlineKeyboardButton("Не знаю", callback_data='unknown')],
]

action_buttons = [
    [InlineKeyboardButton("Сделано", callback_data='done')],
    [InlineKeyboardButton("Не сделано", callback_data='not_done')],
    [InlineKeyboardButton("Не понятно", callback_data='not_understand')],
]

# Define the callback functions for the buttons
def menu_callback(update, context):
    query = update.callback_query
    query.answer()
    context.bot.send_message(chat_id=query.message.chat_id, text='Выберите категорию:', reply_markup=InlineKeyboardMarkup(menu_buttons))
    return SELECT

def truth_callback(update, context):
    query = update.callback_query
    query.answer()
    context.user_data['category'] = 'truth'
    data = db_utils.get_random_data('questions')
    if data:
        context.user_data['question_id'] = data[0]
        context.bot.send_message(chat_id=query.message.chat_id, text=data[1], reply_markup=InlineKeyboardMarkup(truth_buttons))
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text='Извините, в настоящее время в базе данных нет вопросов в этой категории')

def action_callback(update, context):
    query = update.callback_query
    query.answer()
    context.user_data['category'] = 'action'
    data = db_utils.get_random_data('actions')
    if data:
        context.user_data['question_id'] = data[0]
        context.bot.send_message(chat_id=query.message.chat_id, text=data[1], reply_markup=InlineKeyboardMarkup(action_buttons))
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text='Извините, в
