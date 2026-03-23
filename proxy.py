# -*- coding: utf-8 -*-
import os
import time
import urllib.request
import json

# CLEAR SCREEN
os.system("clear")

# BANNER (BURAYI İSTERSEN DEĞİŞTİR)
banner = r"""
  _  _______ ____  _____  _____  _____ _      _____ 
 | |/ /_   _|  _ \|  __ \|_   _|/ ____| |    |_   _|
 | ' /  | | | |_) | |__) | | | | (___ | |      | |  
 |  <   | | |  _ <|  _  /  | |  \___ \| |      | |  
 | . \ _| |_| |_) | | \ \ _| |_ ____) | |____ _| |_ 
 |_|\_\_____|____/|_|  \_\_____|_____/|______|_____|
                                                    
                                                    
"""

print(banner)

# INPUT
proxy = input("[+] Proxy gir (IP:PORT): ")

# EKRANI TEMİZLE (gizli hacker havası 😏)
time.sleep(0.5)
os.system("clear")

print("[~] Proxy test ediliyor...\n")

# TEST
try:
    proxy_handler = urllib.request.ProxyHandler({
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    })

    opener = urllib.request.build_opener(proxy_handler)

    start = time.time()
    response = opener.open("http://ip-api.com/json", timeout=5)
    ms = int((time.time() - start) * 1000)

    data = json.loads(response.read().decode())

    ip = data.get("query")
    country = data.get("country")

    print("[✓] PROXY ÇALIŞIYOR\n")
    print(f"IP      : {ip}")
    print(f"Country : {country}")
    print(f"Speed   : {ms} ms")

except Exception:
    print("[✗] PROXY ÇALIŞMIYOR")

print("\n[!] Çıkmak için ENTER")
input()
