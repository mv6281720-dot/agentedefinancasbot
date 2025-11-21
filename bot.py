import os
import telebot
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

gastos = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Seu agente financeiro está ativo! Basta me enviar mensagens como:\n\nex: *gastei 150 gasolina*\n\nque eu anoto automaticamente.")

@bot.message_handler(func=lambda m: True)
def registrar_gasto(message):
    texto = message.text.lower()

    # tenta extrair valores
    valor = None
    for parte in texto.split():
        parte = parte.replace("r$", "").replace(",", ".")
        if parte.replace(".", "").isdigit():
            valor = float(parte)
            break

    if valor is None:
        bot.reply_to(message, "Não consegui entender o valor. Envie algo como: *gastei 120 mercado*")
        return

    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    registro = f"{data} - R$ {valor:.2f} - {message.text}"
    gastos.append(registro)

    bot.reply_to(message, f"Anotado! ✅\n{registro}")

bot.infinity_polling()
