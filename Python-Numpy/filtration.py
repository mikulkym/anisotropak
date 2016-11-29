from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
import math
import time

# prevedeni obrazku na cernobily, 2D pole
def grayScale(img):
    v, s, t = img.shape
    grayPicture = np.zeros((v, s), dtype=np.uint8)
    for row in range(0, v):
        for column in range(0, s):
            grayPicture[row][column] = sum(img[row][column]) / 3
    return grayPicture


# ulozeni obrazku do 3D pole
def grayTriColor(grayPicture):
    v, s = grayPicture.shape
    img = np.zeros((v, s, 3), dtype=np.uint8)
    for row in range(0, v):
        for column in range(0, s):
            img[row][column][0] = grayPicture[row][column]
            img[row][column][1] = grayPicture[row][column]
            img[row][column][2] = grayPicture[row][column]
    return img


def grayTriColorFloat(grayPicture):
    v, s = grayPicture.shape
    img = np.zeros((v, s, 3), dtype=np.float)
    for row in range(0, v):
        for column in range(0, s):
            img[row][column][0] = grayPicture[row][column]
            img[row][column][1] = grayPicture[row][column]
            img[row][column][2] = grayPicture[row][column]
    return img


# slepeni 3 obrazku k sobe
def glue(*images):
    sumWidth = 0
    maxHight = 0

    for image in images:
        h, w = image.shape[:2]
        sumWidth += w

        if maxHight < h:
            maxHight = h

    newPicture = np.zeros((maxHight, sumWidth, 3), dtype=np.uint8)
    # print "h", maxHight, "w", sumWidth
    actualEnd = 0
    actualBegin = 0
    for image in images:
        h, w = image.shape[:2]
        actualEnd += w
        for x in range(actualBegin, actualEnd):
            for y in range(0, h):
                for c in range(0, 3):
                    # print "short ", (x - actualBegin), "long ", x
                    newPicture[y][x][c] = image[y][x - actualBegin][c]
        actualBegin += w
    return newPicture


def anisotropie(img, lambdaValue=0.1, sigma=0.015):
    h, w = img.shape

    newPicture = img.copy()
    # print newPicture.dtype

    for row in range(1, h - 1):
        for column in range(1, w - 1):
            north = float(img[row - 1][column])
            south = float(img[row + 1][column])
            west = float(img[row][column - 1])
            east = float(img[row][column + 1])

            actual = float(img[row][column])

            northGradient = north - actual
            southGradient = south - actual
            westGradient = west - actual
            eastGradient = east - actual

            cN = math.exp(-((northGradient ** 2) / (sigma ** 2)))
            cS = math.exp(-((southGradient ** 2) / (sigma ** 2)))
            cW = math.exp(-((westGradient ** 2) / (sigma ** 2)))
            cE = math.exp(-((eastGradient ** 2) / (sigma ** 2)))

            newPicture[row][column] = actual * (1 - lambdaValue * (cN + cS + cW + cE)) + lambdaValue * (
            cN * north + cS * south + cW * west + cE * east)

    return newPicture


def main():
    # Read an image from a file as an array
    obrazek = misc.imread('../lena.png')
    # print type(obrazek)

    grayPicture = grayScale(obrazek)
    aniPicture = grayPicture.copy() / 255.0
    # print aniPicture[10][10]

    start = time.time()

    for i in range(0, 10):
        aniPicture = anisotropie(aniPicture)
        print i

    end = time.time()
    anisotropic_time = end - start

    print 'Anisotropic filtration time {0}'.format(anisotropic_time)

    triGray = grayTriColor(grayPicture)
    aniPicture *= 255
    triPicture = grayTriColorFloat(aniPicture)

    allPictures = glue(obrazek, triGray, triPicture)

    plt.imsave("output7.png", allPictures)
    plt.imshow(allPictures)
    plt.show()


if __name__ == "__main__":
    main()
