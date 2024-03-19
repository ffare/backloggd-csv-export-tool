import requests
import re

username = 'NOWITSREYNTIME17'

def getListFromKeyword(text, keyword):
    pattern = re.compile(keyword)
    return pattern.findall(text)

# Parse through and find the maximum number of pages
def getMaxNumberofPages(user, text):
    list = getListFromKeyword(text, r'href="/u/'+user+r'/wishlist\?page=.*')
    page_list = []
    for w in list[0].split():
        currword = re.search('page=.', w)
        if currword:
            page_list.append(currword.group()[-1])
    
    return int(max(page_list, key=int))

with open('debug/result.html', 'w') as file:
    x = requests.get('https://www.backloggd.com/u/'+username+'/wishlist/')
    file.write(x.text)

link_list = []
maxpages = getMaxNumberofPages(username, x.text)
for i in range(maxpages):
    x = requests.get('https://www.backloggd.com/u/'+username+'/wishlist/?page='+str(i+1))
    
    list = getListFromKeyword(x.text, r'<a href="/games/[^/]+/')
    #game_name_keyword = '<div class="game-text-centered"'
   
    #game_name_list = []
    for w in list:
        link_list.append(w[len('<a href=/"'):])
    
print(link_list)
print('\nTotal numer of games: '+str(len(link_list)))