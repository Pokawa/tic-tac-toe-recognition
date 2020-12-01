from line import Line
from cv2 import HoughLinesP, findContours, minAreaRect, boxPoints, warpPerspective, getPerspectiveTransform, imshow
from cv2 import RETR_EXTERNAL, CHAIN_APPROX_SIMPLE, boundingRect
from math import radians, pi
from numpy import int0, array


def find_grids(image_contour):
    """
    Finds all areas of image that are TTT grid
    """
    # finds external contours
    contours, hierarchy = findContours(image_contour, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
    result = []

    for contour in contours:
        grid = get_grid(contour, image_contour)
        if grid is not None:
            lines, is_rotated = grid
            result.append((contour, lines, is_rotated))

    return result


def get_grid(contour, image_contour):
    straight_grid = check_for_straight_grids(contour, image_contour)
    if straight_grid is not None:
        return straight_grid, False
    # rotated_grid = check_for_rotated_grids(contour, image_contour)
    # if rotated_grid is not None:
    #     return rotated_grid, True


def check_for_straight_grids(contour, image_contour):
    x, y, w, h = boundingRect(contour)
    piece = image_contour[y:y + h, x:x + w]
    if is_properly_big(piece, image_contour):
        return find_grid_lines(piece)


def check_for_rotated_grids(contour, image_contour):
    warped_piece = pull_rotated_piece(image_contour, contour)
    if is_properly_big(warped_piece, image_contour):
        return find_grid_lines(warped_piece)


def is_properly_big(piece, image_contour):
    return min(piece.shape) > min(image_contour.shape) * 0.1


def pull_rotated_piece(image, contour):
    rectangle, box = get_min_area_box(contour)

    width = int(rectangle[1][0])
    height = int(rectangle[1][1])
    src_pts = box.astype("float32")

    dst_pts = array([[0, height - 1],
                     [0, 0],
                     [width - 1, 0],
                     [width - 1, height - 1]], dtype="float32")
    matrix = getPerspectiveTransform(src_pts, dst_pts)
    return warpPerspective(image, matrix, (width, height))


def get_min_area_box(contour):
    rectangle = minAreaRect(contour)
    box = int0(boxPoints(rectangle))
    return rectangle, box


def find_grid_lines(image_contour):
    shape = image_contour.shape

    min_line_length = min(shape[0:2]) * 0.5  # minimum number of pixels making up a line
    max_line_gap = min(shape[0:2]) * 0.1  # maximum gap in pixels between connectable line segments
    lines = HoughLinesP(image_contour, 1, pi / 180, 15, minLineLength=min_line_length, maxLineGap=max_line_gap)
    lines = [Line((line[0][0], line[0][1]), (line[0][2], line[0][3])) for line in lines]

    lines = get_properly_spaced(shape, lines)
    return find_properly_angled(lines)


def get_properly_spaced(shape, lines):
    end_x = shape[1]
    end_y = shape[0]
    half_x = end_x // 2
    half_y = end_y // 2

    lines = array(sorted(lines, key=lambda line: line.length, reverse=True))
    vertical_left = lines[[line.is_in_rectangle((0, 0), (half_x, end_y)) for line in lines]]
    vertical_right = lines[[line.is_in_rectangle((half_x, 0), (end_x, end_y))for line in lines]]
    horizontal_up = lines[[line.is_in_rectangle((0, 0), (end_x, half_y)) for line in lines]]
    horizontal_down = lines[[line.is_in_rectangle((0, half_y), (end_x, end_y)) for line in lines]]
    return vertical_left, vertical_right, horizontal_up, horizontal_down


def find_properly_angled(lines):
    vertical_left, vertical_right, horizontal_up, horizontal_down = lines

    for line1 in vertical_left:
        for line2 in vertical_right:
            for line3 in horizontal_up:
                for line4 in horizontal_down:
                    if are_properly_angled((line1, line2, line3, line4)):
                        return line1, line2, line3, line4


def are_properly_angled(lines: tuple):
    l1, l2, l3, l4 = lines

    if not Line.is_parallel(l1, l2, max_difference=radians(10)):
        return False
    if not Line.is_parallel(l3, l4, max_difference=radians(10)):
        return False
    if not Line.is_perpendicular(l1, l3, max_difference=radians(10)):
        return False

    # if not l1.is_vertical(radians(10)):
    #     return False
    # if not l2.is_vertical(radians(10)):
    #     return False
    # if not l3.is_horizontal(radians(10)):
    #     return False
    # if not l4.is_horizontal(radians(10)):
    #     return False

    return True
