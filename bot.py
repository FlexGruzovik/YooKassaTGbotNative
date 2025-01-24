import telebot
import json

bot = telebot.TeleBot('*****TOKEN*****')

bot.set_webhook()

from telebot import types
from telebot.types import LabeledPrice, ShippingOption

provider_data = json.dumps({
                "receipt": {
                    "customer" : {
                            "email" : "*****EMAIL FOR RECEIPT*****"
                        },
                    "items": [
                        {
                            "description": "*****ITEM NAME*****",
                            "quantity": 1.000,
                            "amount": {
                                "value": 150.00,
                                "currency": "RUB"
                            },
                            "vat_code": 1,
                            "payment_mode": "full_payment",
                            "payment_subject": "service"
                        }
                    ]
                }
            })

mm = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button1 = types.KeyboardButton("Yes✔️")
button2 = types.KeyboardButton("No❌")
mm.add(button1,button2)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "u wanna + vibe?", reply_markup=mm)

@bot.message_handler(content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def handler(message):
    if message.text == "Yes✔️":
        prices = [LabeledPrice(label='+ vibe', amount=15000)]
        bot.send_invoice(message.from_user.id, title='u need to pay for + vibe',
                         description='bro',
                         provider_token='*****YOOKASSA TOKEN*****',
                         currency='RUB',
                         photo_url='https://medialeaks.ru/wp-content/uploads/2021/10/dasha1280h960-2-1.jpg',
                         need_email=True,
                         send_email_to_provider=True,
                         is_flexible=False,
                         prices=prices,
                         start_parameter='start_parameter',
                         invoice_payload='coupon',
                         provider_data=provider_data)
    if message.text == "No❌":
        bot.send_message(message.chat.id, "Shit")

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print(pre_checkout_query.id)
    print(pre_checkout_query.total_amount)
    print(pre_checkout_query.from_user)
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def process_successful_payment(message):
    bot.send_photo(message.chat.id, caption="Your + vibe", photo='https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fdevkis.club%2Fuploads%2Fposts%2F2023-01%2F1673849285_1-devkis-club-p-erotika-devushek-s-uprugoi-grudyu-1.jpg&lr=47&pos=22&rpt=simage&text=%D0%A1%D0%B8%D1%81%D1%8C%D0%BA%D0%B8')

bot.polling(none_stop=True, interval=0)