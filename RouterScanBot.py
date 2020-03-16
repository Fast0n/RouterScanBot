import os
import sys
import telepot
from time import sleep
from settings import token, mac_address, start_msg
import requests
import validators
from telepot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import json

interface = "en0"


def on_chat_message(msg):
    final = ""
    content_type, chat_type, chat_id = telepot.glance(msg)
    command_input = msg['text']

    if command_input == '/start':
        markup = ReplyKeyboardMarkup(keyboard=[["📡Scansiona", "📈Speedtest"]], resize_keyboard=True,
                                     one_time_keyboard=True)
        bot.sendMessage(chat_id, start_msg, reply_markup=markup)

    if command_input == '/scan' or command_input == "📡Scansiona":
        if not validators.url(mac_address):
            bot.sendMessage(chat_id, "URL non valido")
            sys.exit()
        else:
            wjdata = requests.get(mac_address).json()

        # comando per ricavare le reti
        raw = os.popen("arp-scan --interface=" +
                       interface + " --localnet").read()
        sleep(1)

        # sapere il numero dei dispositivi collegati
        base = raw.split("\n")
        a = len(base)
        lunghezza = str(base[int(a) - 2:-1]).split(".")
        b = len(lunghezza)
        lunghezza = str(lunghezza[int(b) - 1])[:-2]

        # elimina parti inutili del messaggio
        lista = raw.split("\n")[2:-4]
        c = len(lista)

        for i in range(0, c):

            # estrare elementi dalla lista
            ip = lista[i].split("\t")[0]
            mac = lista[i].split("\t")[1]
            desc = lista[i].split("\t")[2]
            try:
                name = wjdata['data']['macaddress'][0][mac]
            except:
                if ip == "192.168.1.1":
                    name = "Modem"
                else:
                    name = "Sconosciuto"

            final += ("["+ip + "]("+ip+") *" + name +
                      "*\n```" + mac + "``` _" + desc + "_\n\n")

        # invia il messaggio su TG
        msg = "*IP\t| Nome\t|Mac Adress\t| Tecnologia\n\n*" +\
            final + "`" + \
            lunghezza.replace("responded", "Dispositivi")[
                1:] + "`\n\nFonte([Qui]("+mac_address+"))"
        bot.sendMessage(chat_id, msg, parse_mode='Markdown')

    if command_input == '/speedtest' or command_input == "📈Speedtest":
        sent = bot.sendMessage(
            chat_id, "SpeedTest in corso...\nIl tempo varia in base alla tua connessione")
        edited = telepot.message_identifier(sent)
        raw = os.popen("speedtest").read()
        raw = raw.split("\n")
        raw = ('\n'.join(raw[1:2]) + "\n" + str(raw[4]) +
               "\n" + str(raw[6]) + "\n" + str(raw[8]))
        bot.editMessageText(edited, raw)


# Main
print("Avvio RouterScanBot")

# PID file
pid = str(os.getpid())
pidfile = "/tmp/RouterScanBot.pid"

# Check if PID exist
if os.path.isfile(pidfile):
    print("%s already exists, exiting!" % pidfile)
    sys.exit()

# Create PID file
f = open(pidfile, 'w')
f.write(pid)

# Start working
try:
    bot = telepot.Bot(token)
    bot.message_loop(on_chat_message)
    while(1):
        sleep(10)
finally:
    os.unlink(pidfile)
