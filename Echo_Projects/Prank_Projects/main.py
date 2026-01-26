import time
import random

def loading(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.05)
    print()

print("Initializing system...")
time.sleep(1)

loading("Connecting to secure server █▒▒▒▒▒▒▒▒▒ 10%")
time.sleep(1)
loading("Bypassing firewall ███▒▒▒▒▒▒▒ 30%")
time.sleep(1)
loading("Accessing mainframe █████▒▒▒▒▒ 50%")
time.sleep(1)
loading("Decrypting passwords ███████▒▒▒ 70%")
time.sleep(1)
loading("Downloading data █████████▒▒ 90%")
time.sleep(1)
loading("HACK COMPLETE ███████████ 100%")

print("\n⚠ WARNING ⚠")
time.sleep(1)

names = ["Instagram", "WhatsApp", "Bank", "School Server", "WiFi Router"]
for i in range(5):
    print(f"Hacking {random.choice(names)}...")
    time.sleep(0.7)

print("\n😈 SYSTEM BREACHED 😈")
time.sleep(1)
print("Just kidding 😂")
print("This is a FAKE hacker prank made by Aaryan 😎")
