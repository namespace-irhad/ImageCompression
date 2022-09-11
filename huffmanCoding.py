# https://www.studytonight.com/data-structures/huffman-coding - Objasnjenje kroz korake
import re
import os
import numpy as np  # Manipulacija nizova
from PIL import Image  # Otvaranje, manipulacija slika

class Cvor(object):
    def __init__(self, ld=None, dd=None):
        self.ld = ld
        self.dd = dd

    def vratiDijecu(self):
        return (self.ld, self.dd)

def createTree(lista):
    while len(lista) > 1:
        [f1, kod1] = lista[-1]
        [f2, kod2] = lista[-2]
        lista = lista[:-2]
        cvor = Cvor(kod1, kod2)
        lista.append([f1 + f2, cvor])
        lista = sorted(lista, key=lambda x: x[0],
                       reverse=True)  # https://stackoverflow.com/questions/36955553/sorting-list-of-lists-by-the-first-element-of-each-sub-list
    return lista

def getOptimalCodes(cvor, ld=True, kodVrijednost=''):
    if type(cvor) is not Cvor:
        return {cvor: kodVrijednost}
    (ld, dd) = cvor.vratiDijecu()
    d = dict()
    d.update(getOptimalCodes(ld, True, kodVrijednost + '0'))
    d.update(getOptimalCodes(dd, False, kodVrijednost + '1'))
    return d

def HuffmanCoding(imgName, ext, decode=False, printHuff=False):
    print(imgName + ext)
    try:
        imageData = np.asarray(Image.open(imgName + ext), np.uint8)
    except:
        print("Slika se ne moze ucitati... Program nastavlja")
        return
    shape = imageData.shape
    a = imageData
    imageData = str(imageData.tolist()).replace(" ", "")
    # Pretraga frekvencije liste slike
    symbols = []
    for symbol in imageData:
        if symbol not in [i[0] for i in symbols]:
            frequency = imageData.count(symbol)  # histogram slike - frekvencija
            symbols.append((symbol, frequency))

    nodes = []
    for symbol in symbols:
        nodes.append([symbol[1], symbol[0]])  # sortiranje frekvencije
    nodes.sort()

    nodes = createTree(nodes)
    huffmanCode = getOptimalCodes(nodes[0][1])  # preuzimanje korijena
    constructedCodes = list(map(list, huffmanCode.items()))
    constructedCodes = sorted(constructedCodes, key=lambda x: len(x[1]))

    if printHuff:
        print("Huffmanovo stablo:")
        for symbol in constructedCodes:
            print(symbol[0], str(symbol[1]))

    codewords = ""
    for character in imageData:
        for item in constructedCodes:
            if character in item:
                codewords = codewords + str(item[1])[1:]
    binary = "0b" + codewords

    with open("rezultati_huffman_kompresije_2.txt", "a") as f:
        results = ""
        results += "Slika: " + str(imgName + ext) + "\n"
        uncompressedSize = os.path.getsize(imgName + ext)
        compressedSize = round((len(binary) - 2) / 8)
        results += "Originalna velicina: " + str(uncompressedSize) + " bajt. Kompresovana velicina: " + str(
            compressedSize) + " bajt. "
        results += "CR: " + str(uncompressedSize / compressedSize) + " %\n\n"
        f.write(results)
        f.close()
    print("Zavrseno:", imgName + ext)

    # Dekodiranje
    if decode:
        output = open("Compressed_" + imgName.split("/")[1] + ".txt", "w+")
        output.write(codewords)

        codewords = str(binary[2:])
        uncompressedImage = ""
        code = ""
        for digit in codewords:
            code = code + digit
            pos = 0
            for symbol in constructedCodes:
                if code == symbol[1]:
                    uncompressedImage = uncompressedImage + constructedCodes[pos][0]
                    code = ""
                pos += 1

        # Dekodiranje slike
        imageFileStringArray = re.findall(r'\d+', uncompressedImage)
        # https://stackoverflow.com/questions/10145347/convert-string-to-integer-using-map
        res = list(map(int, imageFileStringArray))
        res = np.array(res)
        res = np.reshape(res.astype(np.uint8), shape)
        # https://www.geeksforgeeks.org/convert-a-numpy-array-to-an-image/
        Image.fromarray(res).save("Compressed_" + imgName.split("/")[1] + ext)  # show za prikaz


def main():
    for file in os.listdir("slike"):
        formats = ('.png', '.jpg', '.tif', '.tiff')
        ext = os.path.splitext(file)[1].lower()
        imgName = os.path.splitext(file)[0]
        if ext in formats:
            # print('___SLIKA:  ' + imgName + ext + "\n")
            HuffmanCoding('slike/' + imgName, ext, decode=False, printHuff=False)
    print("Zavrsena kompresija")


# NEW slike - https://sipi.usc.edu/database/database.php?volume=misc
# OLD slike - standardne image processing slike (MATLAB)
main()
