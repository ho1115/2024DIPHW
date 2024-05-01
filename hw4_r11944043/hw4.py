from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def FloydDiffu(pixels, error, hori, verti, mask):
    for x in range(2):
        for y in range(-1, 2):
            row = hori + y
            col = verti + x
            if col >= 600: continue
            if row < 0 or row >= 600: continue
            pixels[row, col] = int(pixels[row, col] + error * mask[x, y + 1])

def JarDiffu(pixels, error, hori, verti, mask):
    for x in range(3):
        for y in range(-2, 3):
            row = hori + y
            col = verti + x
            if col >= 600: continue
            if row < 0 or row >= 600: continue
            pixels[row, col] = int(pixels[row, col] + error * mask[x, y + 2])


# problem 1-a --
curImg = Image.open("./SampleImage/sample1.png")
Dmatrix = np.array([[255*(1.5/4), 255*(2.5/4)],[255*(3.5/4), 0]])
pix = curImg.load()
for i in range(0, curImg.size[0], 2):
    for j in range(0, curImg.size[1], 2):
        if (pix[i, j] > Dmatrix[0, 0]) : pix[i, j] = 255
        else : pix[i, j] = 0
        if (pix[i + 1, j] > Dmatrix[0, 1]) : pix[i + 1, j] = 255
        else : pix[i + 1, j] = 0
        if (pix[i, j + 1] > Dmatrix[1, 0]) : pix[i, j + 1] = 255
        else : pix[i, j + 1] = 0
        if (pix[i + 1, j + 1] > Dmatrix[1, 1]) : pix[i + 1, j + 1] = 255
        else : pix[i + 1, j + 1] = 0
curImg.save("result1.png")
# -- problem 1-a --

# problem 1-b --
curImg = Image.open("./SampleImage/sample1.png")
Dmatrix = np.array([[1, 2],[3, 0]])
for i in range(7):
    expSize = 2**(i+1)
    Dmatrix = np.tile(Dmatrix, (2, 2)) * 4
    Dmatrix[:expSize, :expSize] = Dmatrix[:expSize, :expSize] + 1
    Dmatrix[:expSize, expSize:] = Dmatrix[:expSize, expSize:] + 2
    Dmatrix[expSize:, :expSize] = Dmatrix[expSize:, :expSize] + 3
Dmatrix = (Dmatrix + 0.5) * 255 / (256**2)
pix = curImg.load()
for i in range(curImg.size[0]):
    for j in range(curImg.size[1]):
        if (pix[i, j] > Dmatrix[i % 256, j % 256]) : pix[i, j] = 255
        else : pix[i, j] = 0
curImg.save("result2.png")
# -- problem 1-b --

# problem 1-c --
curImg = Image.open("./SampleImage/sample1.png")
jarImg = Image.open("./SampleImage/sample1.png")
FSMask = np.array([[0, 0, 7/16], [3/16, 5/16, 1/16]])
JarMask = np.array([[0, 0, 0, 7/48, 5/48], [3/48, 5/48, 7/48, 5/48, 3/48], [1/48, 3/48, 5/48, 3/48, 1/48]])
FSPix = curImg.load()
JarPix = jarImg.load()
FSError = 0
JarError = 0

for i in range(curImg.size[0]):
    for j in range(curImg.size[1]):
        if (FSPix[i, j] > 127) : 
            FSError = FSPix[i, j] - 255
            FSPix[i, j] = 255
        else : 
            FSError = FSPix[i, j]
            FSPix[i, j] = 0

        if (JarPix[i, j] > 127) : 
            JarError = JarPix[i, j] - 255
            JarPix[i, j] = 255
        else : 
            JarError = JarPix[i, j]
            JarPix[i, j] = 0
        FloydDiffu(FSPix, FSError, i, j, FSMask)
        JarDiffu(JarPix, JarError, i, j, JarMask)

curImg.save("result3.png")
jarImg.save("result4.png")
# -- problem 1-c --