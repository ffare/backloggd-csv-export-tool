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
    if not list:
        print('Could not get number of pages. Exiting...')
        exit()
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

with open('debug/result.html', 'w', encoding='utf-8') as file, open('export/export.csv', 'w', newline='', encoding='utf-8') as csvf:
    x = requests.get('https://www.backloggd.com/u/'+username+'/wishlist/')
    file.write(x.text)
    writer = csv.writer(csvf, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['Name', 'Release Date', 'Companies'])  # Write header 
    
    maxpages = getMaxNumberofPages(username, x.text)
    link_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxpages) as executor1:              
        p_results = [executor1.submit(getRequest, 'https://www.backloggd.com/u/'+username+'/wishlist/?page='+str(i+1)) for i in range(maxpages)]       
        
        for future in concurrent.futures.as_completed(p_results):
            x = future.result()
            list = getListFromKeyword(x.text, r'<a href="/games/[^/]+/')
            link_list.extend([w[10:] for w in list])
        
    print(len(link_list))
    t = time.time()
    # Fetch information after accessing links        
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor2:       
        results = [executor2.submit(getRequest, 'https://www.backloggd.com/'+str(w)) for w in link_list]
        print(time.time()-t)
        
        for future in concurrent.futures.as_completed(results):
            y = future.result()
            
            print((getGameName(y.text), getReleaseDate(y.text), getCompanyNames(y.text)))
            print('....')
            writer.writerow((getGameName(y.text), getReleaseDate(y.text), getCompanyNames(y.text)))                    
            print('done\n')

    print('Elapsed time: '+str(time.time()-t))