import requests
import re
import time

username = 'Hollow'

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

def getReleaseDate(text):
    list = getListFromKeyword(text, r'<div class="col-auto mt-auto pr-0">\n.*')
    return list[0].split('>')[5][:-3]
    
def getGameName(text):
    list = getListFromKeyword(text, r'<div class="col-12 pr-0">\n.*\n.*\n.*')
    return list[0].split('<h1 class="mb-0">')[1][:-5]

def getCompanyNames(text):
    list = getListFromKeyword(text, r'<div class="col-auto pl-lg-1 sub-title">(.*?)</div>', flags=re.DOTALL)
    new_list = re.findall(r'<a href="/company/.*?>(.*?)</a>', list[0], flags=re.DOTALL)
    return new_list

with open('debug/result.html', 'w') as file:
    x = requests.get('https://www.backloggd.com/u/'+username+'/wishlist/')
    file.write(x.text)

link_list = []
gameName_list = []
maxpages = getMaxNumberofPages(username, x.text)
for i in range(maxpages):
    x = requests.get('https://www.backloggd.com/u/'+username+'/wishlist/?page='+str(i+1))
    
    list = getListFromKeyword(x.text, r'<a href="/games/[^/]+/')
    # Fetch information after accessing links
    for w in list:
        w = w[10:]       
        link_list.append(w)
                       
        print('https://www.backloggd.com/games/'+str(w))
        
        s_time = time.time()
        y = requests.get('https://www.backloggd.com/'+str(w))
        print("elapsed time: "+str(time.time() - s_time)[:4])
        
        print(getReleaseDate(y.text))
        print('\n')
        
    list = getListFromKeyword(x.text, r'<div class="game-text-centered".*')
    for w in list:
        w_split = w.split('>')
        gameName_list.append(w_split[1].split('</div')[0].lstrip())

date_list = []
for link in link_list:
    x = requests.get('https://www.backloggd.com/games/'+str(link)+'/')
    if (x.status_code==200):
        date_list.append(getReleaseDate(x.text))
        
print(date_list)