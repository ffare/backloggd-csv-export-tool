import requests
import re
import time
import csv
import concurrent.futures

username = 'Hollow'

def getListFromKeyword(text, keyword, flags=0):
    return re.findall(keyword, text, flags)

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

def getCompanyNames(text):    
    list = getListFromKeyword(text, r'<div class="col-auto pl-lg-1 sub-title">(.*?)</div>', flags=re.DOTALL)
    if not list:
        return 'TDB'
    else:
        final_list = re.findall(r'<a href="/company/.*?>(.*?)</a>', list[0], flags=re.DOTALL)
        return ', '.join(final_list)

def getGameName(text):
    list = getListFromKeyword(text, r'<div class="col-auto pr-1">(.*?)</div>', flags=re.DOTALL)
    if not list:
        return 'TDB'
    else:
        return re.findall(r'<h1 class="mb-0">(.*?)</h1>', list[0], flags=re.DOTALL)[0]

def getRequest(text):
    return requests.get(text, timeout=5)

with open('debug/result.html', 'w', encoding='utf-8') as file, open('export/export.csv', 'w', newline='') as csvf:
    x = requests.get('https://www.backloggd.com/u/'+username+'/wishlist/')
    file.write(x.text)
    writer = csv.writer(csvf, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['Name', 'Release Date', 'Companies'])  # Write header 
    
    link_list = []
    maxpages = getMaxNumberofPages(username, x.text)
    for i in range(maxpages):
        x = requests.get('https://www.backloggd.com/u/'+username+'/wishlist/?page='+str(i+1))
        
        list = getListFromKeyword(x.text, r'<a href="/games/[^/]+/')
        list = [w[10:] for w in list]
        
        # Fetch information after accessing links        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(list)) as executor:
            results = [executor.submit(getRequest, 'https://www.backloggd.com/'+str(w)) for w in list]
        
            for future in concurrent.futures.as_completed(results):
                y = future.result()
                    
                writer.writerow((getGameName(y.text), getReleaseDate(y.text), getCompanyNames(y.text)))
                print((getGameName(y.text), getReleaseDate(y.text), getCompanyNames(y.text)))
                print('\n')