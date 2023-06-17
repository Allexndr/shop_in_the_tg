import telebot
from telebot import types

bot = telebot.TeleBot("")


@bot.message_handler(commands=['start'])
def start(message):
    cart.clear()
    bot.send_message(message.chat.id,
                     "Добро пожаловать в онлайн магазин: <b><u>Odnorazzzka</u></b>. \nВыберите товар и мы доставим его "
                     "бесплатно! ",
                     parse_mode='html')
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Да', callback_data='choose_yes')
    button2 = types.InlineKeyboardButton('Нет', callback_data='choose_no')
    markup.row(button1, button2)
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, Здравствуйте, ответьте на вопрос:<b><u>\nВам "
                                      f"есть 21 год?</u></b>", reply_markup=markup, parse_mode='html')


cart = {}
total = 0



def update_total():
    global total
    total = sum(cart.values())


@bot.callback_query_handler(func=lambda call: call.data == 'cart')
def view_cart(call):
    global result
    result = ''
    update_total()
    for key, value in cart.items():
        result += f' {key}:{value}\n '
        print(result)
    choose_markup = types.InlineKeyboardMarkup()
    bot.send_message(call.message.chat.id, f"Вот ваши товары:\n{result}")
    bot.send_message(call.message.chat.id, f"Сумма товаров:{total}", reply_markup=choose_markup)

    delete_markup = types.InlineKeyboardMarkup()
    delete_markup.add(types.InlineKeyboardButton("Очистить корзину", callback_data="clear"),
                      types.InlineKeyboardButton("Удаление товара из корзины", callback_data="delete"))
    bot.send_message(chat_id=call.message.chat.id,
                     text="Если хотите очистить корзину или удалить товар,жмите на кнопку", reply_markup=delete_markup)


@bot.callback_query_handler(func=lambda call: call.data == "clear")
def clear_cart(call):
    cart.clear()
    bot.send_message(call.message.chat.id, "Корзина была очищена")


@bot.callback_query_handler(func=lambda call: call.data == "delete")
def delete_object(call):
    items = list(cart.keys())
    if len(items) == 0:
        bot.send_message(call.message.chat.id, "Корзина пуста.")
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for item in items:
            button = types.InlineKeyboardButton(f"{item}", callback_data=f"delete_{item}")
            markup.add(button)
        bot.send_message(call.message.chat.id, "Выберите предмет для удаления:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def delete_item(call):
    item = call.data.split("_")[1]
    if item in cart:
        del cart[item]
        bot.send_message(call.message.chat.id, f"{item} был удален из корзины.")
    else:
        bot.send_message(call.message.chat.id, f"{item} не найден в корзине.")

@bot.message_handler(commands=['pay'])
def ask_address(message):
    global address
    address = ''
    bot.send_message(message.chat.id, "Введите ваш полный адрес в формате:г.Алматы,улица,дом,квартира по желанию")
    bot.register_next_step_handler(message, ask_for_address)


def ask_for_address(message):
    global address
    address = message.text
    bot.send_message(message.chat.id, 'Нажмите на номер и он скопируется! \n`5356 5020 1526 4454` ',
                     parse_mode="MARKDOWN")
    bot.send_message(message.chat.id,
                     '<b><u>После оплаты отправляйте скриншот в этот чат,при заказе от 10000₸ доставка бесплатно!</u></b>',
                     parse_mode='HTML')
    cart_summary = ''
    for key, value in cart.items():
        cart_summary += f' {key}:{value}\n '
    # Pass the cart_summary variable as an argument to the ask_for_screenshot function
    bot.register_next_step_handler(message, ask_for_screenshot, cart_summary)


def ask_for_screenshot(message, cart_summary):
    if message.photo:
        bot.send_message(message.chat.id, "Если оплата прошла успешно, с вами свяжется наш оператор")
        forward_chat_id = 
        # forward_chat_id = 
        bot.send_message(forward_chat_id,
                         f"Пользователь: @{message.from_user.username}, {message.from_user.first_name} заказал(а):\n {cart_summary} на сумму: {total} \n  по адресу: {address}")
        bot.send_photo(forward_chat_id, message.photo[-1].file_id)
    else:
        # ask for a valid screenshot
        bot.send_message(message.chat.id, "Пожалуйста, отправьте скриншот оплаты")
        bot.register_next_step_handler(message, ask_for_screenshot, cart_summary)



@bot.callback_query_handler(func=lambda call: True)
def step_1(call):
    if call.data == 'choose_yes':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Жидкости💦', callback_data='liquid'),
                   types.InlineKeyboardButton('Одноразки😤', callback_data='odnorazka'))
        bot.send_message(chat_id=call.message.chat.id, text="Выберите нужный вам товар:",
                         reply_markup=markup)
        # bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "odnorazka":
        odnorazka_markup = types.InlineKeyboardMarkup(row_width=2)
        odnorazka_markup.add(
            types.InlineKeyboardButton('WAKA👽', callback_data='WAKA'),
            types.InlineKeyboardButton("PUFFMI😮‍💨", callback_data='PUFFMI'),
            types.InlineKeyboardButton("CHILLAX😎", callback_data="CHILLAX"),
            types.InlineKeyboardButton("SAB💀", callback_data="SAB"),
            types.InlineKeyboardButton("Back", callback_data="Back_to_main_choose"))

        bot.send_message(chat_id=call.message.chat.id, text="Выберите одноразку", reply_markup=odnorazka_markup)

    elif call.data == "WAKA":
        markup = types.InlineKeyboardMarkup(row_width=1)
        waka_price = types.InlineKeyboardButton('6000(Тяг)-6000₸', callback_data="WAKA_PRICES 6000")
        bot.send_photo(call.message.chat.id,
                       'https://belvaping.com/wp-content/uploads/2022/10/Odnorazki-WAKA-SMASH-6000-02.jpg',
                       reply_to_message_id=waka_price)
        markup.row(waka_price)
        bot.send_message(chat_id=call.message.chat.id, text="Выберите колво тяжек", reply_markup=markup)

    elif call.data == "WAKA_PRICES 6000":
        tastes_waka_markup = types.InlineKeyboardMarkup(row_width=2)
        tastes_waka_markup.add(
            types.InlineKeyboardButton("Cherry Bomb 🍒💣", callback_data="WAKA_TASTE WAKA: Cherry Bomb"),
            types.InlineKeyboardButton('Cherry Lime 🍒🍋', callback_data="WAKA_TASTE WAKA: Cherry Lime"),
            types.InlineKeyboardButton('Strawberry grape 🍓🍇', callback_data="WAKA_TASTE WAKA: Strawberry grape"),
            types.InlineKeyboardButton('Watermelon 🍉', callback_data="WAKA_TASTE WAKA: Watermelon"),
            types.InlineKeyboardButton('Peach kiwi melon 🍑🥝🍈', callback_data="WAKA_TASTE WAKA: Peach kiwi melon"),
            types.InlineKeyboardButton('Apple 🍎', callback_data="WAKA_TASTE WAKA: Apple"),
            types.InlineKeyboardButton('Coconut banana 🥥🍌', callback_data="WAKA_TASTE WAKA: Coconut banana"),
            types.InlineKeyboardButton('Lynche orange 🥭🍊', callback_data="WAKA_TASTE  WAKA: Lynche orange"),
            types.InlineKeyboardButton('Pomegranate 🍎🍇', callback_data="WAKA_TASTE  WAKA: Pomegranate"),
            types.InlineKeyboardButton('Aloe Grape 🍃🍇', callback_data="WAKA_TASTE  WAKA: Aloe Grape"),
            types.InlineKeyboardButton('Back', callback_data="Back_odnorazka"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"))
        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=tastes_waka_markup)
    elif call.data.startswith("WAKA_TASTE"):
        cart[call.data[11:]] = 6000
        update_total()
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[11:]}добавлен в корзину, сумма корзины:{total}, сумма корзины:{total}")
        print(cart)
    elif call.data == "PUFFMI":
        bot.send_photo(call.message.chat.id,
                       'https://sun9-29.userapi.com/impg/AG0vzXbx8v94P1xeYQJjk82oXEpWieml9ATxqg/xx-Exu9n4P0.jpg?size=1280x914&quality=96&sign=00c1803e878b1786b6b3d35613ee8a12&c_uniq_tag=1OiTVf248KaI6BkY6wnZaJWJ-V27_Ft0CGtTKO568Hw&type=album')
        markup_puffmi = types.InlineKeyboardMarkup(row_width=2)
        markup_puffmi.add(
            types.InlineKeyboardButton('DP 1500(Тяг)-2500₸', callback_data="PUFFMI_PRICES 2500"),
            types.InlineKeyboardButton('TX 2000(Тяг)-3200₸', callback_data="PUFFMI_PRICES 3200"),
            types.InlineKeyboardButton('DY 4500(Тяг)-5500₸', callback_data="PUFFMI_PRICES 5500"),
            types.InlineKeyboardButton('MESHBOX 5000(Тяг)-6000₸', callback_data="PUFFMI_PRICES 6000"))
        bot.send_message(chat_id=call.message.chat.id, text="Выберите колво тяжек", reply_markup=markup_puffmi)

    elif call.data == "PUFFMI_PRICES 2500":
        tastes_puffmi_markup_2500 = types.InlineKeyboardMarkup(row_width=2)
        tastes_puffmi_markup_2500.add(
            types.InlineKeyboardButton('Quad berry 🍓🫐', callback_data="PUFFMI_TASTE_2500 PUFFMI: PUFFMI: Quad berry"),
            types.InlineKeyboardButton('Lush Ice 🍉❄️', callback_data="PUFFMI_TASTE_2500 PUFFMI: Lush Ice"),
            types.InlineKeyboardButton('Energy Drink 🔋🍹', callback_data="PUFFMI_TASTE_2500 PUFFMI: Energy Drink"),
            types.InlineKeyboardButton('Strawberry Bubble Gum 🍓🧊',
                                       callback_data="PUFFMI_TASTE_2500 PUFFMI: Strawberry Bubble Gum"),
            types.InlineKeyboardButton('Peach Ice 🍑❄️', callback_data="PUFFMI_TASTE_2500 PUFFMI: Peach Ice"),
            types.InlineKeyboardButton('Double Apple 🍎🍏', callback_data="PUFFMI_TASTE_2500 PUFFMI: Double Apple"),
            types.InlineKeyboardButton('Cola ice 🥤❄️', callback_data="PUFFMI_TASTE_2500 PUFFMI: Cola ice"),
            types.InlineKeyboardButton('Cotton Candy 🍭', callback_data="PUFFMI_TASTE_2500 PUFFMI: Cotton Candy"),
            types.InlineKeyboardButton('Grape Ice 🍇❄️', callback_data="PUFFMI_TASTE_2500 PUFFMI: Grape Ice"),
            types.InlineKeyboardButton('Watermelon Berries 🍉🫐',
                                       callback_data="PUFFMI_TASTE_2500 PUFFMI: Watermelon Berries"),
            types.InlineKeyboardButton('Mint Ice 🌿❄️', callback_data="PUFFMI_TASTE_2500 PUFFMI: Mint Ice"),
            types.InlineKeyboardButton('Banana Ice 🍌❄️', callback_data="PUFFMI_TASTE_2500 PUFFMI: Banana Ice"),
            types.InlineKeyboardButton('Bubble Gum 🧊🍬', callback_data="PUFFMI_TASTE_2500 PUFFMI: Bubble Gum"),
            types.InlineKeyboardButton('Strawberry Ice Cream 🍓🍦',
                                       callback_data="PUFFMI_TASTE_2500 PUFFMI: Strawberry Ice Cream"),
            types.InlineKeyboardButton('Back', callback_data="Back_odnorazka"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"))

        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=tastes_puffmi_markup_2500)
    elif call.data.startswith("PUFFMI_TASTE_2500 PUFFMI:"):
        cart[call.data[18:]] = 2500
        update_total()
    elif call.data == "PUFFMI_PRICES 3200":
        tastes_puffmi_markup_3200 = types.InlineKeyboardMarkup(row_width=2)
        tastes_puffmi_markup_3200.add(
            types.InlineKeyboardButton('Cherry Bomb 🍒💣', callback_data="PUFFMI_TASTE_3200 PUFFMI: Cherry Bomb"),
            types.InlineKeyboardButton('Strawberry Kiwi 🍓🥝', callback_data="PUFFMI_TASTE_3200 PUFFMI: Strawberry Kiwi"),
            types.InlineKeyboardButton('Raspberry Lemon 🍇🍋', callback_data="PUFFMI_TASTE_3200 PUFFMI: Raspberry Lemon"),
            types.InlineKeyboardButton('Tobacco 🧑🏻‍🌾', callback_data="PUFFMI_TASTE_3200 PUFFMI: Tobacco"),
            types.InlineKeyboardButton('Gummy Bear 🐻🍬', callback_data="PUFFMI_TASTE_3200 PUFFMI: Gummy Bear"),
            types.InlineKeyboardButton('Banana Ice 🍌❄️', callback_data="PUFFMI_TASTE_3200 PUFFMI: Banana Ice"),
            types.InlineKeyboardButton('Mango Ice 🥭❄️', callback_data="PUFFMI_TASTE_3200 PUFFMI: Mango Ice"),
            types.InlineKeyboardButton('Peach Mango 🍑🥭', callback_data="PUFFMI_TASTE_3200 PUFFMI: Peach Mango"),
            types.InlineKeyboardButton('Cotton Candy 🍭', callback_data="PUFFMI_TASTE_3200 PUFFMI: Cotton Candy"),
            types.InlineKeyboardButton('Lush Ice 🍉❄️', callback_data="PUFFMI_TASTE_3200 PUFFMI: Lush Ice"),
            types.InlineKeyboardButton('Grape Ice 🍇❄️', callback_data="PUFFMI_TASTE_3200 PUFFMI: Grape Ice"),
            types.InlineKeyboardButton('Pink Lemonade 🍋🍓', callback_data="PUFFMI_TASTE_3200 PUFFMI: Pink Lemonade"),
            types.InlineKeyboardButton('Aloe Grape 🍇🌿', callback_data="PUFFMI_TASTE_3200 PUFFMI: Aloe Grape"),
            types.InlineKeyboardButton('Back', callback_data="Back_odnorazka"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"))

        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=tastes_puffmi_markup_3200)
    elif call.data.startswith("PUFFMI_TASTE_3200 PUFFMI:"):
        cart[call.data[18:]] = 3200
        update_total()
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[18:]}добавлен в корзину, сумма корзины:{total}")
    elif call.data == "PUFFMI_PRICES 5500":
        tastes_puffmi_markup_5500 = types.InlineKeyboardMarkup(row_width=2)
        tastes_puffmi_markup_5500.add(
            types.InlineKeyboardButton('Strawberry Ice Cream 🍓🍦',
                                       callback_data="PUFFMI_TASTE_5500 PUFFMI:` Strawberry Ice Cream"),
            types.InlineKeyboardButton('Strawberry Kiwi 🍓🥝',
                                       callback_data="PUFFMI_TASTE_5500 PUFFMI:` Raspberry Lemon"),
            types.InlineKeyboardButton('Pink Lemonade 🍋🍹', callback_data="PUFFMI_TASTE_5500 PUFFMI:` Pink Lemonade"),
            types.InlineKeyboardButton('Energy Drink ⚡️🥤', callback_data="PUFFMI_TASTE_5500 PUFFMI:` Energy Drink"),
            types.InlineKeyboardButton('Grape Ice 🍇❄️', callback_data="PUFFMI_TASTE_5500 PUFFMI:` Grape Ice"),
            types.InlineKeyboardButton('Cola Ice 🥤❄️', callback_data="PUFFMI_TASTE_5500 PUFFMI:` Cola Ice"),
            types.InlineKeyboardButton('Blue Razz 🔵🍭', callback_data="PUFFMI_TASTE_5500 PUFFMI:` Blue Razz"),
            types.InlineKeyboardButton('Cool Mint ❄️🍃', callback_data="PUFFMI_TASTE_5500 PUFFMI:` Cool Mint"),
            types.InlineKeyboardButton('Back', callback_data="Back_odnorazka"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"))
        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=tastes_puffmi_markup_5500)

    elif call.data.startswith("PUFFMI_TASTE_5500 PUFFMI:"):
        cart[call.data[18:]] = 5500
        update_total()
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[18:]}добавлен в корзину, сумма корзины:{total}")
    elif call.data == "PUFFMI_PRICES 6000":
        tastes_puffmi_markup_6000 = types.InlineKeyboardMarkup(row_width=2)
        tastes_puffmi_markup_6000.add(
            types.InlineKeyboardButton('Pink Lemonade 🍋', callback_data="PUFFMI_TASTE_6000 Pink Lemonade"),
            types.InlineKeyboardButton('Watermelon Gummy Bear 🍉🐻',
                                       callback_data="PUFFMI_TASTE_6000 Watermelon Gummy Bear"),
            types.InlineKeyboardButton('Mango Ice 🥭❄️', callback_data="PUFFMI_TASTE_6000 Mango Ice"),
            types.InlineKeyboardButton('Bubble Gum 🍬', callback_data="PUFFMI_TASTE_6000 Bubble Gum"),
            types.InlineKeyboardButton('Banana Ice 🍌❄️', callback_data="PUFFMI_TASTE_6000 Banana Ice"),
            types.InlineKeyboardButton('Peach Ice 🍑❄️', callback_data="PUFFMI_TASTE_6000 Peach Ice"),
            types.InlineKeyboardButton('Peach Mango Watermelon 🍑🥭🍉',
                                       callback_data="PUFFMI_TASTE_6000 Peach Mango Watermelon"),
            types.InlineKeyboardButton('Strawberry Mango 🍓🥭', callback_data="PUFFMI_TASTE_6000 Strawberry Mango"),
            types.InlineKeyboardButton('Strawberry Ice Cream 🍓🍦',
                                       callback_data="PUFFMI_TASTE_6000 Strawberry Ice Cream"),
            types.InlineKeyboardButton('Strawberry Kiwi 🍓🥝', callback_data="PUFFMI_TASTE_6000 Strawberry Kiwi"),
            types.InlineKeyboardButton('Back', callback_data="Back_liquid"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"))
        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=tastes_puffmi_markup_6000)
    elif call.data.startswith("PUFFMI_TASTE_6000"):
        cart[call.data[18:]] = 6000
        update_total()

        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[18:]}добавлен в корзину, сумма корзины:{total}")
        print(cart)
    elif call.data == "CHILLAX":

        markup = types.InlineKeyboardMarkup(row_width=1)
        chillax_price = types.InlineKeyboardButton('6000(Тяг)-6000₸', callback_data="CHILLAX_PRICES 6000")
        markup.row(chillax_price)
        bot.send_photo(call.message.chat.id,
                       "https://zakupka.shop/thumb/2/cemAAVuO-GnwiOh97_g8HQ/r/d/img_20230328_141716.jpg",
                       reply_to_message_id=chillax_price)

        bot.send_message(chat_id=call.message.chat.id, text="Выберите колво тяжек", reply_markup=markup)
    elif call.data == "CHILLAX_PRICES 6000":
        tastes_chillax_markup = types.InlineKeyboardMarkup(row_width=2)
        tastes_chillax_markup.add(
            types.InlineKeyboardButton('Tropic Berries🍇', callback_data="CHILLAX_TASTE_6000 CHILLAX: Tropic Berries"),
            types.InlineKeyboardButton('Blueberry Lemonade🫐🍋',
                                       callback_data="CHILLAX_TASTE_6000 CHILLAX: Blueberry Lemonade"),
            types.InlineKeyboardButton('Pink Lemonade🍋', callback_data="CHILLAX_TASTE_6000 CHILLAX: Pink Lemonade"),
            types.InlineKeyboardButton('Wild Berries🍓', callback_data="CHILLAX_TASTE_6000 CHILLAX: Wild Berries"),
            types.InlineKeyboardButton('Mango🥭', callback_data="CHILLAX_TASTE_6000 CHILLAX: Mango"),
            types.InlineKeyboardButton('Apple🍎', callback_data="CHILLAX_TASTE_6000 CHILLAX: Apple"),
            types.InlineKeyboardButton('Lush Ice🍇❄️', callback_data="CHILLAX_TASTE_6000 CHILLAX: Lush Ice"),
            types.InlineKeyboardButton('Grape Ice🍇❄️', callback_data="CHILLAX_TASTE_6000 CHILLAX:Grape Ice"),
            types.InlineKeyboardButton('Rum Cherry Cola🍒🥤',
                                       callback_data="CHILLAX_TASTE_6000 CHILLAX: Rum Cherry Cola"),
            types.InlineKeyboardButton('Strawberry Kiwi🍓🥝',
                                       callback_data="CHILLAX_TASTE_6000 CHILLAX: Strawberry Kiwi"),
            types.InlineKeyboardButton('Back', callback_data="Back_odnorazka"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"))

        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=tastes_chillax_markup)
    elif call.data.startswith("CHILLAX_TASTE_6000 CHILLAX: "):
        cart[call.data[13:]] = 6000
        update_total()

        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[13:]}добавлен в корзину, сумма корзины:{total}")
    elif call.data == "SAB":
        bot.send_photo(call.message.chat.id,
                       "https://gotoshop.ua/prices/storage/images/product/689/42_mid.jpg?t=1675303460")
        markup_sab = types.InlineKeyboardMarkup(row_width=2)
        markup_sab.add(
            types.InlineKeyboardButton('1500(Тяг)-3000₸', callback_data="SAB_PRICES 3000"),
            types.InlineKeyboardButton('2500(Тяг)-3800₸', callback_data="SAB_PRICES 3800"))
        bot.send_message(chat_id=call.message.chat.id, text="Выберите колво тяжек", reply_markup=markup_sab)

    elif call.data == "SAB_PRICES 3000":
        sab_tastes_markup = types.InlineKeyboardMarkup(row_width=2)
        sab_tastes_markup.add(
            types.InlineKeyboardButton('Pink Lemonade🍋🍹', callback_data="SAB_TASTE_3000 SAB: Pink Lemonade"),
            types.InlineKeyboardButton('Watermelon Gummy Bear🍉🐻',
                                       callback_data="SAB_TASTE_3000 SAB: Watermelon Gummy Bear"),
            types.InlineKeyboardButton('Mango Ice🥭🧊', callback_data="SAB_TASTE_3000 SAB: Mango Ice"),
            types.InlineKeyboardButton('Bubble Gum🍬', callback_data="SAB_TASTE_3000 SAB: Bubble Gum"),
            types.InlineKeyboardButton('Banana Ice🍌🧊', callback_data="SAB_TASTE_3000 SAB: Banana Ice"),
            types.InlineKeyboardButton('Peach Ice🍑🧊', callback_data="SAB_TASTE_3000 SAB: Peach Ice"),
            types.InlineKeyboardButton('Peach Mango Watermelon🍑🥭🍉',
                                       callback_data="SAB_TASTE_3000 SAB: Peach Mango Watermelon"),
            types.InlineKeyboardButton('Strawberry Mango🍓🥭',
                                       callback_data="SAB_TASTE_3000 SAB: Strawberry Mango"),
            types.InlineKeyboardButton('Strawberry Ice Cream🍓🍦',
                                       callback_data="SAB_TASTE_3000 SAB: Strawberry Mango"),
            types.InlineKeyboardButton('Strawberry Kiwi🍓🥝', callback_data="SAB_TASTE_3000 SAB: Strawberry Mango"),
            types.InlineKeyboardButton('Back', callback_data="Back_odnorazka"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"))

        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=sab_tastes_markup)
    elif call.data.startswith("SAB_TASTE_3000"):
        cart[call.data[14:]] = 3000
        update_total()

        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[14:]}добавлен в корзину, сумма корзины:{total}")
    elif call.data == "SAB_PRICES 3800":
        sab_tastes_markup = types.InlineKeyboardMarkup(row_width=2)
        sab_tastes_markup.add(
            types.InlineKeyboardButton('Ice Watermelon 🍉❄️', callback_data="SAB_TASTE_3800 SAB: Ice Watermelon"),
            types.InlineKeyboardButton('Full Energy ⚡️', callback_data="SAB_TASTE_3800 SAB: Full Energy"),
            types.InlineKeyboardButton('Secret 🤫❓', callback_data="SAB_TASTE_3800 SAB: Secret"),
            types.InlineKeyboardButton('Caramel Cream 🍮', callback_data="SAB_TASTE_3800 SAB: Caramel Cream"),
            types.InlineKeyboardButton('Coconut Ice Cream 🥥🍦', callback_data="SAB_TASTE_3800 SAB: Coconut Ice Cream"),
            types.InlineKeyboardButton('Apple Cake 🍎🍰', callback_data="SAB_TASTE_3800 SAB: Apple Cake"),
            types.InlineKeyboardButton('Mix Berries 🍓🫐', callback_data="SAB_TASTE_3800 SAB: Mix Berries"),
            types.InlineKeyboardButton('Wild Cranberry 🍒', callback_data="SAB_TASTE_3800 SAB: Wild Cranberry"),
            types.InlineKeyboardButton('Lemon Juice 🍋', callback_data="SAB_TASTE_3800 SAB: Lemon Juice"),
            types.InlineKeyboardButton('Cucumber Lemonade 🥒🍋', callback_data="SAB_TASTE_3800 SAB: Cucumber Lemonade"),
            types.InlineKeyboardButton('Back', callback_data="Back_odnorazka"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"))

        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=sab_tastes_markup)

    elif call.data.startswith("SAB_TASTE_3800 SAB:"):
        cart[call.data[14:]] = 3800
        update_total()

        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[14:]}добавлен в корзину, сумма корзины:{total}")
    elif call.data == "liquid":

        liquid_markup = types.InlineKeyboardMarkup(row_width=1)
        liquid_markup.add(
            types.InlineKeyboardButton('Husky🐶', callback_data='Markup Husky'),
            types.InlineKeyboardButton("Dual🙿", callback_data='Dual'),
            types.InlineKeyboardButton("XYLINET🖕🏻", callback_data='XYLINET'),
            types.InlineKeyboardButton("Back", callback_data="Back_to_main_choose"))

        bot.send_message(chat_id=call.message.chat.id, text="Выберите жидкость", reply_markup=liquid_markup)
    elif call.data == "Markup Husky":
        bot.send_photo(call.message.chat.id, "https://alibaba-shop.ru/images/products/20221028/10/n_husky.webp")

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("Husky DOUBLE ICE - 2200₸", callback_data="Husky Dobule ice", ),
            types.InlineKeyboardButton("Husky PREMIUM - 2800₸", callback_data='Husky PREMIUM'),
            types.InlineKeyboardButton("Husky MINT SERIES - 2200₸", callback_data='Husky MINT SERIES'),
            types.InlineKeyboardButton('Back', callback_data="Back_liquid"))

        bot.send_message(chat_id=call.message.chat.id, text="Выберите вид", reply_markup=markup)
    elif call.data == "Husky Dobule ice":
        husky_tastes_double_ice = types.InlineKeyboardMarkup(row_width=2)
        husky_tastes_double_ice.add(
            types.InlineKeyboardButton('Pineapple coconut🍍🥥(STRONG)',
                                       callback_data="HDI2200 HaskyDI: Pineapple coconut(STRONG)"),
            types.InlineKeyboardButton('Mango🥭(STRONG)',
                                       callback_data="HDI2200 HaskyDI: Mango(STRONG)"),
            types.InlineKeyboardButton('Orange pineapple apple',
                                       callback_data="HDI2200 HaskyDI:Orange pineapple apple(STRONG)"),
            types.InlineKeyboardButton('Kiwi🥝(STRONG)',
                                       callback_data="HDI2200 HaskyDI: Kiwi(STRONG)"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"),
            types.InlineKeyboardButton('Back', callback_data="Back_liquid"))

        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=husky_tastes_double_ice)
    elif call.data.startswith("HDI2200 HaskyDI"):
        cart[call.data[8:]] = 2200
        update_total()

        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[8:]}добавлен в корзину, сумма корзины:{total}")
    elif call.data == "Husky PREMIUM":
        husky_tastes_double_ice = types.InlineKeyboardMarkup(row_width=2)
        husky_tastes_double_ice.add(
            types.InlineKeyboardButton('choko loko (PREMIUM STRONG)',
                                       callback_data="HP2800 HP: choko loko(PREMIUM STRONG)"),
            types.InlineKeyboardButton('Spark Day(PREMIUM STRONG)',
                                       callback_data="HP2800 HP: Spark Day(PREMIUM STRONG)"),
            types.InlineKeyboardButton('Yoggi Doggy (PREMIUM STRONG)',
                                       callback_data="HP2800 HP: Orange Yoggi Doggy(PREMIUM STRONG)"),
            types.InlineKeyboardButton('Green Land(PREMIUM STRONG)',
                                       callback_data="HP2800 HP: Green Land(PREMIUM STRONG)"),
            types.InlineKeyboardButton('Sweet Dream(PREMIUM STRONG)',
                                       callback_data="HP2800 HP: Sweet Dream(PREMIUM STRONG)"),
            types.InlineKeyboardButton('Dark Flash(PREMIUM STRONG)',
                                       callback_data="HP2800 HP: Dark Flash(PREMIUM STRONG)"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"),
            types.InlineKeyboardButton('Back', callback_data="Back_liquid"))
        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=husky_tastes_double_ice)
    elif call.data.startswith("HP2800 HP:"):
        cart[call.data[7:]] = 2800
        update_total()

        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[7:]}добавлен в корзину, сумма корзины:{total}")
    elif call.data == "Husky MINT SERIES":
        husky_tastes_double_ice = types.InlineKeyboardMarkup(row_width=2)
        husky_tastes_double_ice.add(
            types.InlineKeyboardButton('Orange citrus (STRONG)',
                                       callback_data="HMS2200HMS: Orange citrus(STRONG)"),
            types.InlineKeyboardButton('Strawberry(STRONG)',
                                       callback_data="HMS2200HMS: Strawberry(STRONG)"),
            types.InlineKeyboardButton('Cherry (STRONG)',
                                       callback_data="HMS2200HMS: Cherry (STRONG)"),
            types.InlineKeyboardButton('Blueberry (STRONG)',
                                       callback_data="HMS2200HMS: Blueberry (STRONG)"),
            types.InlineKeyboardButton('Current raspberry (STRONG)',
                                       callback_data="HMS2200HMS Current "
                                                     "raspberry (STRONG)"),
            types.InlineKeyboardButton('Grape (STRONG)',
                                       callback_data="HMS2200HMS Grape (STRONG)"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"),
            types.InlineKeyboardButton('Back', callback_data="Back_liquid"))

        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=husky_tastes_double_ice)
    elif call.data.startswith("HMS2200HMS"):
        cart[call.data[7:]] = 2200
        update_total()

        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[7:]}добавлен в корзину, сумма корзины:{total}")
    elif call.data == "Dual":
        bot.send_photo(call.message.chat.id,
                       "https://vivalacloud.ru/wp-content/uploads/2021/10/photo_2021-10-13-12.45.59.jpeg")

        dual_markup = types.InlineKeyboardMarkup(row_width=2)
        dual_markup.add(
            types.InlineKeyboardButton('Mint bubble gum 🍃🌟',
                                       callback_data="DUAL2500 DUAL: Mint bubble gum"),
            types.InlineKeyboardButton('Fruit candies(STRONG) 🍬🍇',
                                       callback_data="DUAL2500 DUAL: Fruit candies"),
            types.InlineKeyboardButton('Yougurt peach passion fruit(STRONG) 🍑🍓🌟',
                                       callback_data="DUAL2500 DUAL: Yougurt peach passion fruit(STRONG)"),
            types.InlineKeyboardButton('Peach tea (STRONG) 🍑☕️',
                                       callback_data="DUAL2500 DUAL: Peach tea(STRONG)"),
            types.InlineKeyboardButton('Grape mango (STRONG) 🍇🥭🌟',
                                       callback_data="DUAL2500 DUAL: Grape mango(STRONG)"),
            types.InlineKeyboardButton('Lemon candy (STRONG) 🍋🍬🌟',
                                       callback_data="DUAL2500 DUAL: Lemon candy(STRONG)"),
            types.InlineKeyboardButton('Tarhun ice (STRONG) 🌿❄️',
                                       callback_data="DUAL2500 DUAL: Tarhun ice(STRONG)"),
            types.InlineKeyboardButton('Mango ice(STRONG) 🥭❄️',
                                       callback_data="DUAL2500 DUAL: Mango ice(STRONG)"),
            types.InlineKeyboardButton('Plum peach (STRONG) 🍑🍇🌟',
                                       callback_data="DUAL2500 DUAL: Plum peach(STRONG)"),
            types.InlineKeyboardButton('Pineapple kiwi (STRONG) 🍍🥝🌟',
                                       callback_data="DUAL2500 DUAL: Pineapple kiwi(STRONG)"),
            types.InlineKeyboardButton('Strawberry banana(STRONG) 🍓🍌🌟',
                                       callback_data="DUAL2500 DUAL: Strawberry banana"),
            types.InlineKeyboardButton('Cola ice (STRONG) 🥤❄️',
                                       callback_data="DUAL2500 DUAL: Cola ice"),
            types.InlineKeyboardButton('Strawberry orange passion fruit(strong) 🍓🍊🍑🌟',
                                       callback_data="DUAL2500 DUAL: Strawberry orange passion fruit"),
            types.InlineKeyboardButton('Sprite watermelon lime(strong) 💧🍉🍋🌟',
                                       callback_data="DUAL2500 DUAL: Sprite watermelon lime"),
            types.InlineKeyboardButton('Raspberry(strong) 🍇🌟',
                                       callback_data="DUAL2500 DUAL: Raspberry"),
            types.InlineKeyboardButton('Berries tea(strong) 🍓🍇☕️',
                                       callback_data="DUAL2500 DUAL: Berries tea"),
            types.InlineKeyboardButton('Lychee lime passion fruit(strong) 🍈🍋🍑🌟',
                                       callback_data="DUAL2500 DUAL: Lychee lime passion fruit"),
            types.InlineKeyboardButton('Cherry strawberry(strong) 🍒🍓🌟',
                                       callback_data="DUAL2500 DUAL: Cherry strawberry"),
            types.InlineKeyboardButton('Watermelon melon ice(strong) 🍉🍈❄️',
                                       callback_data="DUAL2500 DUAL Watermelon melon ice"),
            types.InlineKeyboardButton('Melon passion fruit(strong) 🍈🍍',
                                       callback_data="DUAL2500 DUAL Melon passion fruit"),
            types.InlineKeyboardButton('Lemon kiwi(strong) 🍋🥝',
                                       callback_data="DUAL2500 DUAL Lemon kiwi"),
            types.InlineKeyboardButton('Currant raspberry apple(strong) 🍇🍓🍎',
                                       callback_data="DUAL2500 DUAL Currant raspberry apple"),
            types.InlineKeyboardButton('Needles forest berries mint 🌲🍇🍓🌿',
                                       callback_data="DUAL2500 DUAL Needles forest berries mint"),
            types.InlineKeyboardButton('Forest berries(strong) 🌳🍇🍓',
                                       callback_data="DUAL2500 DUAL Forest berries"),
            types.InlineKeyboardButton('Watermelon lemonade(strong) 🍉🍋',
                                       callback_data="DUAL2500 DUAL Watermelon lemonade"),
            types.InlineKeyboardButton('Mango orange ice(strong) 🥭🍊❄️',
                                       callback_data="DUAL2500 DUAL Mango orange ice"),
            types.InlineKeyboardButton('Tobacco truffle walnut vanilla(strong) 🚬🍫🌰🍦',
                                       callback_data="DUAL2500 DUAL Tobacco truffle walnut vanilla"),
            types.InlineKeyboardButton('Grapefruit strawberry(strong) 🍇🍓',
                                       callback_data="DUAL2500 DUAL Grapefruit strawberry"),
            types.InlineKeyboardButton('Garden berries(strong) 🌺🍇🍓',
                                       callback_data="DUAL2500 DUAL Garden berries"),
            types.InlineKeyboardButton('Strawberry kiwi(strong) 🍓🥝',
                                       callback_data="DUAL2500 DUAL Strawberry kiwi"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"),
            types.InlineKeyboardButton('Back', callback_data="Back_liquid"))

        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=dual_markup)

    elif call.data.startswith("DUAL2500"):
        cart[call.data[9:]] = 2500
        update_total()

        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[9:]}добавлен в корзину, сумма корзины:{total}")

    elif call.data == "XYLINET":
        bot.send_photo(call.message.chat.id,
                       "https://www.paradoxvapeshop.ru/upload/iblock/878/1dlz89zzgmu78uxiejhx1el21fgowmod.png")

        XYLINET_markup = types.InlineKeyboardMarkup(row_width=2)
        XYLINET_markup.add(
            types.InlineKeyboardButton('Yablochnie proniknivenie',
                                       callback_data="XYLINET2500 XYLINET: Mint bubble gum"),
            types.InlineKeyboardButton('Ananasivyi kasmhot(STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Fruit candies"),
            types.InlineKeyboardButton('Kislo-sladkiy felching(STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Yougurt peach passion fruit"),
            types.InlineKeyboardButton('Yagodnyi gang-bang tea (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Peach tea"),
            types.InlineKeyboardButton('Malinovyi fisting (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Grape mango"),
            types.InlineKeyboardButton('Mangovyi frottaj (STRONG)',
                                       callback_data="XYLINET2500  XYLINET: Grape (STRONG)"),
            types.InlineKeyboardButton('Kaktusovyui kaning (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Kaktusovyui kaning"),
            types.InlineKeyboardButton('Mangovyi frottaj (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Mangovyi frottaj"),
            types.InlineKeyboardButton('Klubnichnyi minet (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Klubnichnyi minet"),
            types.InlineKeyboardButton('Ezhevichnyi BDSM (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Ezhevichnyi BDSM"),
            types.InlineKeyboardButton('Kislo-sladkiy felching (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Kislo-sladkiy felching"),
            types.InlineKeyboardButton('Persilovyi kuni (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Persilovyi kuni"),
            types.InlineKeyboardButton('Apelsinovyi dozhd (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Apelsinovyi dozhd"),
            types.InlineKeyboardButton('Yagodnyi gang-bang (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Yagodnyi gang-bang"),
            types.InlineKeyboardButton('Kink kivi (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Kink kivi"),
            types.InlineKeyboardButton('Malinovyi fisting (STRONG)',
                                       callback_data="XYLINET2500 XYLINET: Kink kivi"),
            types.InlineKeyboardButton('Посмотреть корзину', callback_data="cart"),
            types.InlineKeyboardButton('Back', callback_data="Back_liquid"))

        bot.send_message(chat_id=call.message.chat.id, text="Нажимай и добавляй в корзину",
                         reply_markup=XYLINET_markup)
    elif call.data.startswith("XYLINET2500"):
        cart[call.data[12:]] = 2500
        update_total()

        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Товар: {call.data[12:]}добавлен в корзину, сумма корзины:{total}")

    elif call.data == "Back_odnorazka":
        odnorazka_markup = types.InlineKeyboardMarkup(row_width=2)
        odnorazka_markup.add(
            types.InlineKeyboardButton('WAKA👽', callback_data='WAKA'),
            types.InlineKeyboardButton("PUFFMI😮‍💨", callback_data='PUFFMI'),
            types.InlineKeyboardButton("CHILLAX😎", callback_data="CHILLAX"),
            types.InlineKeyboardButton("SAB💀", callback_data="SAB"))
        bot.send_message(chat_id=call.message.chat.id, text="Выберите одноразку", reply_markup=odnorazka_markup)
    elif call.data == "Back_liquid":
        liquid_markup = types.InlineKeyboardMarkup(row_width=1)
        liquid_markup.add(
            types.InlineKeyboardButton('Husky🐶', callback_data='Markup Husky'),
            types.InlineKeyboardButton("Dual🙿", callback_data='Dual'),
            types.InlineKeyboardButton("XYLINET🖕🏻", callback_data='XYLINET'),
            types.InlineKeyboardButton("Back", callback_data="Back_to_main_choose"))

        bot.send_message(chat_id=call.message.chat.id, text="Выберите жидкость", reply_markup=liquid_markup)
    elif call.data == "Back_to_main_choose":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Жидкости💦', callback_data='liquid'),
                   types.InlineKeyboardButton('Одноразки😤', callback_data='odnorazka'))
        bot.send_message(chat_id=call.message.chat.id, text="Выберите нужный вам товар:",
                         reply_markup=markup)

    elif call.data == 'choose_no':
        markup = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="По кодексу РК, мы не можем продать вам одноразку",
                                                url="https://adilet.zan.kz/rus/docs/K2000000360")
        markup.row(url_button)
        bot.send_message(chat_id=call.message.chat.id, text="Внимание", reply_markup=markup)


#     callback_query_handler(call)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_query_handler(call):
#     if call.data == "number_of_card":
#         card_number = "5356 5020 1526 4454"  # здесь должен быть код, который получает номер карты
#         xerox.copy(card_number)# копировать номер карты в буфер обмена
#         bot.answer_callback_query(call.id, text="Номер карты скопирован в буфер обмена.")
#

# Запускаем бота
bot.polling()
