from abc import ABC, abstractmethod
from utilities import *
import requests
from os import path
import re

class Audiobook(ABC):
    def __init__(self, link: str):
        self.link = link
        self.headers = headers

    def downloadFiles(self) -> None:
        self.headers['authority'] = 'ipaudio.club'

        # make sure the same directory does not already exist?
        directoryPath = createDirectory(self.getName())

        links = self.getAudioLinks()
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
                    headers=self.headers,
                )

                with open(path.join(directoryPath, f'part{i}.mp3'), 'wb') as f1:
                    f1.write(response.content)
            except Exception as err:
                print(err)
                i -= 1
                print('Failed. Retrying...')
            i += 1
        print('Completed!')

    def getSource(self) -> str:
        return self.link

    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def getAudioLinks(self) -> list[str]:
        pass