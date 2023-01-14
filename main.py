from Searcher import Searcher
from Audiobook import Audiobook

def main(address: str, SearcherClass: Searcher, AudiobookClass: Audiobook) -> None:
    withSearch = int(input('Search a term (1) or give a link (2)?[1/2] '))
    if withSearch == 1:
        term = input('Enter the term to search for: ')
        searcher = SearcherClass(address, term)
        audiobooks = searcher.getNamesAndLinks()
        for i in range(len(audiobooks)):
            print(f'\n[{i + 1}]\nTitle: {audiobooks[i][0]}\n')
        audiobookNumber = int(input('Choose the audiobook number: '))
        audiobook = AudiobookClass(audiobooks[audiobookNumber - 1][1])
        audiobook.downloadFiles()
    elif withSearch == 2:
        link = input('URL - ')
        audiobook = AudiobookClass(link)
        audiobook.downloadFiles()