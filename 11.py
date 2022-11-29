import telebot
from telebot import types
import requests
import time
from random import randint
import math

number = None
count = 1
is_started_game = False
is_started_calc = False
result = None

bot = telebot.TeleBot("token")

markup = types.ReplyKeyboardMarkup()
itembth1 = types.KeyboardButton('привет')
itembth2 = types.KeyboardButton('погода')
itembth3 = types.KeyboardButton('котик')
itembth4 = types.KeyboardButton('играть')
itembth5 = types.KeyboardButton('вычислить')
markup.add(itembth1, itembth2, itembth3, itembth4, itembth5)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет, " + message.from_user.first_name, reply_markup=markup)
 

@bot.message_handler(content_types=["text"])
def hello_user(message):
    data = open('user_message.txt','a+', encoding='utf-8')
    data.writelines(f"{str(message.from_user.id)} {message.from_user.first_name}: {message.text} \n")
    data.close()
    global is_started_game
    global number
    global count
    global is_started_calc
    global result
    if is_started_game:       
        if message.text.isdigit():
            input_number = int(message.text)            
            if input_number > number:
                bot.send_message(message.from_user.id, 'Меньше!')                
            elif input_number < number:
                bot.send_message(message.from_user.id, 'Больше!')
            else:                
                is_started_game = False
                bot.send_message(message.from_user.id, f'Ты выиграл! Загаднное число {number}')
                bot.send_message(message.from_user.id, f'Количество попыток: {count}')
            count = count + 1
        elif message.text == 'стоп':
            is_started_game = False
            bot.send_message(message.from_user.id, 'Игра закончена')
        else:
            bot.send_message(message.from_user.id, 'Введи простое число')
    elif is_started_calc:                
        exp = str(message.text)
        if not '/' and not '*' and '-' in exp:
            exp = exp.replace('-', '+-')        
        if '+' in exp:
            exp = exp.split('+')            
            for number in exp:
                if number.isdigit():                       
                    result = int(exp[0]) + int(exp[1])
                else:
                    bot.send_message(message.from_user.id, 'Вы ввели некорректное выражение, введите выражение вида a+b')
                    bot.send_message(message.from_user.id, 'Для выхода введите "стоп"')
            bot.send_message(message.from_user.id, f'{message.text} = {result}')
            result = None
        elif '/' in exp:
            exp = exp.split('/')
            for number in exp:
                if number.isdigit():
                    result = int(exp[0]) / int(exp[1])                    
                else:
                    bot.send_message(message.from_user.id, 'Вы ввели некорректное выражение, введите выражение вида a+b')
                    bot.send_message(message.from_user.id, 'Для выхода введите "стоп"')
            bot.send_message(message.from_user.id, f'{message.text} = {result}')
            result = None
        elif '*' in exp:
            exp = exp.split('*')
            for number in exp:
                if number.isdigit():
                    result = int(exp[0]) * int(exp[1])                    
                else:
                    bot.send_message(message.from_user.id, 'Вы ввели некорректное выражение, введите выражение вида a+b')
                    bot.send_message(message.from_user.id, 'Для выхода введите "стоп"')
            bot.send_message(message.from_user.id, f'{message.text} = {result}')
            result = None
        elif message.text == 'стоп':
            is_started_calc = False
            bot.send_message(message.from_user.id, 'Вы вышли из режима вычисление')
        else:
            bot.send_message(message.from_user.id, 'Введите выражиажение вида a+b, используя знаки +, -, *, /')
            bot.send_message(message.from_user.id, 'Для выхода введите "стоп"')       

    else:        
        if 'привет' in message.text:
            bot.reply_to(message, 'Привет, ' + message.from_user.first_name)
        elif message.text == 'играть':
                number = randint(1, 1001)
                count = 1
                is_started_game = True
                bot.reply_to(message, f'Я загадал число от 1 до 1000. Попробуй отгадай!')
                bot.reply_to(message, 'Если захочешь закончить игру, просто введи слово "стоп". Введи первое число')
        elif message.text == 'погода':
            r = requests.get('https://wttr.in/?0T')
            bot.reply_to(message, r.text)
        elif message.text == 'котик':
            r = f'https://cataas.com/cat?t=${time.time()}'
            bot.send_photo(message.chat.id, r)
        elif message.text == 'файл':
            data = open('user_message.txt', encoding='utf-8')
            bot.send_document(message.chat.id, data)
            data.close()
        elif message.text == 'вычислить':
                is_started_calc = True
                result = None
                bot.reply_to(message, 'Введи выражение вида a+b, используя знаки +, -, *, /')
                bot.send_message(message.from_user.id, 'Для выхода введите "стоп"') 
        else: bot.reply_to(message, message.text)
    

bot.infinity_polling()