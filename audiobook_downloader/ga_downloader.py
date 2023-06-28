import re
from bs4 import BeautifulSoup
from audiobook_downloader.utilities import *
from audiobook_downloader.searcher import Searcher
from audiobook_downloader.audiobook import Audiobook

class GoldenAudiobookSearcher(Searcher):
    def getNamesAndAudiobooks(self) -> list[tuple]:
        li = re.findall('(?:<div class="image-hover-wrapper">)(\s+.*\s+)', self.html)
        for i in range(len(li)):
            title = re.findall('(?:title=")(.*)"', li[i])[0]
            if '&#8211;' in title:
                title = title.replace('&#8211;', '-')
            if '&#8217;' in title:
                title = title.replace('&#8217;', '\'')
            link = re.findall('(?:href=")(.*?)"', li[i])[0]
            li[i] = title, GoldenAudioBook(link)
        return li

class GoldenAudioBook(Audiobook):
    def getAudioLinks(self) -> list[str]:
        return re.findall('(?:href=")(.*mp3)"', getHTML(self.link))

    def getName(self) -> str:
        soup = BeautifulSoup(getHTML(self.link), 'html.parser')
        return soup.find('figcaption').text

if __name__ == '__main__':
    downloadFromSingleSource('https://goldenaudiobooks.com', GoldenAudiobookSearcher, GoldenAudioBook)