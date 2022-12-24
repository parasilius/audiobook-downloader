from urllib.request import Request, urlopen
import re
import requests
from os import mkdir, path
from bs4 import BeautifulSoup
from utilities import *

def getSearchHTML(term: str) -> str:
    global headers
    headers['authority'] = 'goldenaudiobooks.com'

    params = {
        's': f'{term}',
        # 'id': '28332',
    }

    response = requests.get('https://goldenaudiobooks.com/', params=params, headers=headers)
    return response.text

def getSearchTuplesList(html: str) -> list[tuple]:
    li = re.findall('(?:<div class="image-hover-wrapper">)(\s+.*\s+)', html)
    for i in range(len(li)):
        title = re.findall('(?:title=")(.*)"', li[i])[0]
        if '&#8211;' in title:
            title = title.replace('&#8211;', '-')
        if '&#8217;' in title:
            title = title.replace('&#8217;', '\'')
        link = re.findall('(?:href=")(.*?)"', li[i])[0]
        li[i] = title, link
    return li

def getLinks(html: str) -> list[str]:
    return re.findall('(?:href=")(.*mp3)"', html)

def getAudiobookName(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('figcaption').text

def downloadFiles(html: str) -> None:
    links = getLinks(html)

    global headers
    headers['authority'] = 'ipaudio.club'

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

            with open(path.join(directoryPath, f'part{i}.mp3'), 'wb') as f1:
                f1.write(response.content)
        except:
            i -= 1
            print('Failed. Retrying...')
        i += 1
    print('Completed!')

if __name__ == '__main__':
    withSearch = int(input('Search a term (1) or give a link (2)?[1/2] '))
    if withSearch == 1:
        term = input('Enter the term to search for: ')
        audiobooks = getSearchTuplesList(getSearchHTML(term))
        for i in range(len(audiobooks)):
            print(f'\n[{i + 1}]\nTitle: {audiobooks[i][0]}\n')
        audiobookNumber = int(input('Choose the audiobook number: '))
        downloadFiles(getHTML(audiobooks[audiobookNumber - 1][1]))
    elif withSearch == 2:
        url = input('URL - ')
        downloadFiles(getHTML(url))