import json
import os
import shutil
import img2pdf
from rich.console import Console
from rich.traceback import install

install()
console = Console()


currentDir = os.path.dirname(os.path.abspath(__file__))
pagesDir = os.path.join(currentDir, "..", "pages")

fileNames = []


def formFileNames():
    for file in os.listdir(pagesDir):
        if file.endswith(".jpg"):
            if file == "cover.jpg":
                continue
            fileNames.append(file)
    fileNames.sort(key=lambda x: int(x.split(".")[0]))


formFileNames()


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
            os.rename(os.path.join(pagesDir, file), os.path.join(pagesDir, newName))


def makeHundredsPagesFolder():
    lastFileName = int(fileNames[-1].split(".")[0])

    root = os.path.join(pagesDir, "..", "pages_hundreds")
    os.makedirs(root, exist_ok=True)

    for i in range(0, lastFileName, 100):
        hundredFolderName = str(i)
        hundredFolderPath = os.path.join(root, hundredFolderName)
        os.makedirs(hundredFolderPath, exist_ok=True)

    for file in os.listdir(pagesDir):
        if file == "cover.jpg":
            continue

        hundred = int(file.split(".")[0]) // 100

        hundredFolderName = str(hundred * 100)
        hundredFolderPath = os.path.join(root, hundredFolderName)

        originalFilePath = os.path.join(pagesDir, file)
        destinationFilePath = os.path.join(hundredFolderPath, file)

        shutil.copyfile(originalFilePath, destinationFilePath)
        console.print(f"Copying '{file}' to '{hundredFolderPath}'")


def formPdf():
    outputFilePath = os.path.join(currentDir, "..", "ESV_Study_Bible.pdf")
    fileNames.insert(0, "cover.jpg")

    with open(outputFilePath, "wb") as f:
        allImageFiles = [os.path.join(pagesDir, file) for file in fileNames]
        convertedImages = img2pdf.convert(allImageFiles)
        f.write(convertedImages)
    console.print(f"Finished forming PDF file")


def checkFileAvailability():
    leastPageNumber = int(fileNames[0].split(".")[0])
    mostPageNumber = int(fileNames[-1].split(".")[0])
    missingPages = []

    for i in range(leastPageNumber, mostPageNumber + 1):
        if not os.path.exists(os.path.join(pagesDir, str(i) + ".jpg")):
            console.print(f"[red bold]Page {i} not found[/red bold]")
            missingPages.append(i)

    currentDir = os.path.dirname(os.path.abspath(__file__))
    resultsPath = os.path.join(currentDir, "missing_pages.json")

    with open(resultsPath, "w", encoding="utf-8") as f:
        json.dump(missingPages, f, indent=2)


checkFileAvailability()
