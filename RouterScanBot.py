import os
import sys
import telepot
from time import sleep
from settings import token, mac_address,start_msg
import requests

def on_chat_message(msg):
    nameX = ""
    content_type, chat_type, chat_id = telepot.glance(msg)

    command_input = msg['text']

    if command_input == '/start':
        bot.sendMessage(chat_id, start_msg)

    if command_input == '/scan':
        # comando per ricavare le reti
        os.popen("sudo arp-scan")
        raw = os.popen("sudo arp-scan --interface=eth0 --localnet").read()
        sleep(1)
        
        # scarica la lista degli indirizzi conosciuti
        url = mac_address
        r = requests.get(url)
        file = open("address_list.txt", "w")
        file.write(r.text)
        file.close()
        address_list = open("address_list.txt", "r").read()
            
        # elimina parti inutili del messaggio
        base = raw.split("\n")[2:-4]
        a = len(base)
        # crea un for con il numero delle reti trovate
        for i in range(0, a):
            name1 = base[i].split("\t")
            a = address_list.split("\n")
            # crea un fot con il numero delle reti scritte nella lista
            for o in range(0, len(a)):
                ab = a[o].split("&")
                # se la rete trvata è uguale a una rete scritta nella lista
                # scrivi il nome nel messaggio
                if ab[0][:-1].lower().replace(" ","") == name1[1]:
                    try:
                        name = name1[0] + "\t" + ab[1][1:] + "\t" + \
                            name1[1]
                    except:
                        name = name1[0] + "\t" +"\t" + name1[1]
                    
                    nameX += name + "\n"
                    out = sorted(nameX.split("\n"))
        
        msg = '\n'.join(out)
        # invia il messaggio su TG
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
