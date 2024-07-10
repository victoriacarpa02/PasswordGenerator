# Password Generator Bot
This project is a Telegram bot that generates random passwords. Users can choose to generate a password with default settings or specify custom parameters such as length and character types.

## Features
- _Generate Random Password:_ Generates a 15-character password using numbers, symbols, lowercase, and uppercase letters.
- _Generate Password with Parameters:_ Allows users to specify the length (4-64 characters) and select character types 
  to include (lowercase, uppercase, digits, symbols).

## Setup and Installation
1. Clone the Repository:
```
git clone https://github.com/yourusername/password-generator-bot.git
cd password-generator-bot
```
2. Install Dependencies:
Ensure you have Python 3.x installed. Then, install the required packages:
```
pip install pyTelegramBotAPI
```

## Usage
1. Start the Bot:
   - Send /start to the bot to initialize it.
   - You will receive a welcome message with two buttons: "Generate random password" and "Generate password with 
     parameters".

2. Generate Random Password:
   - Click "Generate random password" to receive a 15-character password.

3. Generate Password with Parameters:
   - Click "Generate password with parameters".
   - Enter the desired password length (between 4 and 64 characters).
   - Select the character types (lowercase, uppercase, digits, symbols) by responding to the bot's prompts.

## Code Overview
__Global Variables__
- all_symbols: String containing all possible characters (lowercase, uppercase, digits, punctuation).
- length: Default password length (4).
- parameters: Dictionary to hold character type inclusion settings.

__Functions__
- create_keyboard(): Creates the initial keyboard with two buttons.
- main(message): Handles the /start and /help commands.
- handle_message(message): Processes button clicks.
- callback_message(callback): Manages user input for custom password parameters.
- pass_len(message): Handles password length input.
- random_pass(message): Generates a random password with default settings.
- param_pass(): Generates a password based on user-defined parameters.

__Bot Polling__
- bot.polling(none_stop=True): Starts the bot and keeps it running.

## Acknowledgements
[pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/) for the Telegram bot framework.