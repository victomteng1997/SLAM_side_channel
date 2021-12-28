from utils.FeatureExtract import process_img
import os
import cv2
import time
from threading import Thread
import cython


@cython.boundscheck(False)
cpdef unsigned char[:, :] condition_list_fast(unsigned char [:, :] image):
    cdef int x, y, HEIGHT, WEIGHT
    HEIGHT= image.shape[0]
    WEIGHT = image.shape[1]
    # data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    data = image
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
        condition_list


def GenerateImage(source_path, output_path, start_from = None):
    folder_1 = "image_0"
    folder_2 = "image_1"

    filenames = os.listdir(source_path+folder_1)
    filenames.sort()
    if start_from:
        filenames = filenames[start_from:]
    # print(filenames)
    start_time = time.time()
    for img_name in filenames:
        im_gray1 = cv2.imread(source_path+folder_1+'/'+img_name, cv2.IMREAD_GRAYSCALE)
        im_gray1 = cv2.imread(source_path+folder_2+'/'+img_name,  cv2.IMREAD_GRAYSCALE)
        mat1 = process_img(im_gray1)
        mat2 = process_img(im_gray1)
        cv2.imwrite(output_path+folder_1+'/'+img_name, mat1)
        cv2.imwrite(output_path+folder_2+ '/' + img_name, mat2)
        print("Processed:", str(img_name), "Time:", str(time.time()-start_time))

def GenerateImageCython(source_path, output_path, start_from=None):
    folder_1 = "image_0"
    folder_2 = "image_1"

    filenames = os.listdir(source_path + folder_1)
    filenames.sort()
    if start_from:
        filenames = filenames[start_from:]
    # print(filenames)
    start_time = time.time()
    for img_name in filenames:
        im_gray1 = cv2.imread(source_path + folder_1 + '/' + img_name, cv2.IMREAD_GRAYSCALE)
        im_gray2 = cv2.imread(source_path + folder_2 + '/' + img_name, cv2.IMREAD_GRAYSCALE)
        result = condition_list_fast(im_gray1)
        #mat1 = process_img(im_gray1)
        #mat2 = process_img(im_gray2)
        #cv2.imwrite(output_path + folder_1 + '/' + img_name, mat1)
        #cv2.imwrite(output_path + folder_2 + '/' + img_name, mat2)
        print("Processed:", str(img_name), "Time:", str(time.time() - start_time))



if __name__ == "__main__":
    source_path = "./resource/07/"
    output_path = "./output_resource_cython/07/"
    result = GenerateImageCython(source_path, output_path, start_from=0)
