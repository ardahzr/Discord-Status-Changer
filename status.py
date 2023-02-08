from colorama import Fore, init, Style
import requests
import ctypes
import time
import os
import psutil
import bs4
from unidecode import unidecode

ffile=open('token.txt','r').read()
ini=ffile.find("token")+(len("token")+3)
rest=ffile[ini:]
search_enter=rest.find('\n')
token2=str(rest[:search_enter])

ini=ffile.find("city")+(len("city")+3)
rest=ffile[ini:]
search_enter=rest.find('\n')
city2=str(rest[:search_enter])

ffile=open('token.txt','r').close()

ctypes.windll.kernel32.SetConsoleTitleW('Discord Status Changer')
init(convert=True, autoreset=True)
SuccessCounter = 0
os.system('cls')

UPDATE_DELAY = 1 
def get_size(bytes):
    for unit in ['', ' K', ' M', ' G', ' T', ' P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}bp"
        bytes /= 1024

io = psutil.net_io_counters()
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv
x = 0
option = 1

if option == 1:
    os.system('cls')
    token = token2.replace('"','')
    print(' ')
    def ChangeStatus():
        global SuccessCounter
        global x
        global bytes_sent, bytes_recv
        time.sleep(1)
        io_2 = psutil.net_io_counters()
        us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
        download = str("Download: " + get_size(ds*5.4) + "s")
        upload = str("Upload: " + get_size(us*5.4) + "s")
        bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv

        city = city2.replace('"','')
        url = "https://www.google.com/search?q="+"weather"+city
        html = requests.get(url).content
        soup = bs4.BeautifulSoup(html, 'html.parser')
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        yazi = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
        data = yazi.split('\n')
        sky = data[1]
        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        strd = listdiv[5].text
        pos = strd.find('Wind')
        other_data = strd[pos:]


        try:
            session = requests.Session()
            headers = {
                'authorization': token,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                'content-type': 'application/json'
            } 
            liste = ["CPU: %" + str(psutil.cpu_percent()), "RAM: %"+ str(psutil.virtual_memory().percent), download, upload, "Istanbul Hava: "+temp.replace("°"," .")+"", unidecode(sky)]
            text = liste[x]
            data = '{"custom_status":{"text":"' + text + '"}}' 
            r = session.patch('https://discordapp.com/api/v6/users/@me/settings', headers=headers, data=data)
            x += 1
            if '"custom_status": {"text": "' in r.text:
                print(Fore.GREEN + '[SUCCESS] ' + Fore.WHITE + Style.BRIGHT + 'Status changed: ' + str(text))
                SuccessCounter += 1
                ctypes.windll.kernel32.SetConsoleTitleW('Discord Status Changer | Success: ' + str(SuccessCounter))
            else:
               print(r.text)
        except:
            pass
        if x == len(liste):
            x = 0
    while True:
        ChangeStatus()
