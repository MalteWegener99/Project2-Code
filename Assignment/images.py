import requests
import random
import urllib.request
import re
import shutil
from random import shuffle

query = "civil aircraft"

r = requests.get("https://api.qwant.com/api/search/images",
    params={
        'count': 250,
        'q': query,
        't': 'images',
        'safesearch': 1,
        'locale': 'en_US',
        'uiv': 4
    },
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
)

response = r.json().get('data').get('result').get('items')
print(response)
urls = [r.get('media') for r in response]

for j in range(0, 50):
    shuffle(urls)

    i = 0
    for url in urls:
        i += 1
        name = "A" + str(i)
        print(i)
        try:
            urllib.request.urlretrieve(url, "pics/" + name+url[-4:])
        except:
            i -= 1
        if i == 120:
            exit()

    shutil.make_archive('pics'+str(j), 'zip')
    print(j)
