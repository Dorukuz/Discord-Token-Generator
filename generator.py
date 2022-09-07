import os, time, json, random, base64, threading, re, sys
try: import requests, colorama, cursor; from capmonster_python import HCaptchaTask
except: os.system('pip install -q capmonster-python websocket requests colorama cursor')
import requests, colorama, cursor; from capmonster_python import HCaptchaTask
from colorama import *
from pystyle import *
import hashlib


System.Title("Axi Token Generator ^| Made By Dorukuz#4555")
axi = """
                                                     ███
                           ▄████████ ▀████    ▐████▀   
                          ███    ███   ███▌   ████▀  ███  
                          ███    ███    ███  ▐███    ███▌ 
                          ███    ███    ▀███▄███▀    ███▌ 
                        ▀███████████    ████▀██▄     ███▌ 
                          ███    ███   ▐███  ▀███    ███  
                          ███    ███  ▄███     ███▄  ███  
                          ███    █▀  ████       ███▄ ███  
                                                                                 
              
              ⌜――――――――――――――――――――――――――――――――――――――――――――――――――――⌝
              ┇      [Discord] https://discord.gg/qQrMUXp2M2       ┇
              ┇      [Github]  https://github.com/Dorukuz          ┇
              ⌞――――――――――――――――――――――――――――――――――――――――――――――――――――⌟



                              › Press Enter...
"""
axigen = """
                                      
      ▄██████▄     ▄████████ ███▄▄▄▄      ▄████████    ▄████████    ▄████████     ███      ▄██████▄     ▄████████ 
     ███    ███   ███    ███ ███▀▀▀██▄   ███    ███   ███    ███   ███    ███ ▀█████████▄ ███    ███   ███    ███ 
     ███    █▀    ███    █▀  ███   ███   ███    █▀    ███    ███   ███    ███    ▀███▀▀██ ███    ███   ███    ███ 
    ▄███         ▄███▄▄▄     ███   ███  ▄███▄▄▄      ▄███▄▄▄▄██▀   ███    ███     ███   ▀ ███    ███  ▄███▄▄▄▄██▀ 
   ▀▀███ ████▄  ▀▀███▀▀▀     ███   ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   ▀███████████     ███     ███    ███ ▀▀███▀▀▀▀▀   
     ███    ███   ███    █▄  ███   ███   ███    █▄  ▀███████████   ███    ███     ███     ███    ███ ▀███████████ 
     ███    ███   ███    ███ ███   ███   ███    ███   ███    ███   ███    ███     ███     ███    ███   ███    ███ 
     ████████▀    ██████████  ▀█   █▀    ██████████   ███    ███   ███    █▀     ▄████▀    ▀██████▀    ███    ███ 
                                                      ███    ███                                       ███    ███ 
                                                   
                                                   > Press Enter..."""
System.Size(200,40)
Anime.Fade(Center.Center(axi), Colors.rainbow, Colorate.Vertical, interval=0.020, enter=True)
Anime.Fade(Center.Center(axigen), Colors.rainbow, Colorate.Vertical, interval=0.020, enter=True)

class Booster:
    def __init__(self) -> None:
        colorama.init()
        cursor.hide()
        
        self.config         = json.load(open('./data/config.json', 'r'))
        self.proxies        = open('./data/proxies.txt', 'r').read().splitlines()
        if not len(self.proxies):
            print(f"\n{Fore.RED}[{Fore.RESET}{Fore.MAGENTA}!{Fore.RESET}{Fore.RED}]{Fore.RESET} No proxy found in proxy folder.\n{Fore.RED}[{Fore.RESET}{Fore.MAGENTA}!{Fore.RESET}{Fore.RED}]{Fore.RESET} Please edit the config file in the data folder.") # err if no proxy in data/proxies.txt
            time.sleep(10)
            os._exit(0)
        self.usernames      = open('./data/usernames.txt', 'r',encoding='utf8').read().splitlines()

        
        self.threads        = self.config['threads']
        self.capmonster_key = self.config['capmonster_key']
        self.invite_code    = self.config['invite_code']
        self.online_tokens  = self.config['online_tokens']
        self.password       = self.config['password']
        self.captcha_tokens = []
        
        self.lock    = threading.Lock()
        
        self.lerror    = f"{Fore.RED}[{Fore.RESET}{Fore.MAGENTA}*{Fore.RESET}{Fore.RED}]{Fore.RESET}"
        self.lcaptcha  = f"{Fore.GREEN}[{Fore.RESET}{Fore.MAGENTA}!{Fore.RESET}{Fore.GREEN}]{Fore.RESET}"
        self.ljoined   = f"{Fore.BLUE}[{Fore.RESET}{Fore.MAGENTA}>{Fore.RESET}{Fore.BLUE}]{Fore.RESET}"

        self.red      = colorama.Fore.RED
        self.green    = colorama.Fore.GREEN
        self.blue    = colorama.Fore.BLUE
        self.cyan     = colorama.Fore.CYAN
        self.purp     = colorama.Fore.MAGENTA
        
    def __name__(self) -> str:
        username = random.choice(self.usernames)
        return username
    
    def __email__(self) -> str:
        domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com", "@protonmail.com"]
        email =  "axi" + "_" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8)) + random.choice(domains)
        return email
    
    def __properties__(self):
        data = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
            "browser_version": "102.0.5005.61",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": 130153,
            "client_event_source": None
        }

        return base64.b64encode(json.dumps(data).encode()).decode()
    
    def print(self, arg):
        self.lock.acquire()
        print(arg)
        self.lock.release()
        
    def __headers__(self, session: requests.Session) -> str:
        cookies = ""
        for item in session.cookies.items(): 
            cookies += "=".join(item) + '; ' 

        return cookies
    
    def __cookies__(self, session: requests.Session, proxy) -> list:
        try:
            proxies = {
                "http": f'http://{proxy}',
                "https": f'http://{proxy}'
            }

            url = "https://discord.com/"

            headers = {
                "host": "discord.com",
                "connection": "keep-alive",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "sec-fetch-site": "none",
                "sec-fetch-mode": "navigate",
                "sec-fetch-user": "?1",
                "sec-fetch-dest": "document",
                "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9"
            }
            
            response = session.get(url, headers=headers, proxies=proxies)
            
            __dcfduid, __sdcfduid = re.findall('[a-z0-9]{32,96}', response.headers["set-cookie"])
            return __dcfduid, __sdcfduid
        except:
            proxy = random.choice(self.proxies)
            self.__cookies__(session , proxy)

    def __main__(self):
        while threading.active_count() < self.threads:
            threading.Thread(target=self.__captcha__).start()
    
    def __gen__(self, captcha_token: str, proxy: str) -> None:
        try:
            session = requests.Session()
            self.__cookies__(session , proxy)
            
            email = self.__email__()
            username = self.__name__()
            
            payload = {
                "captcha_service": "hcaptcha",
                "captcha_key": captcha_token,
                "consent": "true",
                "date_of_birth": "2000-02-13",
                "email": f"{email}",
                "gift_code_sku_id": "null",
                "invite": self.config['invite_code'],
                "password": self.config['password'],
                "promotional_email_opt_in": "false",
                "username": username,
            }
            
            headers = {
                'Host': 'discord.com', 
                'X-Super-Properties': self.__properties__(),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) sAppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47",
                'X-Debug-Options': 'bugReporterEnabled',
                "Cookie": self.__headers__(session),
            }

            r = session.post(
                url = 'https://discord.com/api/v10/auth/register', 
                headers = headers, 
                json = payload, 
                proxies = {
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}"
                }
            )
            
            if 'captcha_key' in r.text:
                self.print(f'{self.lerror}{self.red}  Error   {self.purp}|{self.cyan} Invalid captcha')
                return
            
            if 'The resource is being rate limited.' in r.text:
                time_to_wait = int(r.json()['retry_after']) + 1
                self.print(f'{self.lerror}{self.red}  Error   {self.purp}|{self.cyan} ratelimited ' + proxy + " | " + str(time_to_wait) + 's')
                
                if time_to_wait > 15:
                    if captcha_token in self.captcha_tokens:
                        return
                    if captcha_token not in self.captcha_tokens:
                        self.captcha_tokens.append(captcha_token)

                    proxy = random.choice(self.proxies)
                    self.__gen__(captcha_token, proxy)
                    
                time.sleep(time_to_wait)
                r = session.post(
                    url = 'https://discord.com/api/v10/auth/register', 
                    headers = headers, 
                    json = payload, 
                    proxies = {
                        "http": f"http://{proxy}",
                        "https": f"http://{proxy}"
                    }
                )
            
            token = r.json()['token']
            self.captcha_tokens.append(captcha_token)
            with open("./data/tokens.txt", "a") as x: x.write(f'{token}\n')
            with open("./data/accounts.txt", "a") as x: x.write(f'{email}:{self.config["password"]}:{token}\n')
            self.print(f'{self.ljoined}{self.blue} Joined server  {self.purp} {self.cyan} ' + token)

        except Exception as e:
            if captcha_token in self.captcha_tokens:
                return
            else:
                proxy = random.choice(self.proxies)
                self.print(f'{self.lerror}{self.red}  Error   {self.purp}|{self.cyan} retrying with ' + proxy)
                self.captcha_tokens.append(captcha_token)
                self.__gen__(captcha_token, proxy)

    def __captcha__(self):
        while True:
            try:
                proxy = random.choice(self.proxies)
                capmonster = HCaptchaTask(self.config["capmonster_key"])
                task_id = capmonster.create_task("https://discord.com/register", "4c672d35-0701-42b2-88c3-78380b0db560")
                #self.print(f'{self.green}Task    {self.purp}|{self.cyan} ' + str(task_id))
                captcha_token = capmonster.join_task_result(task_id)["gRecaptchaResponse"]
                self.print(f'{self.lcaptcha}{self.green} Captcha Passed!  ' + captcha_token[:15])
                
                self.__gen__(captcha_token, proxy)
            except Exception as e:
                print(e)
                continue

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    Booster().__main__()
    
