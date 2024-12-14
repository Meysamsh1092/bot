import os
import re

# Function to clear the screen and display the logo
def display_logo():
    os.system("clear")  # Clear the terminal screen
    logo = """
\033[1;31m#########################################################\033[0m
\033[1;31m#                                                       #\033[0m
\033[1;31m#                      ███╗   ███╗                      #\033[0m
\033[1;31m#                      ████╗ ████║                      #\033[0m
\033[1;31m#                      ██╔████╔██║                      #\033[0m
\033[1;31m#                      ██║╚██╔╝██║                      #\033[0m
\033[1;31m#                      ██║ ╚═╝ ██║                      #\033[0m
\033[1;31m#                      ╚═╝     ╚═╝                      #\033[0m
\033[1;31m#                                                       #\033[0m
\033[1;31m#                   M E Y S A M S H 1 0 9 2             #\033[0m
\033[1;31m#########################################################\033[0m
"""
    print(logo)
    print("\n")

# Function to download and set up initial files and service
def download_and_setup():
    try:
        # Download db.py file
        os.system("curl -o /root/db.py https://raw.githubusercontent.com/meysamsh1092/bot/main/db.py")
        print("File db.py downloaded and saved to /root.")
        
        # Install required packages
        os.system("apt install curl socat -y && apt install pip -y && apt install screen -y && apt install python3-pip -y")
        os.system("pip3 install python-telegram-bot && pip3 install --force-reinstall -v 'python-telegram-bot==13.5' && pip install telegram-send")
        print("Packages installed successfully.")
        
        # Set permissions for db.py
        os.system("chmod +x /root/db.py")
        print("Permissions for db.py set successfully.")

        # Create the service file
        service_content = """
[Unit]
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
            service_file.write(service_content.strip())
        print("Service file db.service created successfully.")

        # Enable and start the service
        os.system("systemctl daemon-reload && systemctl enable db.service && systemctl start db.service && systemctl restart db.service")
        print("Service db started successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to update the sleep time
def update_time():
    try:
        # Get the new time from the user
        hours = float(input("Enter the number of hours: "))
        seconds = int(hours * 3600)
        
        # Update the time.sleep value in db.py
        with open("/root/db.py", "r") as file:
            data = file.read()
        
        if "time.sleep" in data:
            # Replace the value inside time.sleep()
            data = re.sub(r"time\.sleep\(\d+\)", f"time.sleep({seconds})", data)
            with open("/root/db.py", "w") as file:
                file.write(data)
            print(f"Delay time updated to {seconds} seconds.")
            
            # Restart the service
            os.system("systemctl restart db.service")
            print("Service restarted successfully.")
        else:
            print("time.sleep not found in db.py.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to restart the service
def restart_service():
    try:
        os.system("systemctl restart db.service")
        print("Service restarted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main menu
def main():
    while True:
        display_logo()  # Clear screen and show logo
        print("Select an option:")
        print("1. Download and set up")
        print("2. Update delay time")
        print("3. Restart service")
        print("4. Exit")
        
        choice = input("\nYour choice: ")
        
        if choice == "1":
            download_and_setup()
        elif choice == "2":
            update_time()
        elif choice == "3":
            restart_service()
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to return to the main menu...")  # Wait for user to press Enter
        display_logo()  # Clear screen and show logo again

if __name__ == "__main__":
    main()
