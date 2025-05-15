import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import os
import random

def getFrames(filename, first_frame, second_frame):
    cap = cv2.VideoCapture(filename)
    cap.set(cv2.CAP_PROP_POS_FRAMES, first_frame - 1)
    res1, fr1 = cap.read()
    cap.set(cv2.CAP_PROP_POS_FRAMES, second_frame - 1)
    res2, fr2 = cap.read()
    cap.release()
    return fr1, fr2

def getBitsPerPixel(im):
    h, w = im.shape
    im_list = im.tolist()
    bits = 0
    for row in im_list:
        for pixel in row:
            bits += math.log2(abs(pixel) + 1)
    return bits / (h * w)

def getReconstructTarget(residual, predicted):
    return np.add(residual, predicted)

def getResidual(target, predicted):
    return np.subtract(target, predicted)

def segmentImage(anchor, blockSize=16):
    h, w = anchor.shape
    hSegments = int(h / blockSize)
    wSegments = int(w / blockSize)
    return hSegments, wSegments

def getAnchorSearchArea(x, y, anchor, blockSize, searchArea):
    h, w = anchor.shape
    cx, cy = getCenter(x, y, blockSize)
    sx = max(0, cx - int(blockSize / 2) - searchArea)
    sy = max(0, cy - int(blockSize / 2) - searchArea)
    anchorSearch = anchor[
        sy:min(sy + searchArea * 2 + blockSize, h),
        sx:min(sx + searchArea * 2 + blockSize, w)
    ]
    return anchorSearch

def getCenter(x, y, blockSize):
    return int(x + blockSize / 2), int(y + blockSize / 2)

def getBestMatch(tBlock, aSearch, blockSize):
    step = 4
    ah, aw = aSearch.shape
    acy, acx = int(ah / 2), int(aw / 2)
    minMAD = float("+inf")
    minP = None
    while step >= 1:
        pointList = [
            (acx, acy), (acx + step, acy), (acx, acy + step), (acx + step, acy + step),
            (acx - step, acy), (acx, acy - step), (acx - step, acy - step),
            (acx + step, acy - step), (acx - step, acy + step)
        ]
        for p in pointList:
            aBlock = getBlockZone(p, aSearch, tBlock, blockSize)
            MAD = getMAD(tBlock, aBlock)
            if MAD < minMAD:
                minMAD = MAD
                minP = p
        step = int(step / 2)

    px, py = minP
    px, py = max(0, px - int(blockSize / 2)), max(0, py - int(blockSize / 2))
    matchBlock = aSearch[py:py + blockSize, px:px + blockSize]
    return matchBlock

def getBlockZone(p, aSearch, tBlock, blockSize):
    px, py = p
    px, py = max(0, px - int(blockSize / 2)), max(0, py - int(blockSize / 2))
    aBlock = aSearch[py:py + blockSize, px:px + blockSize]
    assert aBlock.shape == tBlock.shape
    return aBlock

def getMAD(tBlock, aBlock):
    return np.sum(np.abs(np.subtract(tBlock, aBlock))) / (tBlock.shape[0] * tBlock.shape[1])

def blockSearchBody(anchor, target, blockSize, searchArea=7):
    h, w = anchor.shape
    hSegments, wSegments = segmentImage(anchor, blockSize)
    predicted = np.ones((h, w)) * 255
    for y in range(0, int(hSegments * blockSize), blockSize):
        for x in range(0, int(wSegments * blockSize), blockSize):
            targetBlock = target[y:y + blockSize, x:x + blockSize]
            anchorSearchArea = getAnchorSearchArea(x, y, anchor, blockSize, searchArea)
            anchorBlock = getBestMatch(targetBlock, anchorSearchArea, blockSize)
            predicted[y:y + blockSize, x:x + blockSize] = anchorBlock
    return predicted

def main(anchorFrame, targetFrame, saveOutput=True):
    h, w, ch = anchorFrame.shape
    diffFrameRGB = np.zeros((h, w, ch))
    predictedFrameRGB = np.zeros((h, w, ch))
    residualFrameRGB = np.zeros((h, w, ch))
    restoreFrameRGB = np.zeros((h, w, ch))

    bitsAnchor = []
    bitsDiff = []
    bitsPredicted = []

    for i in range(0, 3):
        anchorFrame_c = anchorFrame[:, :, i]
        targetFrame_c = targetFrame[:, :, i]
        diffFrame = cv2.absdiff(anchorFrame_c, targetFrame_c)
        predictedFrame = blockSearchBody(anchorFrame_c, targetFrame_c, 16)
        residualFrame = getResidual(targetFrame_c, predictedFrame)
        reconstructTargetFrame = getReconstructTarget(residualFrame, predictedFrame)
        bitsAnchor.append(getBitsPerPixel(anchorFrame_c))
        bitsDiff.append(getBitsPerPixel(diffFrame))
        bitsPredicted.append(getBitsPerPixel(residualFrame))
        diffFrameRGB[:, :, i] = diffFrame
        predictedFrameRGB[:, :, i] = predictedFrame
        residualFrameRGB[:, :, i] = residualFrame
        restoreFrameRGB[:, :, i] = reconstructTargetFrame

    if saveOutput:
        cv2.imwrite("Results/First_frame.png", anchorFrame)
        cv2.imwrite("Results/Second_frame.png", targetFrame)
        cv2.imwrite("Results/Difference.png", diffFrameRGB)
        cv2.imwrite("Results/Prediction.png", predictedFrameRGB)
        cv2.imwrite("Results/Residual.png", residualFrameRGB)
        cv2.imwrite("Results/Restore.png", restoreFrameRGB)


    compression_ratio = round(sum(bitsAnchor) / sum(bitsPredicted), 2)
    plt.bar(["Original", "Difference", "Predicted"], [sum(bitsAnchor), sum(bitsDiff), sum(bitsPredicted)])
    plt.title(f"Compression Ratio = {compression_ratio}")

    results_dir = "D:\\TIC_Kratinov\\LessСompressionMPEG\\Results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    plt.savefig("Results/Histogram.png", dpi=300, format='png')


if __name__ == "__main__":
    fr = random.randint(0, 3000)
    frame1, frame2 = getFrames("sample4.avi", fr, fr + 1)
    main(frame1, frame2)
