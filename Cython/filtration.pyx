#cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True

import time
from PIL import Image
from libc.math cimport exp as c_exp
from cpython cimport array

# template pole
cdef array.array float_array_template = array.array('f', [])

def greyScale(img, int h, int w):
    """
    prevedeni obrazku na cernobily
    :param img: color picture, 1D array of tuples [(R,G,B), (R,G.B), ....]
    :param h: height of picture
    :param w: width of picture
    :return: black and white picture, array [x, x, ...]
    """

    greyPicture = [sum(img[i]) / 3 for i in range(h*w)]

    return greyPicture


def anisotropie(float[:] img, int h, int w, float lambdaValue=0.1, float sigma=0.015):
    """
    Anisotropic filtering (AF), a method of enhancing the image quality of textures
    :param img: greyScale image
    :param h: height of picture
    :param w: width of picture
    :param lambdaValue:
    :param sigma:
    :return: filtered picture
    """

    cdef float north = 0.0, south = 0.0, west = 0.0, east = 0.0, actual = 0.0
    cdef float northGradient = 0.0, southGradient = 0.0, westGradient = 0.0, eastGradient = 0.0
    cdef float cN = 0.0, cS = 0.0, cW = 0.0, cE = 0.0
    cdef int nt = 0
    cdef int N = h - 2, M = w - 2
    cdef int column = 0, row = 0, r = 0, c = 0

    # vytvarim pole
    cdef array.array newPic = array.clone(float_array_template, (h * w), zero=False)
    # reference na pole, pointer
    cdef float[:] newPicture = newPic

    for r in range(N):
        row = r + 1
        for c in range(M):
            column = c + 1

            north = (img[(row - 1) * w + column])
            south = (img[(row + 1) * w + column])
            west = (img[row * w + (column - 1)])
            east = (img[row * w + (column + 1)])

            actual = float(img[row * w + column])

            northGradient = north - actual
            southGradient = south - actual
            westGradient = west - actual
            eastGradient = east - actual

            cN = c_exp(-((northGradient ** 2) / (sigma ** 2)))
            cS = c_exp(-((southGradient ** 2) / (sigma ** 2)))
            cW = c_exp(-((westGradient ** 2) / (sigma ** 2)))
            cE = c_exp(-((eastGradient ** 2) / (sigma ** 2)))

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

    img = Image.new('L', (h, w))

    cdef int x = 0, y = 0

    for x in range(w):
        for y in range(h):
            img.putpixel((x, y), picture[x*w +y])

    img.rotate(270).transpose(Image.FLIP_LEFT_RIGHT).show()


def main(int count=10):
    img = Image.open('../lena.png')
    img.show()

    cdef int h = img.size[0]
    cdef int w = img.size[1]

    obrazek = img.getdata()
    greyPicture = greyScale(obrazek, h, w)
    showPicture(greyPicture, h, w)

    # generator dela rovnou nove pole. takze kopie
    aniPictureTmp = [greyPicture[i] / 255.0 for i in range(h * w)]
    cdef array.array aniPictureArr = array.array('f', aniPictureTmp)
    cdef float[:] aniPicture = aniPictureArr

    start = time.time()

    for i in range(count):
        aniPicture = anisotropie(aniPicture, h, w)
        # print i

    end = time.time()
    anisotropic_time = end - start

    print 'Anisotropic filtration time {0}'.format(anisotropic_time)

    aniPictureNormal = [int(aniPicture[i] * 255.0) for i in range(h * w)]
    showPicture(aniPictureNormal, h, w)

    # Anisotropic filtration time 0.164086103439


if __name__ == "__main__":
    main()
