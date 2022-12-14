from urllib.request import Request, urlopen
import re
import requests

url = 'https://goldenaudiobooks.com/ward-farnsworth-the-practicing-stoic-audiobook/'

def getHTML(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(req).read().decode('UTF-8')

def getLinks(html):
    return re.findall('(?:href=")(.*mp3)"', html)

def downloadFiles(links):
    headers = {
        'authority': 'ipaudio.club',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.6',
        'range': 'bytes=0-',
        'referer': 'https://goldenaudiobooks.com/',
        'sec-fetch-dest': 'audio',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    for i in range(len(links)):
        params = {
            '_': f'{i + 1}',
        }

        response = requests.get(
            links[i],
            params=params,
            headers=headers,
        )

        open(f'part{i + 1}.mp3', 'wb').write(response.content)

if __name__ == '__main__':
    downloadFiles(getLinks(getHTML(url)))