from bs4 import BeautifulSoup
from utilities import *
from Searcher import Searcher
from Audiobook import Audiobook
from main import main

class DailyAudiobookSearcher(Searcher):
    def getNamesAndLinks(self) -> list[tuple]:
        soup = BeautifulSoup(self.html, 'html.parser')
        h2list = soup.find_all('h2', attrs={'class': 'entry-title post-title'})
        tuples = []
        for h2 in h2list:
            titleAndAuthor = h2.find('a').text
            link = h2.find('a').get('href')
            tuples.append((titleAndAuthor, link))
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
    main('https://dailyaudiobooks.com', DailyAudiobookSearcher, DailyAudiobook)