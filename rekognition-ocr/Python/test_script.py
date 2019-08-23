
import boto3
import io

from lib import mwo_image_slicer
from lib import mech_scrape
from lib import mwo_data_utils
import pandas as pd
#load mech variant weight data

#instantiate ocr client
client = boto3.client('rekognition')
#Scrape mech data from web and save as CSV files by weight class
mech_data_scraper = mech_scrape.mechScraper()
mech_data_scraper.main() #save mech variant web data to file
mech_info_df = pd.read_csv("../output/variant_weights.txt", sep="|") #load all variant weights

mwo_slicer = mwo_image_slicer.mwoImageSlicer(client)
mwo_scores = mwo_slicer.get_files_in_folder()

mwo_munger = mwo_data_utils.mwo_data_engine()
#mwo_munger.clean_20171118200711_1()
scores_df = mwo_munger.clean_20171118204451_1()
#scores_df = pd.read_csv("../output/cleaned_df_from_img/20171118200711_1.csv", sep="|")
#scores_df = mwo_munger.clean_mech_variants(scores_df)
joined_df = mwo_munger.combine_scores_with_scrape(scores_df, mech_info_df)
print(joined_df)

#joined_df.to_csv("../output/joint_test.txt", index=False, sep="|")
#test_df = mwo_slicer.img_to_dataframe(mwo_scores[3])
#imgs = mwo_slicer.get_images_in_folder(mwo_slicer.image_folder)
#sliced = mwo_slicer.slice_image_horizontal(imgs[0])
#print(test_df)
#print(mwo_slicer.is_downloadable("https://steamuserimages-a.akamaihd.net/ugc/949601342893592988/26AACEA63DE6B2EB173C5FABF5766EE390BA31AA/"))

#mwo_slicer.show_image(mwo_slicer.resize_image(img, new_width=1680))
#test_df = mwo_slicer.img_to_dataframe(mwo_slicer.resize_image(img, new_width=1680))
#print(test_df)
#mwo_slicer.main()

