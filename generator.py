import os
import time
import json
import random
import base64
import threading
import re
import sys
from typing import Optional
import requests
from colorama import Fore, Style, init
import cursor
from advanced_captcha_solver import AdvancedCaptchaSolver
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv

# Initialize colorama
init(autoreset=True)
console = Console()

class DiscordTokenGenerator:
    def __init__(self):
        load_dotenv()
        # No API key needed for AI solver
        self.api_version = 10  # Discord's current API version
        self.base_url = f"https://discord.com/api/v{self.api_version}"
        # Fallback fingerprint in case API fails
        self.fallback_fingerprint = ""  # Will be generated randomly
        # Create realistic browser headers
        browser_version = "121.0.0.0"
        self.headers = {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browser_version} Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/register",
            "Sec-Ch-Ua": '"Google Chrome";v="121", "Not A(Brand";v="99", "Chromium";v="121"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Super-Properties": base64.b64encode(json.dumps({
                "os": "Windows",
                "browser": "Chrome",
                "device": "",
                "browser_user_agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browser_version} Safari/537.36",
                "browser_version": browser_version,
                "os_version": "10",
                "referrer": "https://discord.com/",
                "referring_domain": "discord.com",
                "referrer_current": "https://discord.com/register",
                "referring_domain_current": "discord.com",
                "release_channel": "stable",
                "client_build_number": 245662,
                "client_event_source": None
            }).encode()).decode()
        }
        # Disable SSL warnings
        import urllib3
        urllib3.disable_warnings()
        self.session = requests.Session()
        self.captcha_tokens = []
        self.proxies = self.load_proxies()
        
    def display_banner(self):
        console.print("================ Discord Token Generator ================\n")
        console.print("[cyan]Created by:[/cyan] Dorukuz")
        console.print("[cyan]Version:[/cyan] 2.0 (AI-Powered)\n")
        console.print("[cyan]Links:[/cyan]")
        console.print("- Telegram: https://t.me/Dorukuz")
        console.print("- Github: https://github.com/Dorukuz\n")
        console.print("[yellow]Status:[/yellow] AI Pattern Matcher Ready\n")

    def solve_captcha(self, site_key: str, site_url: str) -> Optional[str]:
        try:
            console.print("[cyan]Using Advanced AI Captcha Solver with multiple methods...[/cyan]")
            solver = AdvancedCaptchaSolver()
            result = solver.solve_captcha(site_key, site_url)
            if result:
                console.print("[green]Advanced AI successfully solved the captcha![/green]")
                return result
            else:
                console.print("[yellow]Advanced AI failed to solve the captcha, retrying...[/yellow]")
                return None
        except Exception as e:
            console.print(f"[red]Error in Advanced AI captcha solver: {str(e)}[/red]")
            return None
        finally:
            # Clean up resources
            if 'solver' in locals() and hasattr(solver, 'close'):
                try:
                    solver.close()
                except:
                    pass

    def fetch_proxies(self) -> list:
        try:
            console.print("[cyan]Fetching fresh proxies...[/cyan]")
            proxies = set()
            
            # Source 1: proxyscrape.com
            try:
                response = self.session.get(
                    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
                    verify=False
                )
                if response.status_code == 200:
                    proxies.update(response.text.strip().split('\n'))
            except Exception as e:
                console.print(f"[yellow]Error fetching from source 1: {str(e)}[/yellow]")

            # Source 2: openproxy.space
            try:
                response = self.session.get(
                    "https://openproxy.space/list/http",
                    verify=False
                )
                if response.status_code == 200:
                    proxies.update([f"{p['ip']}:{p['port']}" for p in response.json()['data']])
            except Exception as e:
                console.print(f"[yellow]Error fetching from source 2: {str(e)}[/yellow]")

            # Source 3: proxy-list.download
            try:
                response = self.session.get(
                    "https://www.proxy-list.download/api/v1/get?type=http",
                    verify=False
                )
                if response.status_code == 200:
                    proxies.update(response.text.strip().split('\n'))
            except Exception as e:
                console.print(f"[yellow]Error fetching from source 3: {str(e)}[/yellow]")

            # Filter and verify proxies
            working_proxies = []
            console.print("[cyan]Testing proxies...[/cyan]")
            
            for proxy in proxies:
                if not proxy.strip():
                    continue
                try:
                    response = self.session.get(
                        "https://www.google.com",
                        proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                        timeout=5,
                        verify=False
                    )
                    if response.status_code == 200:
                        working_proxies.append(proxy)
                        console.print(f"[green]Found working proxy: {proxy}[/green]")
                        if len(working_proxies) >= 10:  # Get at least 10 working proxies
                            break
                except:
                    continue

            if working_proxies:
                console.print(f"[green]Successfully found {len(working_proxies)} working proxies[/green]")
                return working_proxies
            else:
                console.print("[yellow]No working proxies found, running without proxies[/yellow]")
                return []
                
        except Exception as e:
            console.print(f"[red]Error fetching proxies: {str(e)}[/red]")
            return []

    def load_proxies(self) -> list:
        # First try to load from file
        if os.path.exists('proxies.txt'):
            try:
                with open('proxies.txt', 'r') as f:
                    proxies = [line.strip() for line in f if line.strip()]
                if proxies:
                    console.print("[green]Loaded proxies from proxies.txt[/green]")
                    return proxies
            except Exception as e:
                console.print(f"[yellow]Error loading proxies from file: {str(e)}[/yellow]")
        
        # If no file or empty file, fetch from online
        return self.fetch_proxies()
        
    def _get_fingerprint(self, proxy_dict=None):
        """Try to get a fingerprint from Discord API"""
        try:
            # First try with a direct API request
            try:
                response = self.session.get(
                    f"{self.base_url}/experiments",
                    verify=False,
                    proxies=proxy_dict,
                    timeout=15
                )
                if response.status_code == 200 and "fingerprint" in response.text:
                    return response.json()["fingerprint"]
            except Exception as e:
                console.print(f"[yellow]Direct API fingerprint failed: {str(e)}[/yellow]")
            
            # If direct API fails, try to get it from the register page HTML
            try:
                response = self.session.get(
                    "https://discord.com/register",
                    headers={**self.headers, "Content-Type": "text/html"},
                    verify=False,
                    proxies=proxy_dict,
                    timeout=15
                )
                
                if response.status_code == 200:
                    # Try to find the fingerprint in the HTML
                    import re
                    match = re.search(r'"fingerprint":"([^"]+)"', response.text)
                    if match:
                        return match.group(1)
            except Exception as e:
                console.print(f"[yellow]HTML extraction fingerprint failed: {str(e)}[/yellow]")
                
            # Both methods failed
            console.print("[red]Failed to get fingerprint from Discord[/red]")
            return None
            
        except Exception as e:
            console.print(f"[red]Error in fingerprint fetching: {str(e)}[/red]")
            return None
    
    def _generate_fallback_fingerprint(self):
        """Generate a fallback fingerprint if API fails"""
        if not self.fallback_fingerprint:
            # Discord fingerprints are 18 characters of hex
            import uuid
            # Generate a random fingerprint-like string
            self.fallback_fingerprint = uuid.uuid4().hex[:18]
        return self.fallback_fingerprint

    def generate_token(self, proxy: Optional[str] = None) -> Optional[str]:
        try:
            proxy_dict = None
            if proxy:
                proxy_dict = {
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}"
                }

            # First, try to get a fingerprint from Discord API
            fingerprint = self._get_fingerprint(proxy_dict)
            
            # If that fails, use a fallback method
            if not fingerprint:
                fingerprint = self._generate_fallback_fingerprint()
                console.print(f"[yellow]Using fallback fingerprint: {fingerprint}[/yellow]")
            
            # Solve Captcha
            captcha_key = self.solve_captcha(
                "4c672d35-0701-42b2-88c3-78380b0db560",
                "https://discord.com"
            )
            
            if not captcha_key:
                return None

            if captcha_key in self.captcha_tokens:
                console.print("[yellow]Captcha token already used, retrying...[/yellow]")
                return None

            # Generate random username and password
            username = f"User_{random.randint(10000, 99999)}"
            password = f"Password{random.randint(100000, 999999)}"
            
            # Register request
            payload = {
                "username": username,
                "password": password,
                "consent": True,
                "fingerprint": fingerprint,
                "captcha_key": captcha_key
            }
            
            try:
                # Create a session cookie first to appear more natural
                self.session.get(
                    "https://discord.com/register",
                    headers={**self.headers, "Content-Type": "text/html"},
                    verify=False,
                    proxies=proxy_dict
                )
                
                # Make the registration request
                response = self.session.post(
                    f"{self.base_url}/auth/register",
                    headers=self.headers,
                    json=payload,
                    verify=False,
                    proxies=proxy_dict,
                    timeout=20
                )
            except requests.exceptions.ConnectionError:
                console.print("[yellow]Connection reset by Discord. Retrying with delay...[/yellow]")
                time.sleep(10)  # Wait before retry
                
                # Try with a fresh session
                self.session = requests.Session()
                
                try:
                    # Get a new fingerprint
                    fingerprint_response = self.session.get(
                        f"{self.base_url}/experiments",
                        verify=False,
                        proxies=proxy_dict,
                        timeout=15
                    )
                    if fingerprint_response.status_code == 200:
                        payload["fingerprint"] = fingerprint_response.json()["fingerprint"]
                    
                    # Retry the request
                    response = self.session.post(
                        f"{self.base_url}/auth/register",
                        headers=self.headers,
                        json=payload,
                        verify=False,
                        proxies=proxy_dict,
                        timeout=20
                    )
                except Exception as e:
                    console.print(f"[red]Connection failed on retry: {str(e)}[/red]")
                    return None
            
            if response.status_code == 201:
                token = response.json().get("token")
                self.captcha_tokens.append(captcha_key)
                # Save account info
                with open("accounts.txt", "a") as f:
                    f.write(f"{username}:{password}:{token}\n")
                console.print(f"[green]Successfully generated token: {token}")
                return token
            elif 'captcha_key' in response.text:
                console.print("[yellow]Captcha invalid, retrying...[/yellow]")
                return None
            elif 'The resource is being rate limited.' in response.text:
                retry_after = response.json().get('retry_after', 5)
                console.print(f"[yellow]Rate limited, waiting {retry_after} seconds...[/yellow]")
                time.sleep(retry_after)
                return self.generate_token(proxy)
            else:
                console.print(f"[red]Failed to generate token: {response.text}")
                return None
                
        except Exception as e:
            console.print(f"[red]Error generating token: {str(e)}")
            if proxy:
                console.print(f"[yellow]Retrying with different proxy...[/yellow]")
                new_proxy = random.choice(self.proxies) if self.proxies else None
                return self.generate_token(new_proxy)
            return None

    def run(self):
        cursor.hide()
        self.display_banner()
        
        while True:
            console.print("\n[cyan]Options:")
            console.print("[1] Generate Tokens")
            console.print("[2] Exit")
            
            try:
                choice = input("\nEnter your choice: ")
                
                if choice == "1":
                    try:
                        num_tokens = int(input("Enter number of tokens to generate: "))
                        for i in range(num_tokens):
                            # Give the user a chance to cancel
                            console.print(f"\n[cyan]Generating token {i+1}/{num_tokens}... (Press Ctrl+C to cancel)[/cyan]")
                            time.sleep(1)
                            
                            # Try up to 5 times with different approaches
                            max_retries = 5
                            success = False
                            
                            for retry in range(max_retries):
                                if retry > 0:
                                    console.print(f"[yellow]Retry attempt {retry}/{max_retries-1}...[/yellow]")
                                
                                # Get a fresh proxy for each retry
                                proxy = random.choice(self.proxies) if self.proxies and len(self.proxies) > 0 else None
                                if proxy:
                                    console.print(f"[cyan]Using proxy: {proxy}[/cyan]")
                                else:
                                    console.print("[yellow]No proxy available, trying direct connection[/yellow]")
                                
                                # Try with a fresh session for each retry
                                if retry > 0:
                                    self.session = requests.Session()
                                    # Make it look like a new browser visit
                                    self.session.get(
                                        "https://discord.com",
                                        headers={**self.headers, "Content-Type": "text/html"},
                                        verify=False,
                                        timeout=10
                                    )
                                
                                token = self.generate_token(proxy)
                                if token:
                                    with open("tokens.txt", "a") as f:
                                        f.write(f"{token}\n")
                                    success = True
                                    break
                                    
                                # Wait between retries with increasing delay
                                if retry < max_retries - 1:
                                    # Random delay to avoid pattern detection
                                    delay = random.uniform((retry + 1) * 2, (retry + 1) * 3)
                                    console.print(f"[yellow]Waiting {delay:.1f} seconds before next retry...[/yellow]")
                                    time.sleep(delay)
                            
                            if not success:
                                console.print("[red]Failed to generate token after multiple attempts[/red]")
                                console.print("[yellow]Discord may be blocking our requests. Try again later or with different proxies.[/yellow]")
                                
                            # Add random delay between token generations
                            delay = random.uniform(2, 5)
                            console.print(f"[cyan]Waiting {delay:.1f} seconds before next token...[/cyan]")
                            time.sleep(delay)
                    except ValueError:
                        console.print("[red]Please enter a valid number")
                        
                elif choice == "2":
                    console.print("[yellow]Exiting...")
                    break
                    
                else:
                    console.print("[red]Invalid choice!")
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Exiting...")
                break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}")
                break

if __name__ == "__main__":
    generator = DiscordTokenGenerator()
    generator.run()
