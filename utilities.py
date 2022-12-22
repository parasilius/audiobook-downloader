from urllib.request import Request, urlopen
from pathlib import Path
from os import mkdir, path

def getHTML(url: str) -> str:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(req).read().decode('UTF-8')

def createDirectory(name: str) -> str:
    directory_path = path.join(Path.home(), 'Music', 'Audiobooks', name)
    mkdir(directory_path)
    return directory_path