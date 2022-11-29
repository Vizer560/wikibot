import telebot
from telebot import types
import config
import wikipedia
#Токен
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'help'])
#Главное меню
def menustart(message):
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
   wiki = types.KeyboardButton('Википедия📄')
   about = types.KeyboardButton('О авторе👤')
   markup.add(wiki, about)
   bot.send_sticker(message.chat.id, "CAACAgMAAxkBAAEGL_xjVqdgR-LEzxcPvCGgYYrdB_UMIgACGQAD6grUAoGCPwIWb_xtKgQ")
   bot.send_message(message.chat.id, 'Выбери что будешь делать:', reply_markup=markup)

@bot.message_handler(content_types=['text'])
#Проверка комманд
def main(message):
   #Вкладка Википедия
   if message.text=="Википедия📄":
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
      menu = types.KeyboardButton('Главное меню🧭')
      markup.add(menu)
      who = bot.send_message(message.chat.id, 'Что хотите найти🔎?',reply_markup=markup)
      bot.register_next_step_handler(who, formuy)
   #Вкладка о авторе
   elif message.text=="О авторе👤":
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
      menu = types.KeyboardButton('Главное меню🧭')
      donate = types.KeyboardButton('Купить автору покушать🍴')
      markup.add(menu, donate)
      bot.send_message(message.chat.id, 'Автор @Vizer560 👤', reply_markup=markup)
   #Возращение в главное меню
   elif message.text== 'Главное меню🧭':
      menustart(message)
   #Донат
   elif message.text== 'Купить автору покушать🍴':
      bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEGNDxjWR_TZzt4osTJjUsi21_9PlbMLQACDwADbj6pGDwarhsFMdKkKgQ")
      bot.send_message(message.chat.id, parse_mode='HTML', text='<b>Донат на покушать🍴</b> \n\n💳5375 4112 0004 7863 \n\n🔗https://send.monobank.ua/jar/4Py9qh9Utk')
      menustart(message)
   #Неизвесная комманда
   else:
      bot.send_message(message.chat.id, 'Неизвесная комманда😔')
#Обработка данных принятых у пользователя
def formuy(message):
   who = str((message.text))
   if who == "Главное меню🧭":
      menustart(message)
   else:
      try:
         wikipedia.set_lang("ru")
         sontry = wikipedia.summary(who)
         bot.send_message(message.chat.id, sontry)
         menustart(message)
      except wikipedia.exceptions.PageError:
         bot.send_message(message.chat.id, "Не удалось найти статью🙀")
         menustart(message)
      except wikipedia.exceptions.DisambiguationError:
         bot.send_message(message.chat.id, "Не удалось найти статью🙀")
         menustart(message)
      except telebot.apihelper.ApiTelegramException:
         bot.send_message(message.chat.id, "Слишком длиное предложение попробуйте еще раз но покороче🙀")
         menustart(message)
bot.polling(none_stop=True)
