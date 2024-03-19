import requests
import re

def getListFromKeyword(text, keyword):
    pattern = re.compile(keyword)
    return pattern.findall(text)

with open('result.html', 'w') as file:
    x = requests.get('https://www.backloggd.com/u/Hollow/wishlist/')
    file.write(x.text)

list = getListFromKeyword(x.text, r'href="/u/Hollow/wishlist\?page=.*')

page_list = []
for w in list[0].split():
    currword = re.search('page=.', w)
    if currword:
        page_list.append(currword.group()[-1])
    
    
#print(list)
print(page_list)