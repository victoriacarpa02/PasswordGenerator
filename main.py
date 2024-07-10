import telebot
import random
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


bot = telebot.TeleBot('token')

# set global variables
all_symbols = ascii_lowercase + ascii_uppercase + digits + punctuation
length = 4
parameters = {ascii_lowercase: True, ascii_uppercase: True, digits: True, punctuation: True}


# create two buttons that will be appearing nonestop
def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Generate random password')
    button2 = telebot.types.KeyboardButton('Generate password with parameters')
    keyboard.add(button1, button2)
    return keyboard


@bot.message_handler(commands=['start'])
def main(message):
    keyboard = create_keyboard()
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!\n\nWelcome to the <b>password '
                                      f'generator</b>.\n\nChoose an action: ', parse_mode='html', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def main(message):
    keyboard = create_keyboard()
    bot.send_message(message.chat.id, f'<u>Information about this bot: </u>\n\n\n<b>Generate random password</b> --> '
                                      f'generates a 15-character password using numbers, symbols, lowercase and capital '
                                      f'letters.\n\n\n<b>Generate password with parameters</b> --> generates password '
                                      f'according to your parameters;\n\n<i>P.S.(You need to enter the length of the '
                                      f'password and select what characters will be used in the password)</i>',
                        parse_mode='html', reply_markup=keyboard)


# what happens if user clicks any button below
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Generate random password':
        random_pass(message)
    elif message.text == 'Generate password with parameters':
        bot.send_message(message.chat.id, 'Enter the password length (min 4, max 64): ')
        bot.register_next_step_handler(message, pass_len)
    else:
        bot.send_message(message.chat.id, "Choose one of the buttons")


# function that adds data into the dictionary pasrameters? depending on whether the password needs to use such
# character type; after that, this function calls another function, that can generate password with user`s data
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global parameters
    if 'lwcase' in callback.data:
        parameters[ascii_lowercase] = True if callback.data == 'agree_lwcase' else False

        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton('Yes', callback_data='agree_upcase')
        btn2 = telebot.types.InlineKeyboardButton('No', callback_data='disagree_upcase')
        markup.row(btn1, btn2)
        bot.send_message(callback.message.chat.id, 'Should the password has uppercase letters?', reply_markup=markup)
    elif 'upcase' in callback.data:
        parameters[ascii_uppercase] = True if callback.data == 'agree_upcase' else False

        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton('Yes', callback_data='agree_nums')
        btn2 = telebot.types.InlineKeyboardButton('No', callback_data='disagree_nums')
        markup.row(btn1, btn2)
        bot.send_message(callback.message.chat.id, 'Should the password has digits?', reply_markup=markup)
    elif 'nums' in callback.data:
        parameters[digits] = True if callback.data == 'agree_nums' else False

        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton('Yes', callback_data='agree_symb')
        btn2 = telebot.types.InlineKeyboardButton('No', callback_data='disagree_symb')
        markup.row(btn1, btn2)
        bot.send_message(callback.message.chat.id, 'Should the password has symbols?', reply_markup=markup)
    elif 'symb' in callback.data:
        parameters[punctuation] = True if callback.data == 'agree_symb' else False
        bot.send_message(callback.message.chat.id, param_pass())


# function to handle with user input (length)
def pass_len(message):
    global length
    try:
        length = int(message.text.strip())
        if length < 4 or length > 64:
            raise ValueError
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton('Yes', callback_data='agree_lwcase')
        btn2 = telebot.types.InlineKeyboardButton('No', callback_data='disagree_lwcase')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Should the password have lowercase letters?', reply_markup=markup)
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid number for the length.")
        bot.register_next_step_handler(message, pass_len)


# function to generate random password with system settings
def random_pass(message):
    result = []
    i = 0

    for param in parameters:
        for j in range(random.randint(1, 4)):
            result.append(random.choice(param))
        i += 1

    while len(result) != 15:
        result.append(random.choice(all_symbols))

    random.shuffle(result)

    bot.send_message(message.chat.id, ''.join(result))


# function to generate random password with user settings
def param_pass():
    list_of_symbols = [ascii_lowercase, ascii_uppercase, digits, punctuation]

    result = []
    i = 0

    for s in parameters.values():
        if s is True:
            amount = random.randint(1, length//4)
            for j in range(amount):
                result.append(random.choice(list_of_symbols[i]))
        i += 1

    alowed_symbols = ''.join([x for x in parameters if parameters[x] is True])

    while len(result) < length:
        result.append(random.choice(alowed_symbols))

    random.shuffle(result)
    return ''.join(result)


bot.polling(none_stop=True)
