import os
import sys
import telepot
from time import sleep
from settings import token, mac_address, start_msg
import requests

def on_chat_message(msg):
    findX = ""
    notfindX = ""
    content_type, chat_type, chat_id = telepot.glance(msg)

    command_input = msg['text']

    if command_input == '/start':
        bot.sendMessage(chat_id, start_msg)

    if command_input == '/speedtest':
        sent = bot.sendMessage(chat_id, "SpeedTest in corso...\nIl tempo varia in base alla tua connessione")
        edited = telepot.message_identifier(sent)
        raw = os.popen("speedtest").read()
        raw = raw.split("\n")
        raw = ('\n'.join(raw[1:2]) + "\n" + str(raw[4]) + "\n" + str(raw[6]) + "\n" + str(raw[8]))
        bot.editMessageText(edited, raw)
        
    if command_input == '/scan':
        # comando per ricavare le reti
        os.popen("sudo ls").read()
        raw = os.popen("sudo arp-scan --interface=eth0 --localnet").read()
        sleep(1)

        # scarica la lista degli indirizzi conosciuti
        url = mac_address
        r = requests.get(url)
        file = open("address_list.txt", "w")
        file.write(r.text)
        file.close()
        address_list = open("address_list.txt", "r").read()

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
            righa = lista[i]
            
            # estrare il mac address dalla lista
            divisione = lista[i].split("\t")[1:-1]
            d = len(divisione)

            for o in range(0, d):
                elementi = divisione[o]
                # crea la lista
                url = address_list.split("\n")
                e = len(url)

                for j in range(0, e):
                    indirizzi = url[j]
                    if not url[j].find(divisione[o].upper()) == -1:
                        name = url[j].split("&")
                        name = name[1]

                        findX += str(lista[i].split("\t")[-3]) + "\t" +\
                            name[1:] + "\n" +\
                            divisione[o].upper() + "\t" +\
                            str(lista[i].split("\t")[-1]) + "_ "
                        break
                    if not elementi in address_list and j == e - 1:
                        notfindX += str(lista[i].split("\t")[-3]) + "\t" +\
                            "Sconosciuto" + "\n" +\
                            elementi.upper() + "\t" +\
                            str(lista[i].split("\t")[-1]) + "\n\n"
                    else:
                        notfindX = ""

        # invia il messaggio su TG
        msg = "IP\t| Nome\t|Mac Adress\t| Tecnologia\n" +\
            findX.replace("_ ", "\n\n") + notfindX +\
            lunghezza.replace("responded", "Dispositivi")[1:]
        bot.sendMessage(chat_id, msg)


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
