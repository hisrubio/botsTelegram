# - *- coding: utf- 8 - *-

#@botfather en telegram /new nombre y te da el token y tal


from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,CommandHandler,MessageHandler,CallbackQueryHandler,Filters
import urllib2, json, time, schedule

updater = Updater(token='XXX')
dispatcher = updater.dispatcher

esperoTexto=False
comicAutomatico=False
chatIdComicAutomatico=None
botComicAutomatico=None

def Xkcdobtainer (comic=""):
  f = urllib2.urlopen('http://xkcd.com/'+comic+'/info.0.json')
  json_string = f.read()
  parsed_json = json.loads(json_string)
  img = parsed_json['img']
  f.close()
  return img

def start(bot, update):
  update.message.reply_text("Hola! \n /help si quieres ayuda")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def help(bot, update):
  update.message.reply_text("/lastxkcd Para sacar el último comic \n/xkcd Para elegir comic \n/automatico Para activar o desactivar que llegue automaticamente el ultimo comic cuando se publique")
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

def lastXkcd (bot, update):
  img = Xkcdobtainer()
  update.message.reply_photo(img)
lastXkcd_handler = CommandHandler('lastxkcd', lastXkcd)  
dispatcher.add_handler (lastXkcd_handler)

def Xkcd (bot, update):
  global esperoTexto
  esperoTexto=True
  update.message.reply_text("introduce numero")
Xkcd_handler = CommandHandler('xkcd', Xkcd)  
dispatcher.add_handler (Xkcd_handler)

def Automatico(bot, update):
  keyboard = [
      [InlineKeyboardButton("Si", callback_data='1'),InlineKeyboardButton("No", callback_data='2')]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  update.message.reply_text("¿Quieres recibir el ultimo comic cada vez que se publique uno nuevo?",reply_markup=reply_markup)
automatico_handler = CommandHandler('automatico', Automatico)
dispatcher.add_handler(automatico_handler)

def Job():
  if(comicAutomatico):
    img = Xkcdobtainer()
    botComicAutomatico.sendPhoto(chatIdComicAutomatico,photo=img)



def InlineBttn(bot, update):
    query=update.callback_query.data
    chatqueryid=update.callback_query.message.chat.id
    
    if query == "1":
        bot.send_message(chatqueryid,text='Vale, activado')
        global comicAutomatico
        comicAutomatico=True
        global chatIdComicAutomatico
        chatIdComicAutomatico=chatqueryid
        global botComicAutomatico
        botComicAutomatico=bot
    else:
      if query == "2":
        bot.send_message(chatqueryid,text='Desactivado')
        global comicAutomatico
        comicAutomatico=False
        global chatIdComicAutomatico
        chatIdComicAutomatico=None
        global botComicAutomatico
        botComicAutomatico=None
inlineBttn_handler=CallbackQueryHandler(callback=InlineBttn)
updater.dispatcher.add_handler(inlineBttn_handler)

def root (bot, update):
  if(esperoTexto):
    img=Xkcdobtainer(update.message.text)
    update.message.reply_photo(img)
    global esperoTexto
    esperoTexto=False
root_handler = MessageHandler(Filters.text, root)  
dispatcher.add_handler (root_handler)


schedule.every().monday.at("17:00").do(Job)
schedule.every().wednesday.at("17:00").do(Job)
schedule.every().friday.at("17:00").do(Job)

while True:
    schedule.run_pending()
    updater.start_polling()
    updater.idle()



