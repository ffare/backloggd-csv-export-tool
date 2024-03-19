import requests

with open('debug/result.html', 'w') as file:
    x = requests.get('https://www.backloggd.com/u/Hollow/wishlist/')
    file.write(x.text)

link_list = []
game_name_list = []
link_keyword = '<a href="/games/'
game_name_keyword = '<div class="game-text-centered"'
for line in x.text.splitlines():
    if link_keyword in line:
        link_list.append(line.strip())
        
print(link_list)