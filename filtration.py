from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
import math

# prevedeni obrazku na cernobily, 2D pole
def greyScale(img):
    v, s, t = img.shape
    '''
    grayPicture = np.zeros((v, s), dtype=np.uint8)
    for row in range(0, v):
        for column in range(0, s):
            grayPicture[row][column] = sum(img[row][column]) / 3
    '''
    greyPicture = [[[sum(img[row][column]) / 3] for column in range(v)] for row in range(s)]
    return greyPicture

# ulozeni obrazku do 3D pole
def greyTriColor(greyPicture):
    v, s = greyPicture.shape
    '''
    img = np.zeros((v, s, 3), dtype=np.uint8)
    for row in range(0, v):
        for column in range(0, s):
            img[row][column][0] = grayPicture[row][column]
            img[row][column][1] = grayPicture[row][column]
            img[row][column][2] = grayPicture[row][column]
    '''
    img = [[[
        greyPicture[row][column],
        greyPicture[row][column],
        greyPicture[row][column]
        ] for column in range(s)
        ] for row in range(v)
        ]
    return img


def greyTriColorFloat(greyPicture):
    v, s = greyPicture.shape
    '''
    img = np.zeros((v, s, 3), dtype=np.float)
    for row in range(0, v):
        for column in range(0, s):
            img[row][column][0] = grayPicture[row][column]
            img[row][column][1] = grayPicture[row][column]
            img[row][column][2] = grayPicture[row][column]
    '''
    img = [[[
        greyPicture[row][column],
        greyPicture[row][column],
        greyPicture[row][column]
        ] for column in range(s)
        ] for row in range(v)
        ]
    return img


'''
def gluePictures(first, second):  # must be same size
    v, s = first.shape[:2]
    newPicture = np.zeros((v, 2 * s, 3), dtype=np.uint8)
    first.astype(np.float64)
    second.astype(np.float64)
    for row in range(0, v):
        for column in range(0, s):
            newPicture[row][column][0] = first[row][column][0]
            newPicture[row][column][1] = first[row][column][1]
            newPicture[row][column][2] = first[row][column][2]

            newPicture[row][column + s][0] = second[row][column][0]
            newPicture[row][column + s][1] = second[row][column][1]
            newPicture[row][column + s][2] = second[row][column][2]
    return newPicture
'''

# slepeni 3 obrazku k sobe
def glue(*images):
    sumWidth = 0
    maxHight = 0

    for image in images:
        h, w = image.shape[:2]
        sumWidth += w

        if maxHight < h:
            maxHight = h

    # newPicture = np.zeros((maxHight, sumWidth, 3), dtype=np.uint8)
    newPicture = [[[0][0][0] for column in range(sumWidth)] for row in range(maxHight)]
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

    # newPicture = img
    #newPicture = np.zeros((h, w))
    # Proc musim pokazde udelat kopii obrazku ???
    newPicture = img.copy()

    #print newPicture.dtype

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


            #cN = (math.exp(-((northGradient ** 2) / (sigma ** 2)))) * northGradient
            #cS = (math.exp(-((southGradient ** 2) / (sigma ** 2)))) * southGradient
            #cW = (math.exp(-((westGradient ** 2) / (sigma ** 2))))*westGradient
            #cE = (math.exp(-((eastGradient ** 2) / (sigma ** 2))))*eastGradient


            """
            gN = math.exp(-((north ** 2) / (sigma ** 2)))
            gS = math.exp(-((south ** 2) / (sigma ** 2)))
            gW = math.exp(-((west ** 2) / (sigma ** 2)))
            gE = math.exp(-((east ** 2) / (sigma ** 2)))
            """
            cN = math.exp(-((northGradient ** 2) / (sigma ** 2)))
            cS = math.exp(-((southGradient ** 2) / (sigma ** 2)))
            cW = math.exp(-((westGradient ** 2) / (sigma ** 2)))
            cE = math.exp(-((eastGradient ** 2) / (sigma ** 2)))

            #newPicture[row][column] = (actual + north + south + west + east )/5
            newPicture[row][column] = actual * (1 - lambdaValue * (cN + cS + cW + cE)) + lambdaValue * (
            cN * north + cS * south + cW * west + cE * east)

    return newPicture


# return newNextPicture


# #######################################################################################################################

def main():
    # Creating a numpy array from an image file:
    obrazek = misc.imread('lena.png')
    #print type(obrazek)

    greyPicture = greyScale(obrazek)
    # aniPicture = anisotropie(greyPicture)
    # aniPicture = greyPicture / 255.0

    #
    aniPicture = greyPicture.copy() / 255.0
    # print aniPicture[10][10]
    for i in range(0, 50):
        aniPicture = anisotropie(aniPicture)
        print i
    # print aniPicture[10][10]

    triGrey = greyTriColor(greyPicture)
    aniPicture *= 255
    triPicture = greyTriColorFloat(aniPicture)
    # triPicture *= 255
    # print triPicture[10][10]

    allPictures = glue(obrazek, triGrey, triPicture)

    plt.imsave("output7.png", allPictures)
    plt.imshow(allPictures)
    plt.show()


if __name__ == "__main__":
    main()
