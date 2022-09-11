# https://martinheinz.dev/blog/57
from math import log10, sqrt
import pathlib
import glob
import zlib, sys, bz2, os, lzma
import numpy as np

def deflate_compression(filename_in, filename_out, saveFile):
    with open(filename_in, mode="rb") as fin, open(filename_out, mode="wb") as fout:
        data = fin.read()
        compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
        saveFile += ("Deflate Compression\n")
        saveFile += (f"Uncompressed size: {sys.getsizeof(data)}\n")
        saveFile += (f"Compressed size: {sys.getsizeof(compressed_data)}\n")
        #fout.write(compressed_data)
        return saveFile

def burrows_wheeler(filename_in, filename_out, saveFile):
    with open(filename_in, mode="rb") as fin, bz2.open(filename_out, "wb") as fout:
        fout.write(fin.read())
    saveFile += ("Burrows-Wheeler Compression\n")
    saveFile += (f"Uncompressed size: {os.stat(filename_in).st_size}\n")
    saveFile += (f"Compressed size: {os.stat(filename_out).st_size}\n")
    return saveFile

def lzmaAlg(filename_in, filename_out, saveFile):
    lzc = lzma.LZMACompressor()
    with open(filename_in, mode="rb") as fin, open(filename_out, "wb") as fout:
        data = fin.read()
        compressed_chunk = lzc.compress(data)
        fout.write(compressed_chunk)
        fout.write(lzc.flush())
    saveFile += ("LZMA Compression\n")
    saveFile += (f"Uncompressed size: {os.stat(filename_in).st_size}\n")
    saveFile += (f"Compressed size: {os.stat(filename_out).st_size}\n")
    return saveFile

def main():
    #original = cv2.imread("original_image.png")
    #compressed = cv2.imread("compressed_image.png", 1)
    #value = PSNR(original, compressed)
    #print(f"PSNR value is {value} dB")
    print("Poredjenje sa ostalim kompresijama\n\n")
    #deflate_compression(slika, slikaOut)

    with open("rezultati_lossless_kompresije.txt", "w") as f:
        results = ""
        slike = glob.glob("slike/*")
        for index, slika in enumerate(slike):
            ekstenzija = pathlib.Path(slika).suffix
            results += ("___SLIKA: " + slika + "\n")
            results = deflate_compression(slika, "slike/kompresovan" + str(index) + ekstenzija, results)
            results += "\n\n"
            results = burrows_wheeler(slika, "slike/kompresovan" + str(index + 100) + ekstenzija, results)
            results += "\n\n"
            results = lzmaAlg(slika, "slike/kompresovan" + str(index + 200) + ekstenzija, results)
            results += "\n\n"

        f.write(results)
        for filename in glob.glob("slike/kompresovan*"):
            os.remove(filename)
        print("Zavrsena kompresija")
main()