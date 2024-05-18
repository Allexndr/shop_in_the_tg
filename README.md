# README.md

## English

### Project Overview

This project is a Telegram bot for an online store called "Odnorazzzka". The bot allows users to browse and order disposable vape products, with features like cart management and order processing. The bot is built using the `telebot` library and provides a user-friendly interface for shopping.

### Features

- Welcome message and age verification
- Product selection and cart management
- Viewing and clearing the cart
- Order placement with address input
- Payment instructions and screenshot submission

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/odnorazzzka-bot.git
    ```

2. Navigate to the project directory:

    ```sh
    cd odnorazzzka-bot
    ```

3. Install the required dependencies:

    ```sh
    pip install pyTelegramBotAPI
    ```

4. Set up your Telegram bot token in the code:

    ```python
    bot = telebot.TeleBot("YOUR_BOT_TOKEN_HERE")
    ```

5. Run the bot:

    ```sh
    python bot.py
    ```

### Usage

1. Start the bot in your Telegram app by sending the `/start` command.
2. Follow the prompts to verify your age and browse products.
3. Add products to your cart by selecting the desired items.
4. View your cart with the provided option and manage its contents.
5. Proceed to checkout by entering your address and following payment instructions.
6. Submit a screenshot of your payment to complete the order.

### Bot Commands

- `/start` - Start the bot and clear the cart.
- `/pay` - Proceed to checkout by entering your address and receiving payment instructions.

### Callback Data

- `choose_yes`, `choose_no` - Age verification responses.
- `cart` - View the cart.
- `clear` - Clear the cart.
- `delete` - Delete an item from the cart.
- Product-specific data like `WAKA`, `PUFFMI`, `CHILLAX`, etc. - Select specific products and flavors.


---

## Русский

### Обзор проекта

Этот проект представляет собой Telegram-бот для онлайн-магазина "Odnorazzzka". Бот позволяет пользователям просматривать и заказывать одноразовые электронные сигареты, с функциями управления корзиной и обработки заказов. Бот построен с использованием библиотеки `telebot` и предоставляет удобный интерфейс для покупок.

### Функции

- Приветственное сообщение и проверка возраста
- Выбор товаров и управление корзиной
- Просмотр и очистка корзины
- Оформление заказа с вводом адреса
- Инструкции по оплате и отправка скриншотов

### Установка

1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/yourusername/odnorazzzka-bot.git
    ```

2. Перейдите в каталог проекта:

    ```sh
    cd odnorazzzka-bot
    ```

3. Установите необходимые зависимости:

    ```sh
    pip install pyTelegramBotAPI
    ```

4. Настройте токен вашего Telegram-бота в коде:

    ```python
    bot = telebot.TeleBot("YOUR_BOT_TOKEN_HERE")
    ```

5. Запустите бота:

    ```sh
    python bot.py
    ```

### Использование

1. Запустите бота в своем приложении Telegram, отправив команду `/start`.
2. Следуйте инструкциям для подтверждения возраста и просмотра товаров.
3. Добавляйте товары в корзину, выбирая нужные позиции.
4. Просмотрите корзину и управляйте её содержимым.
5. Перейдите к оформлению заказа, введя ваш адрес и следуя инструкциям по оплате.
6. Отправьте скриншот оплаты для завершения заказа.

### Команды бота

- `/start` - Запустить бота и очистить корзину.
- `/pay` - Перейти к оформлению заказа, введя адрес и получив инструкции по оплате.

### Callback Data

- `choose_yes`, `choose_no` - Ответы на проверку возраста.
- `cart` - Просмотр корзины.
- `clear` - Очистить корзину.
- `delete` - Удалить товар из корзины.
- Данные, относящиеся к продуктам, такие как `WAKA`, `PUFFMI`, `CHILLAX` и др. - Выбор конкретных продуктов и вкусов.



