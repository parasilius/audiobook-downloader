from bs4 import BeautifulSoup
from audiobook_downloader.utilities import *
from audiobook_downloader.searcher import Searcher
from audiobook_downloader.audiobook import Audiobook

class DailyAudiobookSearcher(Searcher):
    def getNamesAndAudiobooks(self) -> list[tuple]:
        soup = BeautifulSoup(self.html, 'html.parser')
        h2list = soup.find_all('h2', attrs={'class': 'entry-title post-title'})
        tuples = []
        for h2 in h2list:
            titleAndAuthor = h2.find('a').text
            link = h2.find('a').get('href')
            tuples.append((titleAndAuthor, DailyAudiobook(link)))
        return tuples

class DailyAudiobook(Audiobook):
    def getAudioLinks(self) -> list[str]:
        soup = BeautifulSoup(getHTML(self.link), 'html.parser')
        li = soup.find_all('audio')
        for i in range(len(li)):
            li[i] = li[i].contents[-1].text
        return li

    def getName(self) -> str:
        soup = BeautifulSoup(getHTML(self.link), 'html.parser')
        return soup.find('h1', class_='entry-title post-title').contents[0]

if __name__ == '__main__':
    downloadFromSingleSource('https://dailyaudiobooks.com', DailyAudiobookSearcher, DailyAudiobook)