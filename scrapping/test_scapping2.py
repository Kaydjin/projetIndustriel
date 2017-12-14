import requests
res = requests.get('https://www.facebook.com/public/Mike-Lecourt')
res.raise_for_status()
playFile = open('test.txt', 'wb')

for chunk in res.iter_content(100000):
    playFile.write(chunk)

playFile.close()