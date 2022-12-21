from urllib.request import Request, urlopen
import re
import requests
from os import mkdir, path
from bs4 import BeautifulSoup
from pathlib import Path

def getSearchHTML(term):
    headers = {
        'authority': 'goldenaudiobooks.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'referer': 'https://goldenaudiobooks.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }

    params = {
        's': f'{term}',
        # 'id': '28332',
    }

    response = requests.get('https://goldenaudiobooks.com/', params=params, headers=headers)
    return response.text

def getSearchTuplesList(html):
    li = re.findall('(?:<div class="image-hover-wrapper">)(\s+.*\s+)', html)
    for i in range(len(li)):
        li[i] = re.findall('(?:title=")(.*)\s&.*;\s(.*)"', li[i])[0][0], re.findall('(?:title=")(.*)\s&.*;\s(.*)"', li[i])[0][1], re.findall('(?:href=")(.*?)"', li[i])[0]
    return li

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
    withSearch = int(input('Search a term (1) or give a link (2)?[1/2] '))
    if withSearch == 1:
        term = input('Enter the term to search for: ')
        audiobooks = getSearchTuplesList(getSearchHTML(term))
        for i in range(len(audiobooks)):
            print(f'\n[{i + 1}]\nTitle: {audiobooks[i][1]}\nAuthor: {audiobooks[i][0]}\n')
        audiobookNumber = int(input('Choose the audiobook number: '))
        downloadFiles(getHTML(audiobooks[audiobookNumber - 1][2]))
    elif withSearch == 2:
        url = input('URL - ')
        downloadFiles(getHTML(url))