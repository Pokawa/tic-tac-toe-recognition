from math import pi, atan, sqrt, radians


class Line:
    """
    Line class with comparison methods
    """

    def __init__(self, p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2
        self.p1 = (x1, y1)
        self.p2 = (x2, y2)
        self.angle = atan((y2 - y1) / (x2 - x1))
        self.length = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def __repr__(self):
        return "({}:{}, {}:{})".format(self.p1[0], self.p1[1], self.p2[0], self.p2[1])

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

    def is_in_rectangle(self, p1, p2):
        """
        predicate - checks if line is in given rectangle
        """
        checks_p1 = [p1[0] <= self.p1[0], p1[1] <= self.p1[1], p1[0] <= self.p2[0], p1[1] <= self.p2[1]]
        checks_p2 = [p2[0] >= self.p1[0], p2[1] >= self.p1[1], p2[0] >= self.p2[0], p2[1] >= self.p2[1]]
        return all(checks_p1) and all(checks_p2)
