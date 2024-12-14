import os
import time
import socket
while True:
    os.system("telegram-send --file /etc/x-ui/x-ui.db --caption server:$(hostname -I)")
    time.sleep({DELAY})
