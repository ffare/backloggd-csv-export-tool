import requests
import re

def getListFromKeyword(text, keyword):
    pattern = re.compile(keyword)
    return pattern.findall(text)

with open('debug/result.html', 'w') as file:
    x = requests.get('https://www.backloggd.com/u/Hollow/wishlist/')
    file.write(x.text)

list = getListFromKeyword(x.text, r'<a href="/games/[^/]+/')
#game_name_keyword = '<div class="game-text-centered"'

link_list = []
#game_name_list = []
for w in list:
    link_list.append(w[len('<a href=/"'):])
    
print(link_list)