import requests
import re

def getListFromKeyword(text, keyword):
    pattern = re.compile(keyword)
    return pattern.findall(text)

with open('result.html', 'w') as file:
    x = requests.get('https://www.backloggd.com/u/Hollow/wishlist/')
    file.write(x.text)

list = getListFromKeyword(x.text, r'<div class="game-text-centered".*')
for w in list:
    w_split = w.split('>')
    print(w_split[1].split('</div')[0].lstrip())
    
    
#print(list)
#print(list)