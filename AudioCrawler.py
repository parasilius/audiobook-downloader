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

    i = 1
    while i <= len(links):
        params = {
            '_': f'{i}',
        }

        print(f'Downloading part {i}/{len(links)}...')

        try:
            response = requests.get(
                links[i - 1],
                params=params,
                headers=headers,
            )

            open(path.join(directoryPath, f'part{i}.mp3'), 'wb').write(response.content)
        except:
            i -= 1
            print('Failed. Retrying...')
        i += 1
    print('Completed!')

if __name__ == '__main__':
    downloadFiles(getHTML(url))
