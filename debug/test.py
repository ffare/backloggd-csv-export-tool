import requests
import re

def getListFromKeyword(text, keyword, flags=0):
    return re.findall(keyword, text, flags)

def getCompanyNames(text):
    list = getListFromKeyword(text, r'<div class="col-auto pl-lg-1 sub-title">(.*?)</div>', flags=re.DOTALL)
    new_list = re.findall(r'<a href="/company/.*?>(.*?)</a>', list[0], flags=re.DOTALL)
    return new_list

with open('result.html', 'w', encoding='utf-8') as file:
    x = requests.get('https://www.backloggd.com/games/heroes-of-might-and-magic-ii-gold/')
    if (x.status_code == 200):
        file.write(x.text)
        
print(getCompanyNames(x.text))  


#print(list)
#print(list)