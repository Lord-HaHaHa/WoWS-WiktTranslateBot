from cgitb import text
import re
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from TextareaTags import tags

shipname = "Austin"

URL = "https://wiki.wargaming.net/en/index.php?title=Ship:" + shipname + "&action=edit"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
performace = soup.find_all(id="wpTextbox1")
print(performace)