import telebot
from pytube import YouTube
import os

# Token de acceso del bot de Telegram
TOKEN = '6310943330:AAGa7PveVJ-vowJMslD9Wtli0wLvV_3WzKM'

# Crear instancia del bot
bot = telebot.TeleBot(TOKEN)

# Variable global para almacenar el enlace al video
enlace_video = ""


# Manejar comando /start
@bot.message_handler(commands=['start'])
def inicio(mensaje):
    bot.reply_to(mensaje,
                 '¡Hola! Envíame un enlace de YouTube y te proporcionaré opciones para descargar el contenido.')


# Manejar mensajes de texto con enlaces
@bot.message_handler(func=lambda mensaje: 'youtube.com' in mensaje.text.lower() or 'youtu.be' in mensaje.text.lower())
def manejar_enlace(mensaje):
    global enlace_video
    try:
        # Obtener el enlace del mensaje
        enlace = mensaje.text

        # Verificar si el enlace es válido
        if 'youtube.com' in enlace or 'youtu.be' in enlace:
            enlace_video = enlace

            # Crear botones para descargar el video y el audio
            marcado = telebot.types.InlineKeyboardMarkup()
            marcado.add(telebot.types.InlineKeyboardButton(text='Descargar Video', callback_data='video'),
                        telebot.types.InlineKeyboardButton(text='Descargar Audio', callback_data='audio'))

            # Enviar los botones al usuario
            bot.send_message(mensaje.chat.id, 'Selecciona qué deseas descargar:', reply_markup=marcado)
        else:
            bot.reply_to(mensaje, 'Por favor, envíame un enlace válido de YouTube.')
    except Exception as e:
        print(e)
        bot.reply_to(mensaje, 'No se pudo descargar el video o audio.')


# Manejar la opción seleccionada por el usuario
@bot.callback_query_handler(func=lambda llamada: True)
def respuesta_callback(llamada):
    global enlace_video
    try:
        if llamada.data == 'video':
            video = YouTube(enlace_video)
            video.streams.filter(progressive=True, file_extension='mp4').first().download()
            ruta_video = os.path.join(os.getcwd(), os.path.basename(video.title) + '.mp4')
            archivo_video = open(ruta_video, 'rb')
            bot.send_video(llamada.message.chat.id, archivo_video)
            archivo_video.close()
            os.remove(ruta_video)
        elif llamada.data == 'audio':
            audio_stream = YouTube(enlace_video).streams.filter(only_audio=True, file_extension='mp4').first()
            if audio_stream:
                audio_stream.download()
                # Renombrar archivo para agregar extensión mp3
                ruta_audio = os.path.join(os.getcwd(), os.path.basename(audio_stream.title) + '.mp3')
                os.rename(audio_stream.default_filename, ruta_audio)
                archivo_audio = open(ruta_audio, 'rb')
                bot.send_audio(llamada.message.chat.id, archivo_audio)
                archivo_audio.close()
                os.remove(ruta_audio)
            else:
                bot.reply_to(llamada.message, 'Lo siento, no se encontraron opciones de descarga de audio.')
    except Exception as e:
        print(e)
        bot.send_message(llamada.message.chat.id, 'Ocurrió un error al procesar tu solicitud.')


# Ejecutar el bot
bot.polling()
