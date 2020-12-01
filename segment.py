from itertools import combinations

from numpy import int0, pi, radians
from line import Line
from cv2 import HoughCircles, HOUGH_GRADIENT, HoughLinesP, GaussianBlur, medianBlur


def get_grid_segments(lines, shape):
    vertical_left, vertical_right, horizontal_up, horizontal_down = lines
    up_left = int0(Line.intersection_point(vertical_left, horizontal_up))
    down_left = int0(Line.intersection_point(vertical_left, horizontal_down))
    up_right = int0(Line.intersection_point(vertical_right, horizontal_up))
    down_right = int0(Line.intersection_point(vertical_right, horizontal_down))

    end_y, end_x = shape
    p1 = (0, 0)
    p2 = (up_left[0], 0)
    p3 = (up_right[0], 0)
    p4 = (0, up_left[1])
    p5 = (end_x, up_right[1])
    p6 = (0, down_left[1])
    p7 = (end_x, down_right[1])
    p8 = (down_left[0], end_y)
    p9 = (down_right[0], end_y)
    p10 = (end_x, end_y)

    segments = ((p1, up_left),
                (p2, up_right),
                (p3, p5),
                (p4, down_left),
                (up_left, down_right),
                (up_right, p7),
                (p6, p8),
                (down_left, p9),
                (down_right, p10))

    return segments


def find_circle(segment):
    blured = GaussianBlur(segment.copy(), (3, 3), 1.5, sigmaY=1.5)
    min_distance = min(segment.shape) // 2
    return HoughCircles(blured, HOUGH_GRADIENT, 1, min_distance, param1=80, param2=30, minRadius=0, maxRadius=0)


def find_cross(segment_contour):
    shape = segment_contour.shape[0:2]

    min_line_length = min(shape) * pow(2, 0.5) // 4  # minimum number of pixels making up a line
    max_line_gap = min(shape) * 0.05  # maximum gap in pixels between connectable line segments
    lines = HoughLinesP(segment_contour, 1, pi / 180, 15, minLineLength=min_line_length, maxLineGap=max_line_gap)
    if lines is None:
        return

    lines = [Line((line[0][0], line[0][1]), (line[0][2], line[0][3])) for line in lines]

    for l1, l2 in combinations(lines, 2):
        if Line.is_perpendicular(l1, l2, max_difference=radians(30)):
            if not l1.is_horizontal(radians(5)) and not l2.is_horizontal(radians(5)):
                if not l1.is_vertical(radians(5)) and not l2.is_vertical(radians(5)):
                    point = Line.intersection_point(l1, l2)
                    if point is not None:

                        if l1.is_in_middle(point, min_line_length / 3) and \
                                l2.is_in_middle(point, min_line_length / 3):
                            return l1, l2


def recognise_segments(grid_gray, grid_contour, lines):
    segments = get_grid_segments(lines, grid_contour.shape)

    segments_contour = [grid_contour[y1:y2, x1:x2] for (x1, y1), (x2, y2) in segments]
    segments_gray = [grid_gray[y1:y2, x1:x2] for (x1, y1), (x2, y2) in segments]

    result = []
    for gray, contour, segment in zip(segments_gray, segments_contour, segments):
        recognised = recognise_segment(gray, contour)
        result.append((segment, recognised))
    return result


def recognise_segment(gray, contour):
    lines = find_cross(contour)
    if lines is not None:
        return False, lines

    circle = find_circle(gray)
    if circle is not None:
        return True, int0(circle[0][0])
