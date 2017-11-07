import os
import sys
import telepot
from time import sleep
from settings import token, mac_address, start_msg


def on_chat_message(msg):
    nameX = ""
    content_type, chat_type, chat_id = telepot.glance(msg)

    command_input = msg['text']

    if command_input == '/start':
        bot.sendMessage(chat_id, start_msg)

    if command_input == '/scan':
        raw = os.popen("sudo arp-scan --interface=eth0 --localnet").read()
        base = raw.split("\n")[2:-4]
        a = len(base)        
        for i in range(0, a):
            name1 = base[i].split("\t")
            try:
                name = name1[0] + "\t" + mac_address[name1[1].upper()] + "\t" + \
                      name1[1]
            except:
                name = name1[0] + "\t" + name1[2] + "\t" + name1[1]
            
            nameX += name + "\n"
            out = sorted(nameX.split("\n"))
        bot.sendMessage(chat_id, '\n'.join(out))
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
