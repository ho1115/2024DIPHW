from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def globEqu(pixels, s0, s1):
    cumuTable = [0] * 256

    for i in range(s0):
        for j in range(s1):
            cumuTable[pixels[i, j]] += 1

    for i in range(1, 256) :
        cumuTable[i] += cumuTable[i-1]

    for i in range(s0):
        for j in range(s1):
            pixels[i, j] = round(cumuTable[pixels[i, j]] * 255 / 480000)
    return pixels

def convCal(squ, padW):
    lowerCumu = 0
    length = padW*2 + 1
    for i in range(length):
        for j in range(length):
           if (squ[i, j] < squ[padW, padW]): lowerCumu += 1

    return (lowerCumu+1) * 255 / (length*length)


def locEqu(img, padW):
    imArr = np.pad(np.array(img), ((padW, padW), (padW, padW)), mode = 'reflect')
    for i in range(padW, padW+img.size[1]):
        for j in range(padW, padW+img.size[0]):
            chunk = imArr[i-padW:i+padW+1, j-padW:j+padW+1]
            imArr[i, j] = round(convCal(chunk, padW))
    return imArr[padW:800+padW, padW:600+padW]

def GausRemove(img):
    imArr = np.pad(np.array(img), ((1, 1), (1, 1)), mode = 'reflect')
    for i in range(1, 1+img.size[1]):
        for j in range(1, 1+img.size[0]):
            chunk = imArr[i-1:i+2, j-1:j+2]
            imArr[i, j] = np.sum(chunk) / 9
    return imArr[1:551, 1:501]

def medianRemove(img):
    pix = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            arr = []
            for x in range(i-1, i+2):
                for y in range(j-1, j+2):
                    if x == i and y == j:
                        continue
                    try :
                       arr.append(pix[x, y][0])
                    except :
                        if x < 0 : x = 0
                        if y < 0: y = 0
                        if x == 500: x -= 1
                        if y == 550: y -= 1
                        arr.append(pix[x, y][0])
            arr.sort()
            if pix[i, j][0] > arr[4] or (pix[i, j][0] < arr[4] and pix[i, j][0] == 0) : pix[i, j] = (arr[4], arr[4], arr[4])

def GausRemove3channels(img):
    pix = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            avg = pix[i, j][0]
            for x in range(i-1, i+2):
                for y in range(j-1, j+2):
                    try :
                        avg += pix[x, y][0]
                    except :
                        if x < 0 : x = 0
                        if y < 0: y = 0
                        if x == 500: x -= 1
                        if y == 550: y -= 1
                        avg += pix[x, y][0]
            pix[i, j] = (int(avg / 10), int(avg / 10), int(avg / 10))

def PSNRcal(img):
    orgImg = Image.open("./SampleImage/sample4.png")
    orgPix = orgImg.load()
    pix = img.load()
    mse = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if type(pix[i, j]) is tuple:
                mse += (pix[i, j][0] - orgPix[i, j]) * (pix[i, j][0] - orgPix[i, j])
            else:
                mse += (pix[i, j] - orgPix[i, j]) * (pix[i, j] - orgPix[i, j])
    mse /= 500 * 550
    return 10 * np.log10(255*255/mse)

def makePlot(pixels, s0, s1, pltName):
    vertical = [0] * 256
    for i in range(s0):
        for j in range(s1):
            vertical[pixels[i, j]] += 1
    plt.bar(range(256), vertical)
    plt.savefig(pltName)
    plt.clf()

# problem 0-a --
curImg = Image.open("./SampleImage/sample1.png")
pix = curImg.load()

for i in range(curImg.size[0]):
    for j in range(400):
        tmpPix = pix[i, j]
        pix[i, j] = pix[i, 799-j]
        pix[i, 799-j] = tmpPix
curImg.save("result1.png")
# -- problem 0-a

# problem 0-b --
for i in range(curImg.size[0]):
    for j in range(curImg.size[1]):
        gray = int(pix[i, j][0]*0.299 + pix[i, j][1]*0.587 + pix[i, j][2]*0.114)
        pix[i, j] = (gray, gray, gray)
curImg.save("result2.png")
# -- problem 0-b

# problem 1-a --
curImg = Image.open("./SampleImage/sample2.png")
pix = curImg.load()
# makePlot(pix, curImg.size[0], curImg.size[1], "hiss2.png")
    
for i in range(curImg.size[0]):
    for j in range(curImg.size[1]):
        pix[i, j] = int(pix[i, j] / 3)
curImg.save("result3.png")
# makePlot(pix, curImg.size[0], curImg.size[1], "hisr3.png")
# -- problem 1-a
    
# problem 1-b --
for i in range(curImg.size[0]):
    for j in range(curImg.size[1]):
        pix[i, j] = int(pix[i, j] * 3)
curImg.save("result4.png")
# makePlot(pix, curImg.size[0], curImg.size[1], "hisr4.png")
# -- problem 1-b

# problem 1-d --
curImg = Image.open("./SampleImage/sample2.png")
pix = curImg.load()
pix = globEqu(pix, curImg.size[0], curImg.size[1])
curImg.save("result5.png")
# makePlot(pix, curImg.size[0], curImg.size[1], "hisr5.png")

curImg = Image.open("./result3.png")
pix = curImg.load()
pix = globEqu(pix, curImg.size[0], curImg.size[1])
curImg.save("result6.png")
# makePlot(pix, curImg.size[0], curImg.size[1], "hisr6.png")


curImg = Image.open("./result4.png")
pix = curImg.load()
pix = globEqu(pix, curImg.size[0], curImg.size[1])
curImg.save("result7.png")
# makePlot(pix, curImg.size[0], curImg.size[1], "hisr7.png")
# -- problem 1-d

# problem 1-e --
curImg = Image.open("./SampleImage/sample2.png")
curImg = Image.fromarray(locEqu(curImg, 3))
curImg.save("result8.png")
# makePlot(pix, curImg.size[0], curImg.size[1], "hisr8.png")
# -- problem 1-e


# problem 1-f --
curImg = Image.open("./SampleImage/sample3.png")
pix = curImg.load()
for i in range(curImg.size[0]):
    for j in range(curImg.size[1]):
        pix[i, j] = int(pix[i, j] * 4)
curImg.save("result9.png")
# makePlot(pix, curImg.size[0], curImg.size[1], "hisr9.png")
# -- problem 1-f


# problem 2-a --
curImg = Image.open("./SampleImage/sample5.png")
# print(f"PSNR of sample5.png = {PSNRcal(curImg)}")
curImg = Image.fromarray(GausRemove(curImg))
# print(f"PSNR of result10.png = {PSNRcal(curImg)}")
curImg.save("result10.png")

curImg = Image.open("./SampleImage/sample6.png")
# print(f"PSNR of sample6.png = {PSNRcal(curImg)}")
medianRemove(curImg)
# print(f"PSNR of result11.png = {PSNRcal(curImg)}")
curImg.save("result11.png")
# -- problem 2-a

# problem 2-c --
curImg = Image.open("./SampleImage/sample7.png")
# print(f"PSNR of sample7.png = {PSNRcal(curImg)}")
medianRemove(curImg)
GausRemove3channels(curImg)
# print(f"PSNR of result12.png = {PSNRcal(curImg)}")
curImg.save("result12.png")
# -- problem 2-c