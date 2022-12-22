import requests
from bs4 import BeautifulSoup
from os import mkdir, path
from utilities import *

def getLinks(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    li = soup.find_all('audio')
    for i in range(len(li)):
        li[i] = li[i].contents[-1].text
    return li

def getAudiobookName(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('h1', class_='entry-title post-title').contents[0]

def downloadFiles(html: str) -> None:
    links = getLinks(html)

    headers = {
        'authority': 'ipaudio.club',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'range': 'bytes=0-',
        'referer': 'https://dailyaudiobooks.com/',
        'sec-fetch-dest': 'audio',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    # make sure the same directory does not already exist?
    directoryPath = createDirectory(getAudiobookName(html))

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
    withSearch = int(input('Search a term (1) or give a link (2)?[1/2] '))
    if withSearch == 1:
        pass
    elif withSearch == 2:
        url = input('URL - ')
        downloadFiles(getHTML(url))