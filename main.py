import requests

x = requests.get('https://www.backloggd.com/u/Hollow/wishlist/')
print(x.text)