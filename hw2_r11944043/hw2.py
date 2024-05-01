from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def GausRemove(img):
    imArr = np.pad(np.array(img), ((1, 1), (1, 1)), mode = 'reflect')
    retArr = np.copy(imArr)
    for i in range(1, 1+img.size[1]):
        for j in range(1, 1+img.size[0]):
            chunk = imArr[i-1:i+2, j-1:j+2]
            retArr[i, j] = np.sum(chunk) / 9
    return retArr[1 : 501, 1 : 501]

def GausRemove5by5(img):
    imArr = np.pad(np.array(img), ((2, 2), (2, 2)), mode = 'reflect')
    retArr = np.copy(imArr)
    weightArr = np.array([[2, 4, 5, 4, 2], [4, 9, 12, 9, 4], [5, 12, 15, 12, 5], [4, 9, 12, 9, 4], [2, 4, 5, 4, 2]])
    for i in range(2, 2+img.size[1]):
        for j in range(2, 2+img.size[0]):
            chunk = imArr[i-2:i+3, j-2:j+3]
            sum = 0
            for x in range(5):
                for y in range(5):
                    sum += chunk[x, y] * weightArr[x, y]
            retArr[i, j] = int(sum / 159)
    return retArr[2:602, 2:602]

def sobelDetect(img):
    imArr = np.pad(np.array(img), ((1, 1), (1, 1)), mode = 'reflect')
    retArr = np.copy(imArr)
    for i in range(1, 1+img.size[1]):
        for j in range(1, 1+img.size[0]):
            chunk = imArr[i-1:i+2, j-1:j+2]
            rowG = 0.25 * (chunk[0,2]+2*chunk[1,2]+chunk[2,2]-chunk[0,0]-2*chunk[1,0]-chunk[2,0])
            colG = 0.25 * (chunk[0,0]+2*chunk[0,1]+chunk[0,2]-chunk[2,0]-2*chunk[2,1]-chunk[2,2])
            retArr[i, j] = np.sqrt(rowG*rowG + colG*colG)
    return retArr[1 : 601, 1 : 601]

def directionAssign(val) :
    if ((val >= -22.5 and val < 22.5) or (val>= -180 and val < -157.5) or (val >= 157.5)): return 0
    elif ((val >= 22.5 and val < 67.5) or (val>= -157.5 and val < -112.5)): return 1
    elif ((val >= 67.5 and val < 112.5) or (val>= -112.5 and val < -67.5)): return 2
    elif ((val >= 112.5 and val < 157.5) or (val>= -67.5 and val < -22.5)): return 3

def NMS(imArr, degMap):
    padArr = np.pad(imArr, ((1, 1), (1, 1)), mode = 'reflect')
    reArr = np.copy(padArr)
    for i in range(1, 601):
        for j in range(1, 601):
            chunk = padArr[i-1:i+2, j-1:j+2]
            paraA = 0
            paraB = 0 
            direction = degMap[i, j]
            if (direction == 0) :
                paraA = chunk[1, 2]
                paraB = chunk[1, 0]
            elif (direction == 1) :
                paraA = chunk[0, 2]
                paraB = chunk[2, 0]
            elif (direction == 2) :
                paraA = chunk[0, 1]
                paraB = chunk[2, 1] 
            else :
                paraA = chunk[0, 0]
                paraB = chunk[2, 2] 
            if (imArr[i-1, j-1] > paraA and imArr[i-1, j-1] > paraB) : reArr[i, j] = imArr[i-1, j-1]
            else : reArr[i, j] = 0
    return reArr[1 : 601, 1 : 601]

def linkLine(imgArr, x, y):
    if imgArr[x, y] == 255 :
        for Xoffset in range(-1, 2):
            for Yoffset in range(-1, 2):
                offX = min(max(0, x+Xoffset), 599)
                offY = min(max(0, y+Yoffset), 599)
                if imgArr[offX, offY] == 1:
                    imgArr[offX, offY] = 255
                    if offX != 0 and offX != 599 and offY != 0 and offY != 599:
                        imgArr = linkLine(imgArr, offX, offY)
    return imgArr

def canny(img):
    img = Image.fromarray(GausRemove5by5(img))
    imArr = np.pad(np.array(img), ((1, 1), (1, 1)), mode = 'reflect')
    retArr = np.copy(imArr)
    degreeMap = np.copy(imArr)
    for i in range(1, 1+img.size[1]):
        for j in range(1, 1+img.size[0]):
            chunk = imArr[i-1:i+2, j-1:j+2]
            rowG = 0.25 * (chunk[0,2]+2*chunk[1,2]+chunk[2,2]-chunk[0,0]-2*chunk[1,0]-chunk[2,0])
            colG = 0.25 * (chunk[0,0]+2*chunk[0,1]+chunk[0,2]-chunk[2,0]-2*chunk[2,1]-chunk[2,2])
            degreeMap[i, j] = directionAssign(np.degrees(np.arctan2(colG, rowG)))
            retArr[i, j] = np.sqrt(rowG*rowG + colG*colG)
    thresImg = NMS(retArr[1 : 601, 1 : 601], degreeMap)
    upBond = 15
    lowBond = 10
    edgeSet = []
    for i in range(600):
        for j in range(600):
            if thresImg[i, j] >= upBond : 
                thresImg[i, j] = 255
                edgeSet.append((i, j))
            elif thresImg[i, j] >= lowBond : thresImg[i, j] = 1
            else: thresImg[i, j] = 0
    for ed in edgeSet :
        thresImg = linkLine(thresImg, ed[0], ed[1])
    return thresImg

def makePlot(pixels, s0, s1, pltName):
    vertical = [0] * 256
    for i in range(s0):
        for j in range(s1):
            vertical[pixels[i, j]] += 1
    for i in range(1, 256):
        vertical[i] += vertical[i-1]
    plt.bar(range(256), vertical)
    plt.savefig(pltName)
    plt.clf()


def lapGau(img):
    img = Image.fromarray(GausRemove5by5(img))
    imArr = np.pad(np.array(img), ((1, 1), (1, 1)), mode = 'reflect')
    retArr = np.copy(imArr)
    lapWeight = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    for i in range(1, 1+img.size[1]):
        for j in range(1, 1+img.size[0]):
            chunk = imArr[i-1:i+2, j-1:j+2]
            sum = 0
            for x in range(3):
                for y in range(3):
                    sum += chunk[x, y] * lapWeight[x, y]
            secDeri = sum / 8
            if (abs(secDeri) < 2) : retArr[i, j] = 0
            elif (secDeri > 0) : retArr[i, j] = 3
            else : retArr[i, j] = 1
    for i in range(1, 1+img.size[1]):
        for j in range(1, 1+img.size[0]):
            if (retArr[i, j] == 0):
                chunk = retArr[i-1:i+2, j-1:j+2]
                r1 = (chunk[0, 2] - 2 ) * (chunk[2, 0] - 2)
                r2 = (chunk[1, 0] - 2 ) * (chunk[1, 2] - 2)
                r3 = (chunk[0, 0] - 2 ) * (chunk[2, 2] - 2)
                r4 = (chunk[0, 1] - 2 ) * (chunk[2, 1] - 2)
                if (r1 == -1 or r2 == -1 or r3 == -1 or r4 == -1):
                    retArr[i-1, j-1] = 255
    return retArr[1:601, 1:601]
    

# problem 1-a --
curImg = Image.open(".\\SampleImage\\sample1.png")
curImg = Image.fromarray(sobelDetect(curImg))
curImg.save(".\\result1.png")
pix = curImg.load()
for i in range(curImg.size[0]):
    for j in range(curImg.size[1]):
            if(pix[i, j] < 35) : pix[i, j] = 0
curImg.save(".\\result2.png")
# -- problem 1-a

# problem 1-b --
curImg = Image.open(".\\SampleImage\\sample1.png")
curImg = Image.fromarray(canny(curImg))
curImg.save("result3.png")
# -- problem 1-b

# problem 1-c --
curImg = Image.open(".\\SampleImage\\sample1.png")
curImg = Image.fromarray(lapGau(curImg))
curImg.save("result4.png")

# -- problem 1-c


# problem 1-d --
curImg = Image.open(".\\SampleImage\\sample2.png")
pix = curImg.load()
lowPassImg = Image.fromarray(GausRemove(curImg))
lowPix = lowPassImg.load()

for i in range(curImg.size[0]):
    for j in range(curImg.size[1]):
        pix[i, j] = int(pix[i, j] * 3 - lowPix[i,j] * 2)
curImg.save(".\\result5.png")
# -- problem 1-d

# problem 2-a --
curImg = Image.open(".\\SampleImage\\sample3.png")
imgArr = np.array(curImg)
barArr = np.copy(imgArr)

for i in range(curImg.size[1]):
    shiftY = 300 - i
    for j in range(curImg.size[0]):
        shiftX = j - 270
        rad = np.sqrt(shiftX*shiftX + shiftY*shiftY)
        coe = 1 + (30/180000)*rad**2
        # print(coe, rad)
        # orgRad = int(rad*coe)
        orgX = int(shiftX * coe)
        orgY = int(shiftY * coe)
        outOfBound = 0
        if (orgX < -299 ) or (orgX > 299) : outOfBound = 1
        if (orgY < -299 ) or (orgY > 299) : outOfBound = 1
        if not outOfBound : barArr[i, j] = imgArr[300 - orgY, orgX + 270]
        else : barArr[i, j] = 255

scaleMat = np.array([[2, 0],[0, 2]])
scaleMatInv = np.linalg.inv(scaleMat)
rotateMat = np.array([[np.cos(np.deg2rad(-45)), -np.sin(np.deg2rad(-45))],[np.sin(np.deg2rad(-45)), np.cos(np.deg2rad(-45))]])
rotateMatInv = np.linalg.inv(rotateMat)
newArr = np.copy(barArr)
centerShifted = np.dot(rotateMat, np.dot(scaleMat, np.array([299, 299])))
xOffset = int(centerShifted[0]) % 600 - 299
yOffset = int(centerShifted[1]) % 600 - 299
for i in range(curImg.size[1]):
    for j in range(curImg.size[0]):
        orgCoor = np.dot(rotateMatInv, np.dot(scaleMatInv, np.array([j, 599-i])))
        orgCoor[1] = int(orgCoor[1]-xOffset) % 600
        orgCoor[0] = int(orgCoor[0]-yOffset) % 600
        newArr[(i+30) % 600, (j+80) % 600] = barArr[599 - int(orgCoor[1]), int(orgCoor[0])]

curImg = Image.fromarray(newArr)
curImg.save(".\\result8.png")
# -- problem 2-a

# problem 2-b --
curImg = Image.open(".\\SampleImage\\sample5.png")
imgArr = np.array(curImg)
newArr = np.copy(imgArr)
for i in range(curImg.size[1]):
    offset = int(np.sin(np.deg2rad(i*360/160 - 120)) * 30)
    for j in range(curImg.size[0]):
        newArr[i, j] = imgArr[i, (j - offset) % 800]
curImg = Image.fromarray(newArr)
curImg.save(".\\result9.png")
# -- problem 2-b