from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

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

def holeFillReverse(s_x, s_y, imgArr):
    imgArr[s_x, s_y] = 0
    x_size = imgArr.shape[0]
    y_size = imgArr.shape[1]
    queue = [(s_x, s_y)]
    while (len(queue) > 0):
        center = queue.pop(0)
        x_coor = center[0]
        y_coor = center[1]
        if (y_coor > 0 and imgArr[x_coor, y_coor - 1] == 255) : 
            imgArr[x_coor, y_coor - 1] = 0
            queue.append((x_coor, y_coor - 1))
        if (x_coor > 0 and imgArr[x_coor - 1, y_coor] == 255) : 
            imgArr[x_coor - 1, y_coor] = 0
            queue.append((x_coor - 1, y_coor))
        if (y_coor < y_size - 1 and imgArr[x_coor, y_coor + 1] == 255) : 
            imgArr[x_coor, y_coor + 1] = 0
            queue.append((x_coor, y_coor + 1))
        if (x_coor < x_size - 1 and imgArr[x_coor + 1, y_coor] == 255) : 
            imgArr[x_coor + 1, y_coor] = 0
            queue.append((x_coor + 1, y_coor))
    return imgArr

def noiseLineRemove(imgArr) :
    Mask = np.array([0, 255, 0])
    for i in range(1, imgArr.shape[0] - 1):
        for j in range(1, imgArr.shape[1] - 1):
            if (np.array_equal(imgArr[i-1:i+2, j], Mask) or np.array_equal(imgArr[i, j-1:j+2], Mask)):
                imgArr[i, j] = 0
    return imgArr

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
                       arr.append(pix[x, y])
                    except :
                        if x < 0 : x = 0
                        if y < 0: y = 0
                        if x == 650: x -= 1
                        if y == 600: y -= 1
                        arr.append(pix[x, y])
            arr.sort()
            if pix[i, j] > arr[4] or (pix[i, j] < arr[4] and pix[i, j] == 0) : pix[i, j] = arr[4]

def GausRemove(img):
    imArr = np.pad(np.array(img), ((1, 1), (1, 1)), mode = 'reflect')
    for i in range(1, 1+img.size[1]):
        for j in range(1, 1+img.size[0]):
            chunk = imArr[i-1:i+2, j-1:j+2]
            imArr[i, j] = np.sum(chunk) / 9
    return imArr[1:601, 1:651]

def norTo255(target):
    Max = np.max(target)
    Min = np.min(target)
    if Min == Max : return target
    for i in range(target.shape[0]):
        for j in range(target.shape[1]):
            target[i, j] = ((target[i, j] - Min) / (Max - Min)) * 255
    return target
    
def Laws(imgArr) :
    maskDict = {"L" : np.array([1/6, 1/3, 1/6]), "E" : np.array([-1/2, 0, 1/2]), "S" : np.array([1/2, -1, 1/2])}
    imgArr = np.pad(imgArr, ((1, 1), (1, 1)), mode = 'reflect')
    result = np.empty([400, 600, 9], dtype=int)
    ch = -1
    for kl, vl in maskDict.items():
        for kr, vr in maskDict.items():
            ch += 1
            mask = np.dot(np.transpose(vl), vr)
            copyArr = np.copy(imgArr)
            for i in range(1, imgArr.shape[0] - 1):
                for j in range(1, imgArr.shape[1] - 1):
                    copyArr[i, j] = np.sum(np.multiply(imgArr[i-1:i+2, j-1:j+2], mask))
            # Image.fromarray(norTo255(copyArr[1:401, 1:601])).save(f".\\step-1-{kl+kr}.png")
            target = np.pad(copyArr[1:401, 1:601], ((6, 6), (6, 6)), mode = 'reflect')
            for i in range(6, target.shape[0] - 6):
                for j in range(6, target.shape[1] - 6):
                    value = np.std(target[i-6:i+7, j-6:j+7])
                    result[i-6, j-6, ch] = value
                    copyArr[i-6, j-6] = value
            # Image.fromarray(norTo255(copyArr[1:401, 1:601])).save(f".\\std\\step-2-{kl+kr}.png")
    return result


# problem 1-a --
curImg = Image.open(".\\SampleImage\\sample1.png")
imArr = np.array(curImg)
copyArr =  np.copy(imArr)
structEle = np.array([[255, 255, 255], [255, 255, 255], [255, 255, 255]])
for i in range(1, curImg.size[1] - 1):
    for j in range(1, curImg.size[0] - 1):
        chunk = imArr[i-1:i+2, j-1:j+2]
        if (np.array_equal(chunk, structEle)):
            copyArr[i, j] = 0
curImg = Image.fromarray(copyArr)
curImg.save(".\\result1.png")
# -- problem 1-a

# problem 1-b --
curImg = Image.open(".\\SampleImage\\sample1.png")
imArr = np.array(curImg)
filledArr = np.copy(imArr)
filledArr = holeFill(0 , 0, filledArr)
# Image.fromarray(filledArr).save(".\\s1BackFill.png")
for i in range(1, curImg.size[1] - 1):
    for j in range(1, curImg.size[0] - 1):
        if (imArr[i, j] == 0 and filledArr[i, j] == 0):
            imArr[i, j] = 255
curImg = Image.fromarray(imArr)
curImg.save(".\\result2.png")
# -- problem 1-b

# problem 1-c --
curImg = Image.open(".\\result2.png")
imArr = np.array(curImg)
imArr = noiseLineRemove(noiseLineRemove(imArr))
for i in range(1, curImg.size[1] - 1):
    for j in range(1, curImg.size[0] - 1):
        if (filledArr[i, j] == 0): #filledArr is generated at code section 1-(b)
            imArr[i, j] = 0
curImg = Image.fromarray(imArr)
curImg.save(".\\result3.png")
#hw1 noise remove
# curImg = Image.open(".\\SampleImage\\sample1.png")
# medianRemove(curImg)
# curImg.save("hw1MedianRemove.png")
# curImg = Image.open(".\\SampleImage\\sample1.png")
# curImg = Image.fromarray(GausRemove(curImg))
# curImg.save("hw1GausRemove.png")
#hw1 noise remove
# -- problem 1-c


# problem 1-d --
curImg = Image.open(".\\result3.png")
imArr = np.array(curImg)
for i in range(1, curImg.size[1] - 1):
    for j in range(1, curImg.size[0] - 1):
        if (filledArr[i, j] == 0): #filledArr is generated at code section 1-(b)
            imArr[i, j] = 255
objCnt = 0
for i in range(1, curImg.size[1] - 1):
    for j in range(1, curImg.size[0] - 1):
        if (imArr[i, j] == 255):
            objCnt += 1
            imArr = holeFillReverse(i, j, imArr)
            # Image.fromarray(imArr).save(f".\\count-({objCnt}).png")
print(f"number of objects in sample1.png is {objCnt}")
# -- problem 1-d

# problem 2-a --
curImg = Image.open(".\\SampleImage\\sample2.png")
imArr = np.array(curImg)
featMap = Laws(imArr) # later for 2-(b)
# -- problem 2-a

# problem 2-b --
cent1 = featMap[200, 300]
cent2 = featMap[380, 300]
cent3 = featMap[300, 500]
newCent1 = featMap[200, 300]
newCent2 = featMap[380, 300]
newCent3 = featMap[300, 500]
shift = 50000000
while shift > 0:
    # print(f"counting, cur shift = {shift}")
    g1 = []
    g2 = []
    g3 = []
    for i in range(400):
        for j in range(600):
            dist1 =  np.linalg.norm(featMap[i, j] - cent1)
            dist2 =  np.linalg.norm(featMap[i, j] - cent2)
            dist3 =  np.linalg.norm(featMap[i, j] - cent3)
            if dist1 <= dist2 and dist1 <= dist3: 
                g1.append(featMap[i, j])
                imArr[i, j] = 0
            elif dist2 <= dist1 and dist2 <= dist3: 
                g2.append(featMap[i, j])
                imArr[i, j] = 125
            else: 
                g3.append(featMap[i, j])
                imArr[i, j] = 255
    newCent1 = np.mean(g1, axis = 0)
    newCent2 = np.mean(g2, axis = 0)
    newCent3 = np.mean(g3, axis = 0)
    shift = (np.linalg.norm(cent1 - newCent1) + np.linalg.norm(cent2 - newCent2) + np.linalg.norm(cent3 - newCent3)) / 3
    cent1 = newCent1
    cent2 = newCent2
    cent3 = newCent3
Image.fromarray(imArr).save("result4.png")
# -- problem 2-b

# problem 2-c --
curImg = Image.open(".\\result4.png")
cPix = curImg.load()
groundImg = Image.open(".\\texture\\ground.png")
gPix = groundImg.load()
g_x = groundImg.size[0]
g_y = groundImg.size[1]
treeImg = Image.open(".\\texture\\tree.png")
tPix = treeImg.load()
t_x = treeImg.size[0]
t_y = treeImg.size[1]
skyImg = Image.open(".\\texture\\sky.png")
sPix = skyImg.load()
s_x = skyImg.size[0]
s_y = skyImg.size[1]

for i in range(curImg.size[0]):
    for j in range(curImg.size[1]):
        if j > 350 :
            gray = int(gPix[i % g_x, j % g_y][0]*0.299 + gPix[i % g_x, j % g_y][1]*0.587 + gPix[i % g_x, j % g_y][2]*0.114)
            cPix[i, j] = gray 
        elif cPix[i, j] == 0:
            leftBox = i < 130 and j > 100 and j < 140
            rightBox = i > 380 and j < 50
            if leftBox or rightBox :
                gray = int(sPix[i % s_x, j % s_y][0]*0.299 + sPix[i % s_x, j % s_y][1]*0.587 + sPix[i % s_x, j % s_y][2]*0.114)
            else :
                gray = int(tPix[i % t_x, j % t_y][0]*0.299 + tPix[i % t_x, j % t_y][1]*0.587 + tPix[i % t_x, j % t_y][2]*0.114)
            cPix[i, j] = gray 
        else :
            gray = int(sPix[i % s_x, j % s_y][0]*0.299 + sPix[i % s_x, j % s_y][1]*0.587 + sPix[i % s_x, j % s_y][2]*0.114)
            cPix[i, j] = gray
curImg.save("result5.png")
# -- problem 2-c
