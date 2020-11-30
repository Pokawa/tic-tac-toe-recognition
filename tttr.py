from cv2 import imread, cvtColor, COLOR_BGR2GRAY, Canny, dilate, erode, imshow, waitKey, destroyAllWindows, \
    line, drawContours, boundingRect, rectangle, GaussianBlur, circle, resize, putText, FONT_HERSHEY_PLAIN
from numpy import ones
from grid import find_grids, get_min_area_box, pull_rotated_piece
from segment import recognise_segments
import sys


def main():
    image = imread(sys.argv[1])

    width = 800
    height = int(image.shape[0] * (width / image.shape[1]))
    image = resize(image, (width, height))

    image_gray = cvtColor(image, COLOR_BGR2GRAY)
    image_canny = Canny(image_gray, 100, 200)

    kernel = ones((2, 2))
    image_canny = dilate(image_canny, kernel)
    image_canny = erode(image_canny, kernel)
    image_canny = dilate(image_canny, kernel)

    found_grids = find_grids(image_canny)

    for (contour, lines, is_rotated), index in zip(found_grids, range(len(found_grids))):

        if is_rotated:
            _, box = get_min_area_box(contour)
            grid_image = pull_rotated_piece(image, contour)
            grid_gray = pull_rotated_piece(image_gray, contour)
            grid_contour = pull_rotated_piece(image_canny, contour)
            drawContours(image, [box], 0, (0, 0, 255), 2)
            putText(image, "grid {}".format(index), box[0], FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 2)
        else:
            x, y, w, h = boundingRect(contour)
            grid_image = image[y:y + h, x:x + w].copy()
            grid_gray = image_gray[y:y + h, x:x + w].copy()
            grid_contour = image_canny[y:y + h, x:x + w].copy()
            rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            putText(image, "grid {}".format(index), (x, y), FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 2)

        # print(lines)
        for x1, y1, x2, y2 in lines:
            line(grid_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        game_state = []
        for segment, mark in recognise_segments(grid_gray, grid_contour, lines):
            if mark is not None:
                segment_x, segment_y = segment[0]
                if mark[0]:
                    game_state.append('o')
                    x, y, r = mark[1]
                    circle(grid_image, (x + segment_x, y + segment_y), r, (0, 255, 0), 2)
                else:
                    game_state.append('x')
                    for x1, y1, x2, y2 in mark[1]:
                        line(grid_image, (x1 + segment_x, y1 + segment_y), (x2 + segment_x, y2 + segment_y), (255, 0, 0), 2)
            else:
                game_state.append('-')

        print("Grid {}".format(index))
        print("{}|{}|{}".format(game_state[0], game_state[1], game_state[2]))
        print("{}|{}|{}".format(game_state[3], game_state[4], game_state[5]))
        print("{}|{}|{}".format(game_state[6], game_state[7], game_state[8]))
        imshow("grid {}".format(index), grid_image)

    imshow(sys.argv[1], image)
    waitKey(0)
    destroyAllWindows()


if __name__ == "__main__":
    main()
