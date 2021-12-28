from utils.FeatureExtract import process_img
import os
import cv2
import time
from threading import Thread

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
        im_gray2 = cv2.imread(source_path+folder_2+'/'+img_name,  cv2.IMREAD_GRAYSCALE)
        mat1 = process_img(im_gray1)
        mat2 = process_img(im_gray2)
        cv2.imwrite(output_path+folder_1+'/'+img_name, mat1)
        cv2.imwrite(output_path+folder_2+ '/' + img_name, mat2)
        print("Processed:", str(img_name), "Time:", str(time.time()-start_time))




if __name__ == "__main__":
    source_path = "./resource/07/"
    output_path = "./output_resource_cython/07/"
    result = GenerateImage(source_path, output_path, start_from=423)