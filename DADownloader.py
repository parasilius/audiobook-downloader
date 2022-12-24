import requests
from bs4 import BeautifulSoup
from os import mkdir, path
from utilities import *

def getSearchHTML(term: str) -> str:
    global headers
    headers['authority'] = 'dailyaudiobooks.com'

    params = {
        's': f'{term}',
    }

    response = requests.get('https://dailyaudiobooks.com/', params=params, headers=headers)
    return response.text

def getSearchTuplesList(html: str) -> list[tuple]:
    soup = BeautifulSoup(html, 'html.parser')
    h2list = soup.find_all('h2', attrs={'class': 'entry-title post-title'})
    tuples = []
    for h2 in h2list:
        titleAndAuthor = h2.find('a').text
        link = h2.find('a').get('href')
        tuples.append((titleAndAuthor.split(' – ')[0], titleAndAuthor.split(' – ')[1], link))
    return tuples

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
            print(f'\n[{i + 1}]\nTitle: {audiobooks[i][1]}\nAuthor: {audiobooks[i][0]}')
        audiobookNumber = int(input('Choose the audiobook number: '))
        downloadFiles(getHTML(audiobooks[audiobookNumber - 1][2]))
    elif withSearch == 2:
        url = input('URL - ')
        downloadFiles(getHTML(url))