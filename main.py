import requests
import re

with open('debug/result.html', 'w') as file:
    x = requests.get('https://www.backloggd.com/u/Hollow/wishlist/')
    file.write(x.text)

link_keyword = '<a href="/games/'
game_name_keyword = '<div class="game-text-centered"'

link_list = []
game_name_list = []

list = re.findall(r'<a href="/games/.*', x.text)
for w in list:
    matches = re.search(r'games/[^/]+/', w)
    if matches:
        link_list.append(matches.group())

    
print(link_list)