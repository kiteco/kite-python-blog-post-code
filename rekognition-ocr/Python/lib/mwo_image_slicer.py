import io
import os
from os import listdir
from os.path import isfile, join

import boto3
import pandas as pd
from PIL import Image, ImageFilter
import requests


class mwoImageSlicer(object):
	"""

	"""

	def __init__(self, boto_client):
		"""

		"""
		self.boto_client = boto_client
		self.image_folder = "../data/images/"
		self.download_folder = "../data/images/"
		self.data_save = "../output/df_from_img/"

		#horizontal slicing dimensions
		self.score_1680_1050 = [(565, 205, 1380, 230),
                                (565, 230, 1380, 255),
                                (565, 253, 1380, 280),
                                (565, 275, 1380, 300),
                                (565, 303, 1380, 325),
                                (565, 328, 1380, 350),
                                (565, 350, 1380, 372),
                                (565, 373, 1380, 395),
                                (565, 403, 1380, 425),
                                (565, 425, 1380, 450),
                                (565, 448, 1380, 470),
                                (565, 468, 1380, 492),
                                (565, 503, 1380, 525),
                                (565, 525, 1380, 549),
                                (565, 548, 1380, 572),
                                (565, 570, 1380, 595),
                                (565, 600, 1380, 620),
                                (565, 623, 1380, 645),
                                (565, 645, 1380, 665),
                                (565, 667, 1380, 689),
                                (565, 696, 1380, 719),
                                (565, 718, 1380, 740),
                                (565, 742, 1380, 762),
                                (565, 762, 1380, 789)]

        #Vertical slicing dimensions
        #these are the vertical coordinates for 1680 by 1050 resolution
        #(x_start, y_start, x_end, y_end)
        #FIXME: this won't work as the actual cropping is done from relative areas on non-standard image sizes
		self.score_parts_1680_1050 = {
							        	"clan_area":(0, 0, 915, 1050),
							        	"name_area":(50, 0, 1130, 1050),
							        	"mech_area":(265, 0, 1220, 1050),
							        	"status_area":(390, 0, 1330, 1050),
							        	"score_area":(500, 0, 1430, 1050),
							        	"kills_area":(590, 0, 1505, 1050),
							        	"assist_area":(650, 0, 1560, 1050),
							        	"dmg_area":(710, 0, 1640, 1050),
							        	"ping_area":(760, 0, 1680, 1050)
							         }

	def main(self, redo=False):
		"""
		Creates a list of all images in a directory
		Slices the images into cells
		Calls AWS Rekognition to get text for each image cell
		Compiles the cells into a dataframe
		Saves the dataframe

		Setting redo=True will repeat the process for images that have already been converted to dataframes
		"""
		#get list of images from directory
		img_list = self.get_files_in_folder()
		print(len(img_list), "images in folder")
		if not redo:
			df_files = self.get_files_in_folder(ext="txt", folder="../output/df_from_img/")
			df_files = [file[:-4] for file in df_files]
			img_list = [score for score in img_list if score[:-4] not in df_files]
			print(len(img_list), "remaining images to process")
		#loop over images
		for mwo_img in img_list:
			#open img with PIL
			img = self.load_image(mwo_img)
			#check image resolution
			if img.size != (1680, 1050):
				print("resizing image", mwo_img)
				#resize if needed, this is done to match the slicing pattern
				img = self.resize_image(img, new_width=1680)

			#convert to dataframe
			print("converting to dataframe {} of {}".format(img_list.index(mwo_img), len(img_list)))
			img_df = self.img_to_dataframe(img, mwo_img, save_df=True)
			

	def img_to_dataframe_h(self, img, save_img=False, resize=True, thresh=False, save_df=False, 
						save_name="test_df.txt", filepath=None):
		"""
		Uses AWS Rekognition to parse images from MWO screenshots
		Screenshots are split horizontal components (1 per player0 and resized before sending
		The resulting text is assembled into a dataframe that matches the MWO scorecard
		
		img is the image to be processed
		Setting thresh=True will greyscale by calling the grey_min_max() function to threshold each image before sending to AWS
		Setting save_df=True saves the resulting dataframe as a pipe-delimited text file
		Setting save_img=True will save the image slices to ../data/test_data/
		"""
		match_dict = {
						"clan":[],
						"name":[],
	            		"mech":[],
	            		"status":[],
	            		"score":[],
	            		"kills":[],
	            		"assists":[],
	            		"damage":[], 
	            		"ping":[]
		}

		print("horizontal slicing")
		h_slices = self.slice_image_horizontal(img)
		
		#save, resize, and threshold images if option was selected
		for i in range(len(h_slices)):
			if thresh: #threshold images prior to OCR
					h_slices[i] = self.grey_min_max(h_slices[i])
					
			#resizing images prior to OCR
			if resize:
				h_slices[i] = self.resize_image(h_slices[i], mode="height")
			
			if save_img:
					h_slices[i].save("../data/test_data/"+"h_slice"+str(i)+"_.jpg")
			
		for i in range(len(h_slices)):
			#get OCR for each image in player slice
			player_row_ocr_resp = self.get_image_ocr(img=h_slices[i], full_resp=True, size=False, show=False)
			
			#get words from OCR reponse JSON
			text_words = []
			for text_detected in player_row_ocr_resp["TextDetections"]:
				#Use only "Word" data from the TextDetections object
				if text_detected["Type"] == "WORD":
					text_words.append(text_detected["DetectedText"]) #list of words that should have positional alignment to the match_dict
			print()
			print(text_words)
			if len(text_words) == 9:
				match_dict["clan"].append(text_words[0])
				match_dict["name"].append(text_words[1])
				match_dict["mech"].append(text_words[2])
				match_dict["status"].append(text_words[3])
				match_dict["score"].append(text_words[4])
				match_dict["kills"].append(text_words[5])
				match_dict["assists"].append(text_words[6])
				match_dict["damage"].append(text_words[7])
				match_dict["ping"].append(text_words[8])
				
			elif len(text_words) == 8:
				print("incorrect number of words detected, attempting to omit clan and reposition")
				#omit clan data from match_dict as it is not required for a player to have a clan
				match_dict["clan"].append("NAN")
				match_dict["name"].append(text_words[0])
				match_dict["mech"].append(text_words[1])
				match_dict["status"].append(text_words[2])
				match_dict["score"].append(text_words[3])
				match_dict["kills"].append(text_words[4])
				match_dict["assists"].append(text_words[5])
				match_dict["damage"].append(text_words[6])
				match_dict["ping"].append(text_words[7])
			elif len(text_words) == 10:
				print("incorrect number of words detected, attempting to combine player name pieces")
				#combine 2nd and 3rd items. Assumption is that player name contained a space
				match_dict["clan"].append(text_words[0])
				match_dict["name"].append(text_words[1]+text_words[2])
				match_dict["mech"].append(text_words[3])
				match_dict["status"].append(text_words[4])
				match_dict["score"].append(text_words[5])
				match_dict["kills"].append(text_words[6])
				match_dict["assists"].append(text_words[7])
				match_dict["damage"].append(text_words[8])
				match_dict["ping"].append(text_words[9])
			elif len(text_words) == 11:
				print("incorrect number of words detected, attempting to combine player name pieces")
				#combine 2nd and 3rd items. Assumption is that player name contained a space
				match_dict["clan"].append(text_words[0])
				match_dict["name"].append(text_words[1]+text_words[2]+text_words[3])
				match_dict["mech"].append(text_words[4])
				match_dict["status"].append(text_words[5])
				match_dict["score"].append(text_words[6])
				match_dict["kills"].append(text_words[7])
				match_dict["assists"].append(text_words[8])
				match_dict["damage"].append(text_words[9])
				match_dict["ping"].append(text_words[10])

			else:
				print("text count does not match pattern, not adding to DF")
				print(text_words)

		print("converting to dataframe")
		#print(match_dict)
		match_df = pd.DataFrame.from_dict(match_dict)
		match_df = match_df[["clan", "name", "mech", "status", "score", "kills", 
							 "assists", "damage", "ping"]]
		if save_df:
			print("saving dataframe to", filepath, save_name)
			self.save_dataframe(match_df, save_name, filepath)

		return match_df


	def img_to_dataframe(self, img, save_img=False, resize=True, thresh=False, save_df=False, 
		filepath="../output/df_from_img/"):
		"""
		Uses AWS Rekognition to parse images from MWO screenshots
		Screenshots are split into single element components and resized before sending
		The resulting text is assembled into a dataframe that matches the MWO scorecard

		img is the image to be processed
		Setting thresh=True will greyscale by calling the grey_min_max() function to threshold each image before sending to AWS
		Setting save_df=True saves the resulting dataframe as a pipe-delimited text file
		Setting save_img=True will save the image slices to ../data/test_data/
		
		"""
		match_dict = {
						"clan":[],
						"name":[],
	            		"mech":[],
	            		"status":[],
	            		"score":[],
	            		"kills":[],
	            		"assists":[],
	            		"damage":[], 
	            		"ping":[]
		}
		print("horizontal slicing")
		h_slices = self.slice_image_horizontal(img)
		print("vertical slicing")
		for i in range(len(h_slices)):
			
			player_row_imgs = self.slice_image_vertical(h_slices[i])
			
			if save_img:
				for j in range(len(player_row_imgs)):
					player_row_imgs[j].save("../data/test_data/"+"player_img"+str(j)+"_"+str(i)+".jpg")
			#resize images prior to OCR
			if resize:
				for j in range(len(player_row_imgs)):
					player_row_imgs[j] = self.resize_image(player_row_imgs[j], mode="width")

			#threshold images prior to OCR
			if thresh:
				for j in range(len(player_row_imgs)):
					player_row_imgs[j] = self.grey_min_max(player_row_imgs[j])

			#get OCR for each image in player slice
			print("OCR runnin on slice {} of {}".format(i, len(h_slices)))
			match_dict["clan"].append(self.get_image_ocr(player_row_imgs[0])["text"])
			match_dict["name"].append(self.get_image_ocr(player_row_imgs[1])["text"])
			match_dict["mech"].append(self.get_image_ocr(player_row_imgs[2])["text"])
			#threshing the status column removes "dead" entries as those are shown in red
			match_dict["status"].append(self.get_image_ocr(player_row_imgs[3])["text"])
			match_dict["score"].append(self.get_image_ocr(player_row_imgs[4])["text"])
			match_dict["kills"].append(self.get_image_ocr(player_row_imgs[5])["text"])
			match_dict["assists"].append(self.get_image_ocr(player_row_imgs[6])["text"])
			match_dict["damage"].append(self.get_image_ocr(player_row_imgs[7])["text"])
			match_dict["ping"].append(self.get_image_ocr(player_row_imgs[8])["text"])

		print("converting to dataframe")
		match_df = pd.DataFrame.from_dict(match_dict)
		match_df = match_df[["clan", "name", "mech", "status", "score", "kills", 
							 "assists", "damage", "ping"]]
		if save_df:
			print("saving dataframe to ", filepath, self.image_name)
			self.save_dataframe(match_df, file_name=self.image_name, file_path=filepath)

		return match_df


	def save_dataframe(self, dataframe, file_name, file_path):
		"""
		Saves a dataframe to pipe-delimited text format
		"""

		if not file_path:
			file_path = self.data_save

		if not os.path.exists(file_path):
			os.makedirs(file_path)
		dataframe.to_csv(file_path+file_name[:-4] + ".txt", sep="|", index=False)


	def grey_min_max(self, img, min_grey=185):
		"""
		Sets all pixels below min_grey to black
		Sets all pixesl above min_grey to white
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


	def get_image_ocr(self, img, full_resp=False, show=False, size=False):
		"""
		Uses AWS Rekognition to get the text value from an image slice of a MWO screenshot
		This function only returns a single word (it was designed for getting text resonse from a single cell of an image)
		"""
		if show:
			img.show()
		if size:
			print(img.size)
		#convert image to byte array for use with AWS Rekognition API
		img_byte_arr = io.BytesIO()
		img.save(img_byte_arr, format='PNG')
		img_byte_arr = img_byte_arr.getvalue()

		response = self.boto_client.detect_text(Image={'Bytes': img_byte_arr})
		#limit return to first text read and confidence
		
		try:
			resp_text = {
							"text":response['TextDetections'][0]['DetectedText'],
							"confidence":response['TextDetections'][0]['Confidence']
						}
		except:
			#provide data for empty images
			resp_text = {
							"text":"",
							"confidence":0
			}
		if full_resp:
			return response
		else:
			return resp_text


	def download_images(self, url, download_folder):
		"""
		This does not currently function
		Downloads files from a target site
		"""

		grid_url = "https://steamcommunity.com/profiles/76561198090389241/screenshots/?appid=342200&sort=newestfirst&browsefilter=myfiles&view=grid"
#				    https://steamcommunity.com/profiles/76561198090389241/screenshots/?p=2&appid=342200&sort=newestfirst&browsefilter=myfiles&view=grid&privacy=14

		steam_mwo_url = "https://steamcommunity.com/profiles/76561198090389241/screenshots/?appid=342200"
		#steam image url:
		#https://steamuserimages-a.akamaihd.net/ugc/949601342893592988/26AACEA63DE6B2EB173C5FABF5766EE390BA31AA/
		#https://steamcommunity.com/sharedfiles/filedetails/?id=1664039570


	def show_image(self, img, folder="../data/images/"):
		"""
		Uses the PIL library to display an image
		"""
		print(type(img))

		if type(img) == str:
			img = Image.open(folder+img)

		img.show()


	def get_resolution(self, img_file, folder="../data/images/", display=False):
		"""
		Returns the weidth and height of an image
		"""

		img = Image.open(folder+img_file)
		if display:
			img.show()
		return img.size


	def get_files_in_folder(self, ext="jpg", folder="../data/images/"):
		"""
		Returns a list of files matching a passed extension in a specified folder 
		"""

		img_files = [file for file in listdir(folder) if isfile(join(folder, file))]
		img_files = [file for file in img_files if file[-3:]==ext]
		
		return img_files


	def load_image(self, image, folder_path="../data/images/"): #this might be unnecessary
		"""
		Stores an image file as a class data object for manipulation
		"""

		img = Image.open(folder_path+image)
		self.current_img = img
		self.image_name = image
		return img


	def resize_image(self, img, mode="width", new_base=300, print_size=False):
		"""
		Resizes an image while maintaining aspect ratio

		new_width is the new width of the image in pixels
		height will be set based on the aspect ratio and the passed width parameter
		"""
		if mode == "width":
			width_pct = (new_base / float(img.size[0])) #get new width as a percent of old width for aspect ratio 
			new_height = int((float(img.size[1])*float(width_pct))) #get new height based on new/old width percentage
			img = img.resize((new_base, new_height), Image.ANTIALIAS) #resize image: AWS OCR needs minimum of 80x80 pixels
			if print_size:
				print("new size", img.size)
			return img

		elif mode == "height":
			height_pct = (new_base / float(img.size[1]))
			new_width = int((float(img.size[0])*float(height_pct)))
			img = img.resize((new_width, new_base), Image.ANTIALIAS)
			if print_size:
				print("new size", img.size)
			return img

	def slice_image_horizontal(self, img, save_img=False):
		"""
			Cuts a MWO scorecard screen capture into 24 horizontal segments, 1 for each player
			These rectangles are further cut by slice_image_veritcal() before being sent to AWS Rekognition for OCR
			
			input: MWO match screenshot
			Returns a list of horizontal slices of the screenshot, 1 per player
		"""

		if img is not None:
           
        	#split image into 24 rectangles, 1 for each player
            #args are (x start, y start, x end, y end)
			if type(img) == str:
				img = Image.open(self.image_folder+img)
			
			w, h = img.size
			#winning team players are positions 1-12 (index 0-11)
			#losing team players are positions 13-24 (index 12-23)

			#FIXME: test image resizing for other resolutions 
			        #or create area maps for other resolutions

			player_images = [] #holds one image slice (horizontal bar) for each of the 24 players
			for player_area in self.score_1680_1050:
			    player_images.append(img.crop(player_area))
			    #img.crop(player_area).show()
			if save_img:
				for i in range(len(player_images)):
					player_images[i].save("../data/test_data/horizontal_slice_{}.jpg".format(str(i)))
			
			return player_images

		else:
			print("no image supplied")
		    

	def slice_image_vertical(self, img, sharpen=False):
		""" 
			Cuts a MWO scorecard image into single elements in preparation for OCR and aggregation of data.
			There are 24 players per match. 
			The following data elements will be captured for each player:
				- clan: string
            	- name: string
	            - mech: string
	            - status: string
	            - score: integer
	            - kills: integer
	            - assists: integer
	            - damage: integer
	            - ping: integer

	        input: a horizontal slice from slice_image_horizontal
	        return: a list of images containing the information listed above
		"""

		if img is not None:

            #load image for processing if one was passed
			if type(img) == str:
			    img = Image.open(img)

			if sharpen:
			    #sharpen image
			    img = img.filter(ImageFilter.SHARPEN)
			    
			image_slices = []
			w, h = img.size #get size of passed image, these are the horizontal slices of player data
			#image cropping uses relative mapping
			#get clan    x_start, y_start, x_end,   y_end
			clan_area = (3, 0, w-760, h)
			image_slices.append(img.crop(clan_area))
			#get player name
			name_area = (50, 0, w-550, h)
			image_slices.append(img.crop(name_area))
			#get mech
			mech_area = (265, 0, w-445, h)
			image_slices.append(img.crop(mech_area))
			#get status
			status_area = (390, 0, w-350, h)
			image_slices.append(img.crop(status_area))
			#get match score
			score_area = (500, 0, w-250, h)
			image_slices.append(img.crop(score_area))
			#get kills
			kills_area = (590, 0, w-175, h)
			image_slices.append(img.crop(kills_area))
			#get assists
			assist_area = (650, 0, w-120, h)
			image_slices.append(img.crop(assist_area))
			#get damage
			dmg_area = (710, 0, w-40, h)
			image_slices.append(img.crop(dmg_area))
			#get ping
			ping_area = (760, 0, w, h)
			image_slices.append(img.crop(ping_area))
		else:
			print("No image or area selected")

		return image_slices

