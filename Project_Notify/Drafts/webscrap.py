import requests
from bs4 import BeautifulSoup

url = "https://www.instagram.com/p/C4-2zu9Rguh/?utm_source=ig_web_copy_link"

response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content,"html.parser")

post_text = soup.find("div",class_="C4VMK").span.get_text()

print(post_text)