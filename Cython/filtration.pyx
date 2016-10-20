import math
import copy
import time
from PIL import Image


def greyScale(img, int h, int w):
    """
    prevedeni obrazku na cernobily
    :param img: color picture, 1D array of tuples [(R,G,B), (R,G.B), ....]
    :param h: height of picture
    :param w: width of picture
    :return: black and white picture, array
    """
    # s, v = shape
    greyPicture = [sum(img[i]) / 3 for i in range(h * w)]

    return greyPicture


def anisotropie(img, int h, int w, float lambdaValue=0.1, float sigma=0.015):
    """
    Anisotropic filtering (AF), a method of enhancing the image quality of textures
    :param img: greyScale image
    :param h: height of picture
    :param w: width of picture
    :param lambdaValue:
    :param sigma:
    :return: filtered picture
    """
    # h, w = shape

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


cdef void showPicture(picture, int h, int w):
    """
    Displays a picture
    :param picture: picture to display
    :param h: height of picture
    :param w: width of picture
    """

    img = Image.new('L', h, w)
    # h, w = shape
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

    greyPicture = greyScale(obrazek, h, w)
    showPicture(greyPicture, h, w)

    # generator dela rovnou nove pole. takze kopie
    aniPicture = [greyPicture[i] / 255.0 for i in range(h * w)]

    start = time.time()
    for i in range(0, 10):
        aniPicture = anisotropie(aniPicture, h, w)
        print i
    end = time.time()
    anisotropic_time = end - start
    print 'Anisotropic filtration time {0}'.format(anisotropic_time)

    aniPicture = [int(aniPicture[i] * 255.0) for i in range(h * w)]
    showPicture(aniPicture, h, w)


if __name__ == "__main__":
    main()
