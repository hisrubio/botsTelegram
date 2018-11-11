# - *- coding: utf- 8 - *-

#@botfather en telegram /new nombre y te da el token y tal

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackQueryHandler
import youtube_dl

updater = Updater(token='XXX')
dispatcher = updater.dispatcher

opcion=0
url=False

def start(bot, update):
  update.message.reply_text("hola")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def help(bot, update):
    update.message.reply_text("/descargar para descargar musica o video de youtube")
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

def descargar(bot, update):
      keyboard = [
            [InlineKeyboardButton("MUSICA", callback_data='1'), InlineKeyboardButton("VIDEO", callback_data='2')]
            ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      update.message.reply_text("Vale, ¿que quieres?",reply_markup=reply_markup)
descargar_handler = CommandHandler('descargar', descargar)
dispatcher.add_handler(descargar_handler)  

def coach(bot,update):
      query=update.callback_query.data
      chatqueryid=update.callback_query.message.chat.id
      
      global opcion
      global url
      if query == "1":
            opcion=1
            url=True
      elif query == "2":
            opcion=2
            url=True
                  
      bot.send_message(chatqueryid,text='va, pues mandame la url')

coach_handler=CallbackQueryHandler(callback=coach)
dispatcher.add_handler(coach_handler)

def messageCoach(bot,update):
      if url:
            obtainer(bot,update,update.message.text)
            global url
            url=False
message_handler = MessageHandler(Filters.text, messageCoach)  
dispatcher.add_handler (message_handler)

def obtainer(bot,update, video):
      ydl_opts={}
      extension=""
      if opcion == 1:
            print "-----------------mp3-------------------"
            ydl_opts = {
                  'format': 'bestaudio/best',
                  'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                  }],
                  'noplaylist' : True
            }
            extension=".mp3"
      elif opcion == 2:
            print "-------------------mp4-------------------"
            ydl_opts = {
                  'format': 'bestvideo[ext=mp4]+bestaudio[acodec=aac],mp4',
                  'audioformat' :'aac',
                  'merge_output_format' : 'mp4',
                  'noplaylist' : True
            }
            extension=".mp4"

      update.message.reply_text("ahora te lo envio")

      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(video, download=False)

        ydl.download([video])

      titulo = (meta['title'])
      videoid = meta['id']
      nombre_archivo = titulo+"-"+videoid+extension
      ruta = "/home/miguel/cosas/ejs python/"+ nombre_archivo
      update.message.reply_video(open(str(ruta), 'rb'))
   


updater.start_polling()
updater.idle()