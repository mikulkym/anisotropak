import math
import copy
import time
from PIL import Image


def greyScale(img, shape):
    """
    prevedeni obrazku na cernobily
    :param img: barevny obrazek, 1D pole tuplu [(R,G,B), (R,G.B), ....]
    :param shape: rozmer obrazku
    :return: cernobily obrazek, pole [x, x, ...]
    """
    s, v = shape
    greyPicture = [sum(img[i]) / 3 for i in range(v * s)]

    return greyPicture


def anisotropie(img, shape, lambdaValue=0.1, sigma=0.015):
    """
     anisotropic filtering of image
    :param img:
    :param shape: rozmer obrazku
    :param lambdaValue: konstanta
    :param sigma: konstanta
    :return: filtered image
    """
    h, w = shape

    newPicture = copy.copy(img)

    for row in range(1, h - 1):
        for column in range(1, w - 1):
            north = float(img[(row - 1) * w + column])
            south = float(img[(row + 1) * w + column])
            west = float(img[row * w + (column - 1)])
            east = float(img[row * w + (column + 1)])

            actual = float(img[row * w + column])

            northGradient = north - actual
            southGradient = south - actual
            westGradient = west - actual
            eastGradient = east - actual

            cN = math.exp(-((northGradient ** 2) / (sigma ** 2)))
            cS = math.exp(-((southGradient ** 2) / (sigma ** 2)))
            cW = math.exp(-((westGradient ** 2) / (sigma ** 2)))
            cE = math.exp(-((eastGradient ** 2) / (sigma ** 2)))

            newPicture[row * w + column] = actual * (1 - lambdaValue * (cN + cS + cW + cE)) + lambdaValue * (
            cN * north + cS * south + cW * west + cE * east)

    return newPicture


def showPicture(picture, shape):
    img = Image.new('L', shape)
    h, w = shape
    for x in range(w):
        for y in range(h):
            img.putpixel((x, y), picture[x*w +y])

    img.rotate(270).transpose(Image.FLIP_LEFT_RIGHT).show()


def main():
    img = Image.open('../lena.png')
    shape = img.size
    obrazek = img.getdata()

    img.show()
    h, w = shape

    greyPicture = greyScale(obrazek, shape)
    showPicture(greyPicture, shape)

    # generator dela rovnou nove pole. takze kopie
    aniPicture = [greyPicture[i] / 255.0 for i in range(h * w)]

    start = time.time()
    for i in range(0, 10):
        aniPicture = anisotropie(aniPicture, shape)
        print i
    end = time.time()
    anisotropic_time = end - start
    print 'Anisotropic filtration time {0}'.format(anisotropic_time)

    aniPicture = [int(aniPicture[i] * 255.0) for i in range(h * w)]
    showPicture(aniPicture, shape)


if __name__ == "__main__":
    main()
