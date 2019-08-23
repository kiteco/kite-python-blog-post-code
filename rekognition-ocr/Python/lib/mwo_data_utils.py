import os
import pandas as pd

class mwo_data_engine(object):
	
	def __init__(self):
		"""
		"""
		self.mech_info_csv = "../output/variant_weights.txt"
		self.score_df_path = "../output/df_from_img/"
		self.clean_df_path = "../output/cleaned_df_from_img/"
		self.no_name_clean_path = "../output/no_name_data/"
		
		if not os.path.exists(self.no_name_clean_path):
			os.makedirs(self.no_name_clean_path)


	def combine_scores_with_scrape(self, scores_df, mech_info_df):
		"""
		Combines screenshot match data with mech variant, weightclass, and chassis web scrape
		"""
		if mech_info_df is None:
			mech_info_df = pd.read_csv(self.mech_info_csv, sep="|")

		#merge datasets to get tonnage, and weight class for each mech
		scores_and_weights = scores_df.merge(mech_info_df, how="left", left_on="mech", right_on="variant")
		return scores_and_weights

	def clean_mech_variants(self, scores_df):
		"""
		Fixes bad OCR results in the mech name column

		"""
		#use dictionary to map bad read to actual
		print("pre-changes \n", scores_df)
		mech_name_map = {
		"-BW":"WHM-BW",
		"KGC-O00B":"KGC-000B",
		"UM- -R68(L)":"UM-R68(L)",
		"CTF-3 F-3D(C)":"CTF-3D(C)",
		"STK-3F(C) STK-3":"STK-3F(C)",
		"KGC-000(L) KGC-O": "KGC-000(L)",
		"DWF-PRIMI":"DWF-PRIME",
		"CRB- RB-27(R)":"CRB-27(R)",
		"ACW-PRIMI":"ACW-PRIME",
		"ACH-PRIME H-PRIME":"ACH-PRIME",
		"MAD-I1C-A":"MAD-IIC-A",
		"KFX- FX-G(L)":"KFX-G(L)",
		"MAL-1R(R) MAL-":"MAL-1R(R)",
		"HMN-PRIM":"HMN-PRIME",
		"TNS- NS-4S(S)":"TNS-4S(S)",
		"VA-PRIME":"NVA-PRIME"
		}

		#test with pandas map to column
		for mech in mech_name_map.keys():
			if mech in list(scores_df.mech):
				scores_df.at[scores_df.index[scores_df.mech==mech], "mech"] = mech_name_map[mech]

		number_cols = ["kills", "assists", "damage", "ping"]
		for col in number_cols:
			scores_df[col] = scores_df[col].apply(lambda x: str(x).replace("O", "0"))
			scores_df[col] = scores_df[col].apply(lambda x: str(x).replace("nan", "0"))
			scores_df[col] = scores_df[col].apply(lambda x: x.split(" ")[-1])
		#general rule: last entry in OCR number is correct if multiples are supplied
		#multiples occur with spaces, split on space and take last in list
		
		return scores_df


	def clean_20171118200711_1(self):
		"""
		Cleans the image 20171118200711_1.txt
		These modifications are to correct errors in the OCR return that cannot be done to all images 
		"""
		bad_df = pd.read_csv(self.score_df_path+"20171118200711_1.txt", sep="|")
		bad_df = self.clean_mech_variants(bad_df)
		bad_df.at[18, "mech"] = "TBR-PRIME" #change -PRIME to TBR-PRIME
		bad_df.at[0, "kills"] = 4 #change row 0 kills to 4
		bad_df.at[1, "kills"] = 2 #change row 1 kills to 2
		bad_df.at[3, "kills"] = 2 #change row 3 kills to 2
		#fill NAN with 0
		bad_df.fillna(0, inplace=True)
		bad_df.to_csv(self.clean_df_path+"20171118200711_1.csv", index=False, sep="|")


	def clean_20171118202707_1(self):
		"""
		"""
		bad_df = pd.read_csv(self.score_df_path+"20171118202707_1.txt", sep = "|")
		bad_df = self.clean_mech_variants(bad_df)
		bad_df.at[3, "kills"] = 1 #change row 3 kills to 1
		bad_df.at[22, "kills"] = 1 #change row 22 kills to 1
		bad_df.at[23, "kills"] = 1 #change row 23 kills to 1
		bad_df.at[0, "assists"] = 1 #change row 0 assists to 1
		bad_df.at[2, "assists"] = 1 #change row 2 assists to 1
		bad_df.at[4, "assists"] = 1 #change row 4 assists to 1
		bad_df.at[5, "assists"] = 1 #change row 5 assists to 1
		bad_df.at[6, "assists"] = 1 #change row 6 assists to 1
		bad_df.at[10, "assists"] = 1 #change row 10 assists to 1
		bad_df.at[11, "assists"] = 1 #change row 11 assists to 1
		bad_df.at[16, "assists"] = 1 #change row 16 assists to 1
		bad_df.at[18, "assists"] = 1 #change row 18 assists to 1
		bad_df.at[15, "mech"] = "TNS-5P" #set row 15 TNS-5 to TNS 5P
		bad_df.at[2, "mech"] = "BJ-1DC" #set row 2 to BJ-1DC
		return bad_df

	def clean_20171118203637_1(self):
		"""
		"""

		bad_df = pd.read_csv(self.score_df_path+"20171118203637_1.txt", sep="|")
		bad_df = self.clean_mech_variants(bad_df)
		bad_df.at[22, "mech"] = "TNS-5S" #set row 22 mech to TNS-5S
		bad_df.at[1, "kills"] = 1 #set row 1 kills to 1
		bad_df.at[3, "kills"] = 1 #set row 4 kills to 1
		bad_df.at[3, "assists"] = 5 #set row 4 assists to 5
		bad_df.at[4, "assists"] = 1
		bad_df.at[15, "assists"] = 1 
		return bad_df

	def clean_20171118204451_1(self):
		"""
		"""
		bad_df = pd.read_csv(self.score_df_path+"20171118204451_1.txt", sep="|")
		bad_df = self.clean_mech_variants(bad_df)
		bad_df.at[22, "kills"] = 1
		bad_df.at[8, "assists"] = 4
		bad_df.at[10, "assists"] = 4
		bad_df.at[11, "assists"] = 1
		bad_df.at[12, "assists"] = 1
		bad_df.at[13, "assists"] = 1
		bad_df.at[14, "assists"] = 1
		bad_df.at[17, "assists"] = 1
		bad_df.at[18, "assists"] = 1
		bad_df.at[19, "assists"] = 1		
		bad_df.at[20, "assists"] = 1
		bad_df.at[21, "assists"] = 1
		bad_df.at[23, "assists"] = 1	
		bad_df.at[10, "mech"] = "NVA-PRIME"	
		bad_df.at[8, "mech"] = "NVA-PRIME"
		return bad_df