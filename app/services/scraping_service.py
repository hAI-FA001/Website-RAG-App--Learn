import requests
from bs4 import BeautifulSoup

def scrape(url):
    res = requests.get(url)
    
    soup = BeautifulSoup(res.content, 'html.parser')
    txt = soup.get_text(separator='\n')
    
    return txt