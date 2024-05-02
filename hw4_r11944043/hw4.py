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

def grayScale(pixels, s0, s1, num):
    white = 255
    black = 0
    if num == 3 :
        white = 0
        black = 255
    empty = np.zeros((s1, s0), dtype = np.uint8)
    for i in range(s0):
        for j in range(s1):
            gray = int(pixels[i, j][0]*0.299 + pixels[i, j][1]*0.587 + pixels[i, j][2]*0.114)
            if gray > 127: gray = white
            else: gray = black
            empty[j, i] = gray
    return empty

def holeFill(s_x, s_y, imgArr):
    imgArr[s_x, s_y] = 255
    x_size = imgArr.shape[0]
    y_size = imgArr.shape[1]
    queue = [(s_x, s_y)]
    while (len(queue) > 0):
        center = queue.pop(0)
        x_coor = center[0]
        y_coor = center[1]
        if (y_coor > 0 and imgArr[x_coor, y_coor - 1] == 0) : 
            imgArr[x_coor, y_coor - 1] = 255
            queue.append((x_coor, y_coor - 1))
        if (x_coor > 0 and imgArr[x_coor - 1, y_coor] == 0) : 
            imgArr[x_coor - 1, y_coor] = 255
            queue.append((x_coor - 1, y_coor))
        if (y_coor < y_size - 1 and imgArr[x_coor, y_coor + 1] == 0) : 
            imgArr[x_coor, y_coor + 1] = 255
            queue.append((x_coor, y_coor + 1))
        if (x_coor < x_size - 1 and imgArr[x_coor + 1, y_coor] == 0) : 
            imgArr[x_coor + 1, y_coor] = 255
            queue.append((x_coor + 1, y_coor))
    return imgArr

def drawLetter(s_x, s_y, imgArr):
    empty =  np.zeros((100, 100), dtype = np.uint8)
    x_size = imgArr.shape[0]
    y_size = imgArr.shape[1]
    queue = [(s_x, s_y)]
    while (len(queue) > 0):
        center = queue.pop(0)
        x_coor = center[0]
        y_coor = center[1]
        empty[20 + x_coor - s_x, 20 + y_coor - s_y] = 0
        if (y_coor > 0 and imgArr[x_coor, y_coor - 1] == 0) : 
            imgArr[x_coor, y_coor - 1] = 255
            queue.append((x_coor, y_coor - 1))
        if (x_coor > 0 and imgArr[x_coor - 1, y_coor] == 0) : 
            imgArr[x_coor - 1, y_coor] = 255
            queue.append((x_coor - 1, y_coor))
        if (y_coor < y_size - 1 and imgArr[x_coor, y_coor + 1] == 0) : 
            imgArr[x_coor, y_coor + 1] = 255
            queue.append((x_coor, y_coor + 1))
        if (x_coor < x_size - 1 and imgArr[x_coor + 1, y_coor] == 0) : 
            imgArr[x_coor + 1, y_coor] = 255
            queue.append((x_coor + 1, y_coor))
    return empty

# problem 1-a --
# curImg = Image.open("./SampleImage/sample1.png")
# Dmatrix = np.array([[255*(1.5/4), 255*(2.5/4)],[255*(3.5/4), 0]])
# pix = curImg.load()
# for i in range(0, curImg.size[0], 2):
#     for j in range(0, curImg.size[1], 2):
#         if (pix[i, j] > Dmatrix[0, 0]) : pix[i, j] = 255
#         else : pix[i, j] = 0
#         if (pix[i + 1, j] > Dmatrix[0, 1]) : pix[i + 1, j] = 255
#         else : pix[i + 1, j] = 0
#         if (pix[i, j + 1] > Dmatrix[1, 0]) : pix[i, j + 1] = 255
#         else : pix[i, j + 1] = 0
#         if (pix[i + 1, j + 1] > Dmatrix[1, 1]) : pix[i + 1, j + 1] = 255
#         else : pix[i + 1, j + 1] = 0
# curImg.save("result1.png")
# -- problem 1-a --

# problem 1-b --
# curImg = Image.open("./SampleImage/sample1.png")
# Dmatrix = np.array([[1, 2],[3, 0]])
# for i in range(7):
#     expSize = 2**(i+1)
#     Dmatrix = np.tile(Dmatrix, (2, 2)) * 4
#     Dmatrix[:expSize, :expSize] = Dmatrix[:expSize, :expSize] + 1
#     Dmatrix[:expSize, expSize:] = Dmatrix[:expSize, expSize:] + 2
#     Dmatrix[expSize:, :expSize] = Dmatrix[expSize:, :expSize] + 3
# Dmatrix = (Dmatrix + 0.5) * 255 / (256**2)
# pix = curImg.load()
# for i in range(curImg.size[0]):
#     for j in range(curImg.size[1]):
#         if (pix[i, j] > Dmatrix[i % 256, j % 256]) : pix[i, j] = 255
#         else : pix[i, j] = 0
# curImg.save("result2.png")
# -- problem 1-b --

# problem 1-c --
# curImg = Image.open("./SampleImage/sample1.png")
# jarImg = Image.open("./SampleImage/sample1.png")
# FSMask = np.array([[0, 0, 7/16], [3/16, 5/16, 1/16]])
# JarMask = np.array([[0, 0, 0, 7/48, 5/48], [3/48, 5/48, 7/48, 5/48, 3/48], [1/48, 3/48, 5/48, 3/48, 1/48]])
# FSPix = curImg.load()
# JarPix = jarImg.load()
# FSError = 0
# JarError = 0

# for i in range(curImg.size[0]):
#     for j in range(curImg.size[1]):
#         if (FSPix[i, j] > 127) : 
#             FSError = FSPix[i, j] - 255
#             FSPix[i, j] = 255
#         else : 
#             FSError = FSPix[i, j]
#             FSPix[i, j] = 0

#         if (JarPix[i, j] > 127) : 
#             JarError = JarPix[i, j] - 255
#             JarPix[i, j] = 255
#         else : 
#             JarError = JarPix[i, j]
#             JarPix[i, j] = 0
#         FloydDiffu(FSPix, FSError, i, j, FSMask)
#         JarDiffu(JarPix, JarError, i, j, JarMask)

# curImg.save("result3.png")
# jarImg.save("result4.png")
# -- problem 1-c --

# -- problem 2 --

# for i in range(2, 5):
#     curImg = Image.open(f"./SampleImage/sample{i}.png")
#     pix = curImg.load()
#     binaryPlate = grayScale(pix, curImg.size[0], curImg.size[1], i)
#     for y in range(binaryPlate.shape[0]):
#         if binaryPlate[y, 0] == 0:
#             binaryPlate = holeFill(y, 0, binaryPlate)
#             break
#     Image.fromarray(binaryPlate).save(f"BW{i}.png")
curImg = Image.open(f"./SampleImage/TrainingSet.png")
imArr = np.array(curImg)[:, :, 0]
# horizonAxis = [50, 130, 240, 320, 430, 510]
# for i in range(curImg.size[0]):
#     for j in range(curImg.size[1]):
#         if j in horizonAxis : imArr[j, i] = 0
#         elif j >=50 and j <= 130 and (i-20) % 100 == 0: imArr[j, i] = 0
#         elif j >=240 and j <= 320 and (i-20) % 106 == 0: imArr[j, i] = 0
#         elif j >=430 and j <= 510 and (i-20) % 96 == 0: imArr[j, i] = 0

bigA = imArr[50:130, 20 : 100]

# curImg = Image.fromarray(imArr)
# curImg.save("slicePic.png")
# -- problem 2 --