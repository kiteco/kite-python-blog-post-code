import boto3
import io
import json

import os
import numpy as np 
import pandas as pd
import requests
from PIL import Image, ImageFilter

from lib import mwo_image_slicer

client = boto3.client('rekognition') #instantiate AWS client

test_imgs_path = "E:/MWO/mwo_data/data/test_data/" #test images folder
if not os.path.exists("../output/blog_files/dataframes"):
    os.makedirs("../output/blog_files/dataframes")
    
def convert_to_byte_array(img):
	"""
	Converts an image file to a byte array for use with the 
	Rekognition API
	"""
	img_byte_arr = io.BytesIO()
	img.save(img_byte_arr, format='PNG')
	img_byte_arr = img_byte_arr.getvalue()
	return img_byte_arr

def grey_min_max(img, min_grey=185):
	"""

	"""
	img = img.convert("L")
	img_px = img.load()
	for i in range(img.size[1]):
		for j in range(img.size[0]):
			if img_px[j,i] < min_grey:
				img_px[j,i] = 0 
			else:
				img_px[j,i] = 255
		img.save("../data/test_data/testpx.jpg")
	return img

#instantiate image tools for project
print("loading image to slicer")
mwo_slicer = mwo_image_slicer.mwoImageSlicer(client) #handles image slicing and OCR requests
mwo_slicer.load_image(image="20171118200711_1.jpg") #set current image for handling


#create entire dataframe using cell splitting method
#no greyscale or threshing
ocr_df = mwo_slicer.img_to_dataframe(mwo_slicer.current_img, save_img=True, 
										thresh=False, save_df=True)

ocr_df.to_csv("../output/blog_files/dataframes/split_cell_df.txt", sep="|", index=False)
print(ocr_df)
print("saving DF results to text file")

#create entire dataframe using cell splitting method
#with greyscale and threshing
ocr_thresh_df = mwo_slicer.img_to_dataframe(mwo_slicer.current_img, save_img=True, 
										thresh=True, save_df=True)

print("saving threshed DF results to text file")
ocr_thresh_df.to_csv("../output/blog_files/dataframes/split_cell_threshed_df.txt", sep="|", 
						index=False)
print(ocr_thresh_df)
mwo_slicer.current_img.show()