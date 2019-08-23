import io
import json

import boto3
import numpy as np 
import pandas as pd
import requests
from PIL import Image, ImageFilter

from lib import mwo_image_slicer

client = boto3.client('rekognition') #instantiate AWS client

test_imgs_path = "E:/MWO/mwo_data/data/test_data/" #test images folder

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
		img.save("../../data/test_data/testpx.jpg")
	return img

#pass entire image to AWS and get result
print("opening image")
screenshot = Image.open("../data/images/20171118200711_1.jpg")
screenshot_arr = convert_to_byte_array(screenshot)
print("sending to API")
screenshot_ocr_resp = client.detect_text(Image={"Bytes":screenshot_arr})

print("writing JSON data to file")
with open("../output/blog_files/ocr_responses/full_screenshot_ocr_resp.json", "w") as outfile:
	json.dump(screenshot_ocr_resp, outfile)


text_line = []
text_words = []
for text_detected in screenshot_ocr_resp["TextDetections"]:
	#print(text_detected["DetectedText"])
	if text_detected["Type"] == "LINE":
		text_line.append(text_detected["DetectedText"])
	elif text_detected["Type"] == "WORD":
		text_words.append(text_detected["DetectedText"])

print("line text \n", text_line)
print("words text \n", text_words)