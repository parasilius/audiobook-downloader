from abc import ABC, abstractmethod
from utilities import *
import requests

class Searcher(ABC):
    def __init__(self, address: str, term: str) -> None:
        self.headers = headers
        self.address = address

        headers['authority'] = self.address[8:]

        params = {
            's': f'{term}',
        }

        try:
            response = requests.get(self.address, params=params, headers=headers)
            print(response)
            self.html = response.text
            print(self.html)
        except Exception as err:
            print(err)

    @abstractmethod
    def getNamesAndAudiobooks(self) -> list[tuple]:
        pass