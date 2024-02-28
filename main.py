import telebot
from pytube import YouTube
import os

TOKEN = '6310943330:AAGa7PveVJ-vowJMslD9Wtli0wLvV_3WzKM'

# Creamos el acceso al bot
bot = telebot.TeleBot(TOKEN)

# Recibiendo y ocupando el comando /start
@bot.message_handler(commands=['start'])
def mensajeStart(mensaje):
    bot.reply_to(mensaje, "Hola, ya estoy activo. Enviame cualquier link de youtube y te ayudare con la descarga.")

