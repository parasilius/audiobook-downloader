from urllib.request import Request, urlopen
from pathlib import Path
from os import mkdir, path

headers = {
    'authority': 'dailyaudiobooks.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

def getHTML(url: str) -> str:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(req).read().decode('UTF-8')

def createDirectory(name: str) -> str:
    directory_path = path.join(Path.home(), 'Music', 'Audiobooks', name)
    mkdir(directory_path)
    return directory_path

def downloadFromSingleSource(address: str, SearcherClass, AudiobookClass) -> None:
    withSearch = int(input('Search a term (1) or give a link (2)?[1/2] '))
    if withSearch == 1:
        term = input('Enter the term to search for: ')
        searcher = SearcherClass(address, term)
        audiobooks = searcher.getNamesAndAudiobooks()
        for i in range(len(audiobooks)):
            print(f'\n[{i + 1}]\nTitle: {audiobooks[i][0]}\n')
        audiobookNumber = int(input('Choose the audiobook number: '))
        audiobooks[audiobookNumber - 1][1].downloadFiles()
    elif withSearch == 2:
        link = input('URL - ')
        audiobook = AudiobookClass(link)
        audiobook.downloadFiles()