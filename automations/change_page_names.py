import os
from rich.console import Console
from rich.traceback import install

install()
console = Console()


currentDir = os.path.dirname(os.path.abspath(__file__))
pagesDir = os.path.join(currentDir, "..", "pages")


def cleanName(name):
    number = name.split("_")[-1]
    return number


def renameAllPages():
    for file in os.listdir(pagesDir):
        if file.endswith(".jpg"):
            number = cleanName(file)
            console.print(f"Renaming '{file}' to '{number}'")
            os.rename(os.path.join(pagesDir, file), os.path.join(pagesDir, f"{number}"))


def decrementPages():
    for file in os.listdir(pagesDir):
        if file.endswith(".jpg"):
            if file == "0001.jpg":
                newName = "cover.jpg"
            else:
                number = file.split(".")[0]
                newName = f"{int(number)-10}.jpg"
            console.print(f"Renaming '{file}' to '{newName}'")
            # os.rename(os.path.join(pagesDir, file), os.path.join(pagesDir, newName))


decrementPages()
