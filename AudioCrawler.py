from urllib.request import Request, urlopen
import re
import requests
from os import mkdir, path
from bs4 import BeautifulSoup
from pathlib import Path

url = input('URL - ')

def getHTML(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(req).read().decode('UTF-8')

def getLinks(html):
    return re.findall('(?:href=")(.*mp3)"', html)

def getAudiobookName(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('figcaption').text

def createDirectory(html):
    directory_path = path.join(Path.home(), 'Music', 'Audiobooks', getAudiobookName(html))
    mkdir(directory_path)
    return directory_path

def downloadFiles(html):
    links = getLinks(html)

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

    # make sure the same directory does not already exist?
    directoryPath = createDirectory(html)

    for i in range(len(links)):
        params = {
            '_': f'{i + 1}',
        }

        print(f'Downloading part {i + 1}/{len(links)}...')

        response = requests.get(
            links[i],
            params=params,
            headers=headers,
        )

        open(path.join(directoryPath, f'part{i + 1}.mp3'), 'wb').write(response.content)
    print('Completed!')

if __name__ == '__main__':
    downloadFiles(getHTML(url))
