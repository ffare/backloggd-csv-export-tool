import requests
import re
import csv
import threading
import concurrent.futures
import time

def getListFromKeyword(text, keyword, flags=0):
    return re.findall(keyword, text, flags)

def getGameName(text):
    list = getListFromKeyword(text, r'<div class="col-auto pr-1">(.*?)</div>', flags=re.DOTALL)
    new_list = re.findall(r'<h1 class="mb-0">(.*?)</h1>', list[0], flags=re.DOTALL)
    return new_list[0]

def printtest():
    t = time.time()
    print("working")
    print(time.time() - t)
    
pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
while True:
    pool.submit(printtest())


#print(list)
#print(list)