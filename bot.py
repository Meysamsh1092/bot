import os
import time

def download_and_setup():
    # دانلود فایل db.py
    os.system("curl -o /root/db.py https://raw.githubusercontent.com/meysamsh1092/bot/main/db.py")
    print("file downloaded")
    
    # نصب دستورات
    os.system("apt install curl socat -y && apt install pip -y && apt install screen -y && apt install python3-pip -y")
    os.system("pip3 install python-telegram-bot && pip3 install --force-reinstall -v 'python-telegram-bot==13.5' && pip install telegram-send")
    os.system("telegram-send --configure")
    print("installed")
    
    #acc  db.py
    os.system("chmod +x /root/db.py")
    print("acc done.")
    
    #  create db.service
    service_content = """[Unit]
Description=Backup service
After=multi-user.target
[Service]
User=root
Type=simple
Environment=PYTHONUNBUFFERED=1
WorkingDirectory=/root/
ExecStart=/usr/bin/python3 /root/db.py
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartSec=42s
[Install]
WantedBy=multi-user.target
"""
    with open("/etc/systemd/system/db.service", "w") as service_file:
        service_file.write(service_content)
    print(" db.service created .")
    
    #  run systemctl
    os.system("systemctl daemon-reload && sudo systemctl enable db.service && sudo systemctl start db.service && sudo systemctl restart db.service")
    print(" db service created .")

def update_time():
    try:
        hours = float(input(" Enter time(hour): "))
        seconds = int(hours * 3600)
        with open("/root/db.py", "r") as file:
            data = file.read()
        data = data.replace("time.sleep(3600)", f"time.sleep({seconds})")
        with open("/root/db.py", "w") as file:
            file.write(data)
        print(f" time change to {seconds} .")
    except Exception as e:
        print(f"fail: {e}")

def restart_service():
    os.system("sudo systemctl restart db.service")
    print(" db service restarted .")

def main():
    while True:
        print("choise:")
        print("1.install")
        print("2. time ")
        print("3. restart")
        print("4. exit")
        
        choice = input("choise: ")
        if choice == "1":
            download_and_setup()
        elif choice == "2":
            update_time()
        elif choice == "3":
            restart_service()
        elif choice == "4":
            print("exit")
            break
        else:
            print("try again")

if __name__ == "__main__":
    main()
