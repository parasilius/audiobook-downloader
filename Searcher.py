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

        response = requests.get(self.address, params=params, headers=headers)
        self.html = response.text

    @abstractmethod
    def getNamesAndLinks(self) -> list[tuple]:
        pass