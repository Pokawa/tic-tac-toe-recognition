from skimage.io import imread, imshow
from skimage.transform import rotate, resize, rescale
from skimage.feature import match_template, canny
from skimage.draw import polygon
from skimage.color import rgb2gray
from skimage.measure import find_contours
from skimage.morphology import dilation, erosion
from matplotlib import pyplot 
from numpy import arange, where, unravel_index, argmax

def close_and_dilation(image):
    image = dilation(image)
    image = erosion(image)
    image = dilation(image)
    image = dilation(image)
    return image

def fill_contours(image):
    contours = find_contours(image, 0.8)
    for contour in contours:
        rr, cc = polygon(contour[:, 0], contour[:, 1])
        image[rr, cc] = True
    return image

def prepare_image(image):
    image = rgb2gray(image)
    image = canny(image, sigma=3)
    image = close_and_dilation(image)
    image = fill_contours(image)
    return image

def main():
    template = imread("./data/img_template.jpg")
    image = imread("./data/img2.jpg")

    prepared_template = prepare_image(template)
    prepared_image = prepare_image(image)

    result = match_template(prepared_image, prepared_template)
    ij = unravel_index(argmax(result), result.shape)
    x, y = ij[::-1]

    print(x, y)

    ax1 = pyplot.subplot(2, 2, 1)
    ax2 = pyplot.subplot(2, 2, 2)
    ax3 = pyplot.subplot(2, 2, 3)
    ax4 = pyplot.subplot(2, 2, 4)

    ax1.imshow(prepared_template)
    ax2.imshow(prepared_image)
    ax3.imshow(result)
    ax4.imshow(image)

    h, w = prepared_template.shape
    rect = pyplot.Rectangle((x, y), w, h, edgecolor='r', facecolor='none')
    ax4.add_patch(rect)

    pyplot.show()


if __name__ == "__main__":
    main()