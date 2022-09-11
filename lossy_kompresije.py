# Mala modifikacija na https://www.geeksforgeeks.org/how-to-compress-images-using-python-and-pil/
import os
import glob
from PIL import Image

def lossyKompresija(file, results):
    filepath = os.path.join("slike/", file)
    picture = Image.open(filepath)
    results += "Uncompressed size: " + str(os.path.getsize(filepath)) + "\n"
    # picture.convert(mode="RGB", palette=Image.ADAPTIVE, colors=256) compression_level za .PNG slike
    file = os.path.splitext(file)[0] + '.jpg'
    picture_jpg = picture.convert('RGB')
    picture_jpg.save("slike/compressed/Compressed_" + file, quality=30)
    results += "Compressed size: " + str(os.path.getsize("slike/compressed/Compressed_" + file)) + "\n"
    results += "Compression ratio: " + str(os.path.getsize(filepath) / (os.path.getsize("slike/compressed/Compressed_" + file))) + "\n\n"
    return results


def main():
    with open("rezultati_lossy_kompresije.txt", "w") as f:
        results = ""
        formats = ('.png', '.jpg') # png slike pretvaramo u jpg, tif slike preskacemo
        for file in os.listdir("slike"):
            if os.path.splitext(file)[1].lower() in formats:
                results += '___SLIKA:  ' + file + "\n"
                results = lossyKompresija(file, results)

        f.write(results)
        print("Zavrsena kompresija")
    for filename in glob.glob("slike/compressed/Compressed_*"): # zakomentarisati da slike ostanu u datoteci
        os.remove(filename)

main()
