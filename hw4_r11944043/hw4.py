from PIL import Image
import json
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

def holeFill(s_x, s_y, imgArr, bgVal, objVal):
    imgArr[s_x, s_y] = objVal
    x_size = imgArr.shape[0]
    y_size = imgArr.shape[1]
    queue = [(s_x, s_y)]
    while (len(queue) > 0):
        center = queue.pop(0)
        x_coor = center[0]
        y_coor = center[1]
        if (y_coor > 0 and imgArr[x_coor, y_coor - 1] == bgVal) : 
            imgArr[x_coor, y_coor - 1] = objVal
            queue.append((x_coor, y_coor - 1))
        if (x_coor > 0 and imgArr[x_coor - 1, y_coor] == bgVal) : 
            imgArr[x_coor - 1, y_coor] = objVal
            queue.append((x_coor - 1, y_coor))
        if (y_coor < y_size - 1 and imgArr[x_coor, y_coor + 1] == bgVal) : 
            imgArr[x_coor, y_coor + 1] = objVal
            queue.append((x_coor, y_coor + 1))
        if (x_coor < x_size - 1 and imgArr[x_coor + 1, y_coor] == bgVal) : 
            imgArr[x_coor + 1, y_coor] = objVal
            queue.append((x_coor + 1, y_coor))
    return imgArr

def drawLetter(s_x, s_y, imgArr):
    empty =  np.full((80, 80), 255, dtype = np.uint8)
    x_size = imgArr.shape[0]
    y_size = imgArr.shape[1]
    queue = [(s_x, s_y)]
    pixelsDrawn = 0
    while (len(queue) > 0):
        pixelsDrawn += 1
        center = queue.pop(0)
        x_coor = center[0]
        y_coor = center[1]
        empty[50 + x_coor - s_x, 25 + y_coor - s_y] = 0
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
    if pixelsDrawn <= 10:
        empty = "do Not detect"
    return (imgArr, empty)

def erode(tarArr):
    erodeCnt = 1
    struEle1 = np.array([[255, 255, 255], [-1, 0, -1], [0, 0, 0]])
    struEle2 = np.array([[-1, 255, 255], [0, 0, 255], [-1, 0, -1]])
    while erodeCnt > 0:
        erodeCnt = 0
        for i in range(1, tarArr.shape[0] - 1):
            for j in range(1, tarArr.shape[1] - 1):
                if tarArr[i, j] == 255 : continue
                chunk = tarArr[i-1:i+2, j-1:j+2]
                hit = False
                tmpST1 = np.copy(struEle1)
                tmpST2 = np.copy(struEle2)
                for rotate in range(4):
                    if matchWithST(tmpST1, chunk) or matchWithST(tmpST2, chunk):
                        hit = True
                        break                    
                    tmpST1 = np.rot90(tmpST1)
                    tmpST2 = np.rot90(tmpST2)
                if (hit):
                    erodeCnt += 1
                    tarArr[i, j] = 255
    return tarArr


def findBoundingCoor(tarArr):
    result = [-2, -2, -2, -2] #left-border, right-border, top-border, bottom-border

    for i in range(tarArr.shape[0]):
        for j in range(tarArr.shape[1]):
            if tarArr[i, j] == 0: 
                result[2] = i-1
                break
        if result[2] != -2 : break
    
    for i in range(tarArr.shape[0]-1, -1, -1):
        for j in range(tarArr.shape[1]):
            if tarArr[i, j] == 0: 
                result[3] = i+1
                break
        if result[3] != -2 : break
    
    for i in range(tarArr.shape[1]):
        for j in range(tarArr.shape[0]):
            if tarArr[j, i] == 0: 
                result[0] = i-1
                break
        if result[0] != -2 : break
    
    for i in range(tarArr.shape[1]-1, -1, -1):
        for j in range(tarArr.shape[0]):
            if tarArr[j, i] == 0: 
                result[1] = i+1
                break
        if result[1] != -2 : break
    
    return result
                
def calLake(tarArr):
    tarArr = holeFill(0, 0, tarArr, 255, 0)
    lSize = 0
    for i in range(tarArr.shape[0]):
        for j in range(tarArr.shape[1]):
            if tarArr[i, j] == 255:
                lSize += 1
    return lSize

def circularCal(tarArr):
    pValue = 0
    insideValue = 0
    structEle = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    for i in range(1, tarArr.shape[0] - 1):
        for j in range(1, tarArr.shape[1] - 1):
            if tarArr[i, j] == 0: pValue += 1
            chunk = tarArr[i-1:i+2, j-1:j+2]
            if (np.array_equal(chunk, structEle)):
                insideValue += 1
    return (pValue, pValue - insideValue)

def intensityCal(tarArr):
    black = 0
    for i in range(tarArr.shape[0]):
        for j in range(tarArr.shape[1]):
            if tarArr[i, j] == 0:
                black += 1
    return black / (tarArr.shape[0] * tarArr.shape[1])

def matchWithST(st, tar):
    for i in range(3):
        for j in range(3):
            if st[i, j] == -1: continue
            elif st[i, j] != tar[i, j]: return False
    return True

def removeSpur(tarArr):
    mask1 = np.array([255, 0, 255])
    mask2 = np.array([[255], [0], [255]])
    for i in range(1, tarArr.shape[0] - 1):
        for j in range(1, tarArr.shape[1] - 1):
            if np.array_equal(tarArr[i, j-1:j+2], mask1) or np.array_equal(tarArr[i-1:i+2, j], mask2):
                tarArr[i, j] = 255
    return tarArr


def extractFeat(tarChar, src, SetFeature, width):
    qValueArr = [0, 0, 0, 0, 0]
    diaArr1 = np.array([[255, 0], [0, 255]])
    diaArr2 = np.array([[0, 255], [255, 0]])
    for i in range(79):
        for j in range(width - 1):
            chunk = src[i:i+2, j:j+2]
            qValue = np.count_nonzero(chunk)
            if qValue == 2:
                if np.array_equal(chunk, diaArr1) or np.array_equal(chunk, diaArr2):
                    qValueArr[0] += 1
                else:
                    qValueArr[2] += 1
            elif qValue > 0:
                qValueArr[qValue] += 1
    SetFeature[tarChar] = {}
    SetFeature[tarChar]["E"] = 0.25 * qValueArr[1] - 0.25 * qValueArr[3] + 0.5 * qValueArr[0]
    (p0, a0) = circularCal(src)    
    SetFeature[tarChar]["circularity"] = 4 * np.pi * a0 / (p0**2)
    hwRes = findBoundingCoor(src) 
    wid = hwRes[1] - hwRes[0]
    hei = hwRes[3] - hwRes[2]
    bt = wid + hei
    SetFeature[tarChar]["W_Ratio"] = wid / bt
    SetFeature[tarChar]["H_Ratio"] = hei / bt
    SetFeature[tarChar]["Top_Int"] = intensityCal(src[hwRes[2] + 1: hwRes[2] + 3, hwRes[0] + 1: hwRes[1]])
    SetFeature[tarChar]["Bot_Int"] = intensityCal(src[hwRes[3] - 2: hwRes[3], hwRes[0] + 1: hwRes[1]])
    SetFeature[tarChar]["Lef_Int"] = intensityCal(src[hwRes[2] + 1: hwRes[3], hwRes[0] + 1: hwRes[0] + 3])
    SetFeature[tarChar]["Rig_Int"] = intensityCal(src[hwRes[2] + 1: hwRes[3], hwRes[1] - 2: hwRes[1]])
    SetFeature[tarChar]["Lake_Ratio"] = -1
    if SetFeature[tarChar]["E"] == 0:
        lakeSize = calLake(src)
        SetFeature[tarChar]["Lake_Ratio"] = lakeSize / p0

def engClassifier(features, trainSet):
    if features["E"] == trainSet["B"]["E"]: return "B"

    elif features["E"] == trainSet["A"]["E"]: 
        if features["Lake_Ratio"] <= trainSet["A"]["Lake_Ratio"] + 0.10: return "A"
        else: return "D"

    elif features["Top_Int"] <= trainSet["Y"]["Top_Int"] + 0.10: return "Y" 

    elif features["Bot_Int"] >= 0.5: return "E"

    elif features["Lef_Int"] >= 0.5: return "F"

    else: return "T"
    
def digitClassifier(features, trainSet):
    
    if features["E"] == trainSet["8"]["E"]: return "8"

    elif features["E"] == trainSet["6"]["E"]: return "6"

    elif (np.ceil(features["H_Ratio"] / features["W_Ratio"]) 
        >= np.ceil(trainSet["1"]["H_Ratio"] / trainSet["1"]["W_Ratio"])): return "1"
    
    elif ((trainSet["7"]["Bot_Int"] + 0.12) >= features["Bot_Int"]   
        and features["Bot_Int"] >= (trainSet["7"]["Bot_Int"] - 0.12)) : return "7"

    elif (features["Top_Int"] >= (trainSet["5"]["Top_Int"] - 0.10)) : return "5"
    
    else: return "3"




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

# -- problem 2 --

curImg = Image.open(f"./SampleImage/TrainingSet.png")

# pre-process train set---------
imArr = np.array(curImg)[:, :, 0]
for i in range(curImg.size[0]):
    for j in range(curImg.size[1]):
        if imArr[j, i] > 20 : imArr[j, i] = 255
        else : imArr[j, i] = 0


# start training---------
TrainingSetFeature = {}
# row 1 training
target = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
for i in range(12):
    letterArr = imArr[50:130, 20 + i*100 : 120 + i*100]
    # Image.fromarray(erode(letterArr)).save(f"./erod/{target[i]}.png")
    extractFeat(target[i], letterArr, TrainingSetFeature, 100)

# row 2 training
target = ["M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W"]
for i in range(11):
    letterArr = imArr[240:320, 20 + i*106 : 126 + i*106]
    # Image.fromarray(erode(letterArr)).save(f"./erod/{target[i]}.png")
    extractFeat(target[i], letterArr, TrainingSetFeature, 106)
    
# row 3 training
target = ["X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
for i in range(13):
    letterArr = imArr[430:510, 20 + i*96 : min((116 + i*96), 1240)]
    # Image.fromarray(erode(letterArr)).save(f"./erod/{target[i]}.png")
    extractFeat(target[i], letterArr, TrainingSetFeature, 96)

# with open("TrainingSetFeat.json", "w") as f: 
#     json.dump(TrainingSetFeature, f)

# start test input--------------------------------------
# testSetFeat = {
#     "test2" : {},
#     "test3" : {},
#     "test4" : {},
# }
for i in range(2, 5):
    curImg = Image.open(f"./SampleImage/sample{i}.png")
    pix = curImg.load()
    binaryPlate = grayScale(pix, curImg.size[0], curImg.size[1], i)
    output = ""
    for y in range(binaryPlate.shape[0]):
        if binaryPlate[y, 0] == 0:
            binaryPlate = holeFill(y, 0, binaryPlate, 0, 255)
            break
    # Image.fromarray(binaryPlate).save(f"BW{i}.png")
    detectHeight = curImg.size[1] - 25
    curLetter = np.full((80, 80), 255, dtype = np.uint8)
    letterCnt = 0
    for x in range(curImg.size[0]):
        if binaryPlate[detectHeight, x] == 0:
            binaryPlate, curLetter = drawLetter(detectHeight, x, binaryPlate)
            if not isinstance(curLetter, str): 
                letterFeat = {}
                curLetter = removeSpur(curLetter)
                # Image.fromarray(curLetter).save(f"./tests/{i}-{letterCnt}.png")
                extractFeat(letterCnt, curLetter, letterFeat, 80)
                # testSetFeat[f"test{i}"][letterCnt] = letterFeat[letterCnt]
                if letterCnt < 3 : #只有前三碼是英文
                    output += engClassifier(letterFeat[letterCnt], TrainingSetFeature)
                else: 
                    output += digitClassifier(letterFeat[letterCnt], TrainingSetFeature)
                letterCnt += 1
    # print(f"identify result of sample{i}.png is {output}")
    print(output)
# with open("TestSetFeat.json", "w") as f: 
#     json.dump(testSetFeat, f)
        
# -- problem 2 --