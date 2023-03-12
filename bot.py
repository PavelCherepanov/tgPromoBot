import telebot
import config
import random
import datetime
import threading
import time

bot = telebot.TeleBot(config.TELEGRAM_API_TOKEN)


def get_promo_code(num_chars):
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start]
    return code

def generate_random_time():
    hour = str(random.randint(10, 21))
    minutes = str(random.randint(0, 59))
    if(minutes == "0"):
        minutes += str(random.randint(0, 9))
    return str(str(hour) + ":" + str(minutes))

def check_time():
    while(True):
        if (str(datetime.datetime.now().strftime("%H:%M")) == "08:45"):
            global flag 
            flag = True
            send_message_in_group()
            time.sleep(60*60*24-60*60*int(generate_random_time()[0: 2]))
    

@bot.message_handler(commands=["start", "help"])
def send_promo(message):
    global flag
    if(flag == True):
        flag = False
        now_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        code = get_promo_code(6)
        bot.send_message(message.from_user.id, "Привет, ты первый! Получай промокод на скидку 10%! " + code)
        bot.send_message(config.ADMIN_ID, str(now_time) + "\nКод: \n" + code)
    else:
        bot.send_message(message.from_user.id, "К сожалению промокодов нет :(")
        
def send_message_in_group():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Получить промокод', url="https://t.me/paradoxVSBot", callback_data=1))
    bot.send_message(config.GROUP_ID, "Скидка 10% самого быстрого уже ждет:", reply_markup=markup)
    



if __name__ == "__main__":
    thr = threading.Thread(target = check_time)
    thr.start()
    bot.polling(none_stop=True, interval=0)
