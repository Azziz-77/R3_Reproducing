import re
import requests
from bs4 import BeautifulSoup
import functools
import time
from termcolor import colored
import yaml

def retry(max_retries=3, retry_delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"发生异常：{e}")
                    if i < max_retries - 1:
                        print(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                    else:
                        print("所有重试失败")
                        raise
            return wrapper(*args, **kwargs)  # Pass both args and kwargs
        return wrapper
    return decorator

def cat_html(url: str) -> str:
    # Clean the URL before making the request
    url = url.strip()
    # Remove any quotes
    url = re.sub(r'["\']|\[\w+\]', '', url)
    
    # Add http:// if not present
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract text content
        body_content = soup.find('body')
        if body_content:
            text_content = body_content.get_text(separator="\n", strip=True)
        else:
            text_content = "No body content found"
            
        return text_content
    except requests.RequestException as e:
        return f"Error accessing URL: {str(e)}"

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as config_stream:
        return yaml.safe_load(config_stream)

def print_AutoRT():
    ascii_art = """
    _              _             ____    _____ 
   / \     _   _  | |_    ___   |  _ \  |_   _|
  / _ \   | | | | | __|  / _ \  | |_) |   | |  
 / ___ \  | |_| | | |_  | (_) | |  __/    | |  
/_/   \_\  \__,_|  \__|  \___/  |_|       |_|  
    """
    color = 'red'  # Set the color to red
    for line in ascii_art.splitlines():
        print(colored(line, color))
