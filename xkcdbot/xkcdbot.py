# - *- coding: utf- 8 - *-

#@botfather en telegram /new nombre y te da el token y tal


from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,CommandHandler,MessageHandler,CallbackQueryHandler,Filters
from apscheduler.schedulers.background import BackgroundScheduler
import urllib2, json, time, psycopg2, database

sched = BackgroundScheduler()

updater = Updater(token='XXX')
dispatcher = updater.dispatcher

esperoTexto=False

def guardarChat (chatId):
  conn = database.conect()
  database.statement(conn, "create table if not exists chats(chatId varchar);")
  database.statement(conn, "insert into chats (chatId) values('" + str(chatId) + "');")
  database.close(conn)

def guardarLastImg (img):
  conn = database.conect()
  database.statement(conn, "create table if not exists parametros(param varchar, value varchar);")
  database.statement(conn, "CREATE unique INDEX if not exists param ON parametros(param);")
  database.statement(conn, "insert into parametros (param,value) values('lastImg','') on conflict (param) do update set value='" + str(img) + "';")
  database.close(conn)
  
def borrarChat (chatId):
  conn = database.conect()
  database.statement(conn, "delete from chats where chatId='"+str(chatId)+"';")
  database.close(conn)

def truncateChats ():
  conn = database.conect()
  database.statement(conn, "truncate table chats")
  database.close(conn)

def obtenerChats():
  conn = database.conect()
  cur = database.statement(conn, "SELECT * from chats")
  rows = cur.fetchall()
  database.close(conn)
  return rows

def obtenerChat(chatId):
  conn = database.conect()
  cur = database.statement(conn, "SELECT * from chats where chatId='"+str(chatId)+"';")
  rows = cur.fetchall()
  database.close(conn)
  return rows

def obtenerLastImg():
  conn = database.conect()
  cur = database.statement(conn, "SELECT * from parametros where param='lastImg';")
  rows = cur.fetchall()
  database.close(conn)
  return rows

def Xkcdobtainer (comic=""):
  f = urllib2.urlopen('http://xkcd.com/'+comic+'/info.0.json')
  json_string = f.read()
  parsed_json = json.loads(json_string)
  img = parsed_json['img']
  num = parsed_json['num']
  if comic == "":
    guardarLastImg(num)
  f.close()
  return img, num

def start(bot, update):
  update.message.reply_text("ay hola \ndele /help si quieres ayuda")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def help(bot, update):
  update.message.reply_text("/lastxkcd Para sacar el último comic \n/xkcd Para elegir comic \n/automatico Para activar o desactivar que llegue automaticamente el ultimo comic cuando se publique")
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

def borraLosChats(bot, update):
  truncateChats()
  update.message.reply_text("Done")
BorraLosChats_handler = CommandHandler('admin', borraLosChats)
dispatcher.add_handler(BorraLosChats_handler)

def lastXkcd (bot, update):
  img = Xkcdobtainer()
  update.message.reply_photo(img[0])
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

@sched.scheduled_job('cron', day_of_week='mon,wed,fri', hour=17)
def Job():
  rows = obtenerChats()
  if rows != []:
    lastImg = obtenerLastImg()
    img = Xkcdobtainer()
    if str(lastImg[0][1]) != str(img[1]):
      for row in rows:
        chatId=row[0]
        updater.bot.sendPhoto(chatId,photo=img[0])
        if(sched.get_job('repetir')):
          sched.remove_job('repetir')
    else:
      sched.add_job(Job, 'interval', minutes=30, id='repetir', replace_existing=True)
  sched.print_jobs()



def InlineBttn(bot, update):
    query=update.callback_query.data
    chatqueryid=update.callback_query.message.chat.id
    if query == "1":
        rows = obtenerChat(chatqueryid)
        if rows == []:
          guardarChat(chatqueryid)
          bot.send_message(chatqueryid,text='Vale, activado')
        else:
          bot.send_message(chatqueryid,text='Ya estaba activado')  
    else:
      if query == "2":
        borrarChat(chatqueryid)
        bot.send_message(chatqueryid,text='Desactivado')
inlineBttn_handler=CallbackQueryHandler(callback=InlineBttn)
updater.dispatcher.add_handler(inlineBttn_handler)

def root (bot, update):
  if(esperoTexto):
    img=Xkcdobtainer(update.message.text)
    update.message.reply_photo(img[0])
    global esperoTexto
    esperoTexto=False
root_handler = MessageHandler(Filters.text, root)  
dispatcher.add_handler (root_handler)


sched.start()
updater.start_polling()

