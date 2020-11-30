from math import atan2, tan, sqrt, radians, pi

from numpy import int0


class Line:
    """
    Line class with comparison methods
    """

    def __init__(self, p1, p2):
        if p1[0] ** 2 + p1[1] ** 2 > p2[0] ** 2 + p2[1] ** 2:
            p1, p2 = p2, p1

        (x1, y1) = p1
        (x2, y2) = p2
        self.p1 = (x1, y1)
        self.p2 = (x2, y2)
        self.coordinates = (x1, y1, x2, y2)

        self.angle = atan2(y2 - y1, x2 - x1)
        self.length = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def __repr__(self):
        return "({}:{}, {}:{})".format(self.p1[0], self.p1[1], self.p2[0], self.p2[1])

    def __iter__(self):
        return self.coordinates.__iter__()

    @staticmethod
    def is_parallel(line1, line2, max_difference=radians(0)):
        """
        predicate - checks if two lines are parallel
        """
        difference = abs(line1.angle - line2.angle)
        return difference < max_difference

    @staticmethod
    def is_perpendicular(line1, line2, max_difference=radians(0)):
        """
        predicate - checks if two lines are perpendicular
        """
        difference = abs(line1.angle - line2.angle)
        return difference > radians(90) - max_difference

    @staticmethod
    def intersection_point(line1, line2):
        x_difference = (line1.p1[0] - line1.p2[0], line2.p1[0] - line2.p2[0])
        y_difference = (line1.p1[1] - line1.p2[1], line2.p1[1] - line2.p2[1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(x_difference, y_difference)
        if div == 0:
            return None

        d = (det(line1.p1, line1.p2), det(line2.p1, line2.p2))
        x = det(d, x_difference) / div
        y = det(d, y_difference) / div
        return x, y

    def is_in_rectangle(self, p1, p2):
        """
        predicate - checks if line is in given rectangle
        """
        checks_p1 = [p1[0] <= self.p1[0], p1[1] <= self.p1[1], p1[0] <= self.p2[0], p1[1] <= self.p2[1]]
        checks_p2 = [p2[0] >= self.p1[0], p2[1] >= self.p1[1], p2[0] >= self.p2[0], p2[1] >= self.p2[1]]
        return all(checks_p1) and all(checks_p2)

    def is_in_middle(self, p, max_difference=5):
        x1, y1 = self.p1
        x2, y2 = p
        distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return self.length / 2 - max_difference <= distance <= self.length / 2 + max_difference

    def is_vertical(self, max_difference=radians(0)):
        return pi / 2 - max_difference <= self.angle <= pi / 2 + max_difference

    def is_horizontal(self, max_difference=radians(0)):
        return -max_difference <= self.angle <= max_difference
