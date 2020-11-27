from line import Line
from itertools import permutations
from cv2 import HoughLinesP
from math import radians, pi


def get_lines(image):
    min_line_length = image.shape[0] * 0.5  # minimum number of pixels making up a line
    max_line_gap = image.shape[0] * 0.05  # maximum gap in pixels between connectable line segments
    lines = HoughLinesP(image, 1, pi / 180, 15, minLineLength=min_line_length, maxLineGap=max_line_gap)
    return [Line((line[0][0], line[0][1]), (line[0][2], line[0][3])) for line in lines]


def is_grid(shape, lines):
    for permutation in list(permutations(lines, 4)):
        if are_properly_spaced(shape, permutation) and are_properly_angled(permutation):
            return permutation


def are_properly_spaced(shape, lines: tuple):
    end_x = shape[1]
    end_y = shape[0]
    half_y = end_y // 2
    half_x = end_x // 2

    l1, l2, l3, l4 = lines

    if not l1.is_in_rectangle((0, 0), (half_x, end_y)):
        return False
    if not l2.is_in_rectangle((half_x, 0), (end_x, end_y)):
        return False
    if not l3.is_in_rectangle((0, 0), (end_x, half_y)):
        return False
    if not l4.is_in_rectangle((0, half_y), (end_x, end_y)):
        return False

    print("{} properly spaced".format(lines))
    return True


def are_properly_angled(lines: tuple):
    l1, l2, l3, l4 = lines
    return Line.is_parallel(l1, l2, max_difference=radians(5)) \
           and Line.is_parallel(l3, l4, max_difference=radians(5)) \
           and Line.is_perpendicular(l1, l3, max_difference=radians(5))
