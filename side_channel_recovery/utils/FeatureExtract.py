from PIL import Image
import numpy as np
from sklearn.preprocessing import minmax_scale
import cv2


def process_img(im_gray):
    HEIGHT, WIDTH = im_gray.shape
    # data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    data = im_gray
    # for row in data:
    # print(' '.join('{:3}'.format(value) for value in row))
    threshold = 15  # cannot change
    condition_list = []
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            if i < 3 or i > len(data) - 4 or j < 3 or j > len(data[0]) - 4:
                condition_list.append(1)
                continue
            pixel = data[i][j]
            condition = 0
            if (data[i - 3][j] > pixel + threshold and data[i + 3][j] > pixel + threshold) or (
                    data[i - 3][j] < pixel - threshold and data[i + 3][j] < pixel - threshold):
                condition = 1
                condition_list.append(condition)
                continue

            ## three corner
            diff = 3
            if (data[i][j - 3] > pixel + threshold and data[i][j + 3] > pixel + threshold) or (
                    data[i][j - 3] < pixel - threshold and data[i][j + 3] < pixel - threshold):
                diff -= 1
            if (data[i - 2][j - 2] > pixel + threshold and data[i + 2][j + 2] > pixel + threshold) or (
                    data[i - 2][j - 2] < pixel - threshold and data[i + 2][j + 2] < pixel - threshold):
                diff -= 1
            if (data[i - 2][j + 2] > pixel + threshold and data[i + 2][j - 2] > pixel + threshold) or (
                    data[i - 2][j + 2] < pixel - threshold and data[i + 2][j - 2] < pixel - threshold):
                diff -= 1
            if diff < 2:
                condition = 2
                condition_list.append(condition)
                continue

            ## check the next condition
            pixel_positions = [(0, 3), (-1, 3), (-2, 2), (-3, 1), (-3, 0), (-3, -1), (-2, -2), (-1, -3), (0, -3),
                               (1, -3), (2, -2), (3, -1), (3, 0), (3, 1), (2, 2), (1, 3)]
            continous = 0
            previous_sign = 0
            for pixel_change in pixel_positions:
                new_x = i + pixel_change[0]
                new_y = j + pixel_change[1]
                point_pixel = data[new_x][new_y]
                if previous_sign == 0:
                    if point_pixel > pixel:
                        previous_sign = 1
                    else:
                        previous_sign = -1
                    continous += 1
                else:
                    if (point_pixel > pixel + threshold and previous_sign == 1) or (
                            point_pixel < pixel - threshold and previous_sign == -1):
                        continous += 1
                    else:
                        continous = 0
                        if point_pixel > pixel:
                            previous_sign = 1
                        else:
                            previous_sign = -1
                if continous >= 8:
                    condition = 4
                    # print("4 here")
                    continue
            condition = 3
            condition_list.append(condition)
    # print(condition_list)
    final_image = [0] * (WIDTH * HEIGHT)
    #print(len(condition_list))
    condition_list = [condition_list[offset:offset + WIDTH] for offset in range(0, WIDTH * HEIGHT, WIDTH)]
    final_image = [final_image[offset:offset + WIDTH] for offset in range(0, WIDTH * HEIGHT, WIDTH)]

    #print(len(final_image), len(final_image[1]))
    #print(len(condition_list), len(condition_list[1]))

    for i in range(3, len(condition_list) - 3):
        for j in range(3, len(condition_list[0]) - 3):
            try:
                point = condition_list[i][j]
                # print(point)
                if point == 1:
                    # print("No corner")
                    pass
                if point == 2:
                    for x in range(-3, 4):
                        for y in range(-3, 4):
                            p_c = (i + x, j + x)
                            if abs(x) + abs(y) < 1:
                                final_image[p_c[0]][p_c[1]] += 10
                            elif abs(x) + abs(y) < 2:
                                final_image[p_c[0]][p_c[1]] += 5
                            elif abs(x) + abs(y) < 3:
                                final_image[p_c[0]][p_c[1]] += 2
                            elif abs(x) + abs(y) < 4:
                                final_image[p_c[0]][p_c[1]] += 1
                            elif abs(x) + abs(y) < 5:
                                final_image[p_c[0]][p_c[1]] += 0
                if point == 3:
                    for x in range(-3, 4):
                        for y in range(-3, 4):
                            p_c = (i + x, j + x)
                            if abs(x) + abs(y) < 1:
                                final_image[p_c[0]][p_c[1]] += 20
                            elif abs(x) + abs(y) < 2:
                                final_image[p_c[0]][p_c[1]] += 3
                            elif abs(x) + abs(y) < 3:
                                final_image[p_c[0]][p_c[1]] += 2
                            elif abs(x) + abs(y) < 4:
                                final_image[p_c[0]][p_c[1]] += 1
                            elif abs(x) + abs(y) < 5:
                                final_image[p_c[0]][p_c[1]] += 0

                if point == 4:
                    for x in range(-3, 4):
                        for y in range(-3, 4):
                            p_c = (i + x, j + x)
                            if abs(x) + abs(y) < 1:
                                final_image[p_c[0]][p_c[1]] += 30
                            elif abs(x) + abs(y) < 2:
                                final_image[p_c[0]][p_c[1]] += 10
                            elif abs(x) + abs(y) < 3:
                                final_image[p_c[0]][p_c[1]] += 5
                            elif abs(x) + abs(y) < 4:
                                final_image[p_c[0]][p_c[1]] += 2
                            elif abs(x) + abs(y) < 5:
                                final_image[p_c[0]][p_c[1]] += 1
            except:
                print("Error")
                print(p_c[0], p_c[1], len(final_image[p_c[0]]), len(condition_list[i]))

    # print("final intensity without normalizing", final_image)

    one_dimension_list = []

    for item in final_image:
        for pixel in item:
            one_dimension_list.append(pixel)

    array = np.array(one_dimension_list)
    print(max(array), min(array))

    norm_array = minmax_scale(array, feature_range=(0, 255))
    # print(norm_array)
    norm_array = 255 - norm_array
    mat = np.reshape(norm_array, (HEIGHT, WIDTH))

    return mat


def post_processing(mat):
    '''
    The general idea is to process the image so that the lines are connected
    '''

    threshold = 10
    mat_copy = mat.copy()
    for i in range(2, len(mat) - 2):
        for j in range(2, len(mat[i]) - 2):
            direction_1 = [[i - 1, j - 1], [i + 1, j + 1]]
            direction_2 = [[i - 1, j], [i + 1, j]]
            direction_3 = [[i + 1, j - 1], [i - 1, j + 1]]
            direction_4 = [[i, j + 1], [i, j - 1]]

            darkest = min(mat[i - 1][j - 1:j + 2] + mat[i][j - 1:j + 2] + mat[i + 1][j - 1:j + 2])
            baseline = darkest + threshold
            pixel = mat[i][j]
            if pixel > darkest + threshold:
                processed = False
                cor = direction_1
                if mat[cor[0][0]][cor[0][1]] > baseline and mat[cor[1][0]][cor[1][1]] > baseline:
                    # should increase the intensity
                    processed = True
                    mat_copy[cor[0][0]][cor[0][1]] = min(240, mat_copy[i][j] + 100)
                    mat_copy[cor[1][0]][cor[1][1]] = min(240, mat_copy[i][j] + 100)
                cor = direction_2
                if mat[cor[0][0]][cor[0][1]] > baseline and mat[cor[1][0]][cor[1][1]] > baseline:
                    # should increase the intensity
                    processed = True
                    mat_copy[cor[0][0]][cor[0][1]] = min(240, mat_copy[i][j] + 200)
                    mat_copy[cor[1][0]][cor[1][1]] = min(240, mat_copy[i][j] + 200)
                cor = direction_3
                if mat[cor[0][0]][cor[0][1]] > baseline and mat[cor[1][0]][cor[1][1]] > baseline:
                    # should increase the intensity
                    processed = True
                    mat_copy[cor[0][0]][cor[0][1]] = min(240, mat_copy[i][j] + 100)
                    mat_copy[cor[1][0]][cor[1][1]] = min(240, mat_copy[i][j] + 100)
                cor = direction_4
                if mat[cor[0][0]][cor[0][1]] > baseline and mat[cor[1][0]][cor[1][1]] > baseline:
                    # should increase the intensity
                    processed = True
                    mat_copy[cor[0][0]][cor[0][1]] = min(240, mat_copy[i][j] + 100)
                    mat_copy[cor[1][0]][cor[1][1]] = min(240, mat_copy[i][j] + 100)
                if processed:
                    mat_copy[i][j] = min(240, mat_copy[i][j] + 100)

    return mat_copy





### Sample usage below:

'''
im_gray = cv2.imread('house.jpg', cv2.IMREAD_GRAYSCALE)
# print(im_gray)

# print(data)


mat = process_img(im_gray)
mat_copy = post_processing(mat)

print("Before processing", np.uint8(mat))
print("After processing", np.uint8(mat_copy))

# cv2.imshow("Window1", np.uint8(mat_copy))
# cv2.imshow("Window2", np.uint8(mat))
# cv2.waitKey(0)
cv2.imwrite("result.jpg", mat)
cv2.imwrite("result_processed.jpg", mat_copy)
'''