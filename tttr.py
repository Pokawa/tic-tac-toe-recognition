import cv2
from numpy import ones
from grid import is_grid, get_lines


def main():
    filename = './data/img8.jpg'
    image = cv2.imread(filename)

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_canny = cv2.Canny(image_gray, 100, 200)

    kernel = ones((2, 2))
    image_canny = cv2.dilate(image_canny, kernel)
    image_canny = cv2.erode(image_canny, kernel)
    image_canny = cv2.dilate(image_canny, kernel)

    contours, _ = cv2.findContours(image_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = [cv2.contourArea(c) for c in contours]
    bounding_boxes = sorted(bounding_boxes, reverse=True)

    x, y, w, h = cv2.boundingRect(contours[-1])
    piece = image[y:y + w, x:x + w]
    contour = image_canny[y:y + w, x:x + w]
    lines = get_lines(contour)
    possible = is_grid(contour.shape, lines)
    if possible is not None:
        print("{} found".format(possible))
        for line in possible:
            cv2.line(piece, line.p1, line.p2, (0, 0, 255), 1)

    cv2.imshow('zdjecie', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
