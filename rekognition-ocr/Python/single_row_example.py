import io
import json

import boto3
import numpy as np 
import os
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

#cut and save horizontal image slices to ../data/test_data/
print("slicing image horizontally and saving slices to ../data/test_data/")
h_slices = mwo_slicer.slice_image_horizontal(mwo_slicer.current_img, save_img=True) 

#pass single horizontal slice of the screenshot to AWS and get result
#the example blog uses row 1
horizontal_slice = Image.open("../data/test_data/horizontal_slice_1.jpg")
horizontal_slice_arr = convert_to_byte_array(horizontal_slice)
horizontal_slice_ocr_resp = client.detect_text(Image={"Bytes":horizontal_slice_arr})

print("writing JSON response to file")
with open("../output/blog_files/ocr_responses/single_line_ocr_resp.json", "w") as outfile:
	json.dump(horizontal_slice_ocr_resp, outfile)

#get detected words from OCR response
text_line = []
text_words = []
for text_detected in horizontal_slice_ocr_resp["TextDetections"]:
	#print(text_detected["DetectedText"])
	if text_detected["Type"] == "LINE":
		text_line.append(text_detected["DetectedText"])
	elif text_detected["Type"] == "WORD":
		text_words.append(text_detected["DetectedText"])
print()
print("line text \n", text_line)
print("words text \n", text_words)
#add line spacing for terminal output
print()
print()

#greyscale and threshold horizontal image
print("converting image to greyscale and threshing")
horizontal_slice_grey = grey_min_max(horizontal_slice)
horizontal_slice_grey_arr = convert_to_byte_array(horizontal_slice_grey)
horizontal_slice_grey_ocr_resp = client.detect_text(Image={"Bytes":horizontal_slice_grey_arr})

print("writing JSON response to file")
with open("../output/blog_files/ocr_responses/single_line_grey_ocr_resp.json", "w") as outfile:
	json.dump(horizontal_slice_grey_ocr_resp, outfile)

#get detected words from OCR response
text_line_grey = []
text_words_grey = []
for text_detected in horizontal_slice_grey_ocr_resp["TextDetections"]:
	#print(text_detected["DetectedText"])
	if text_detected["Type"] == "LINE":
		text_line_grey.append(text_detected["DetectedText"])
	elif text_detected["Type"] == "WORD":
		text_words_grey.append(text_detected["DetectedText"])

print()
print("line text after greyscale and threshold \n", text_line_grey)
print("words text after greyscale and threshold \n", text_words_grey)

print("showing image before and after grey scale and threshold modifications")
horizontal_slice.show()
horizontal_slice_grey.show()

#add line spacing for terminal output
print()
print()
print("*"*50) #show delineation of single line vs full dataframe results
print("Creating full dataframe from horizontal screenshot slices")

#create entire dataframe using horizontal slices
#no greyscale or threshing
horizontal_slice_df = mwo_slicer.img_to_dataframe_h(mwo_slicer.current_img, save_img=True, 
	thresh=False, save_df=True, save_name="h_method_df.txt", filepath="../output/blog_files/dataframes/")
print(horizontal_slice_df)
print()
print("*"*50)
print("Creating full dataframe from horizontal screenshot slices using threshing method")

#create entire dataframe using horizontal slices
#with greyscale and threshing
horizontal_slice_thresh_df = mwo_slicer.img_to_dataframe_h(mwo_slicer.current_img, save_img=True, 
	thresh=True, save_df=True, save_name="h_method_threshed_df.txt", filepath="../output/blog_files/dataframes/")
print(horizontal_slice_thresh_df)

## Construct entire dataframe: first without resize and thresholding, second with resize and thresholding