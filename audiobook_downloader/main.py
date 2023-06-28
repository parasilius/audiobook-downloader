import da_downloader
import ga_downloader

def downloadFromAllSources():
    term = input('Enter the term to search for: ')
    audiobooks = []
    try:
        gaSearcher = ga_downloader.GoldenAudiobookSearcher('https://goldenaudiobooks.com', term)
        audiobooks += gaSearcher.getNamesAndAudiobooks()
    except:
        print('Cannot connect to GoldenAudiobooks')
    try:
        daSearcher = da_downloader.DailyAudiobookSearcher('https://dailyaudiobooks.com', term)
        audiobooks += daSearcher.getNamesAndAudiobooks()
    except:
        print('Cannot connect to DailyAudiobooks')
    if len(audiobooks) < 1:
        print('No respond from any of the sites!')
        return 1
    for i in range(len(audiobooks)):
        print(f'\n[{i + 1}]\nTitle: {audiobooks[i][0]}\nSource: {audiobooks[i][1].getSource()}\n')
    audiobookNumber = int(input('Choose the audiobook number: '))
    audiobooks[audiobookNumber - 1][1].downloadFiles()

if __name__ == '__main__':
    downloadFromAllSources()