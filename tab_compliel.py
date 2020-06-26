import pandas as pd 
import numpy as np 
import os 

# The tabs for expended will be combined here 

# Making a list of excel files 
filepath_sorted = 'C:\\Users\\celeb\\Dropbox\\Kunt\\clusters\\kunt_final'
file_list = os.listdir(filepath_sorted)
file_list.pop(0)
file_list.pop(-1)

for file in file_list:
	
	df_con= pd.read_excel(file, sheet_name='Conserved')
	df_ct_con_1 = pd.read_excel(file, sheet_name='Conserved cell type')
	df_ct_con_2 = pd.read_excel(file, sheet_name='Conserved expended cell type')


	df_up= pd.read_excel(file, sheet_name='MS up')
	df_ct_up_1 = pd.read_excel(file, sheet_name='MS up cell type')
	df_ct_up_2 = pd.read_excel(file, sheet_name='MS up expended cell type')


	df_down= pd.read_excel(file, sheet_name='MS down')
	df_ct_down_1 = pd.read_excel(file, sheet_name='MS down cell type')
	df_ct_down_2 = pd.read_excel(file, sheet_name='MS down expended cell type')

	#
	df_ct_con =pd.concat([df_ct_con_1,df_ct_con_2],axis=1).drop('gene',axis=1)
	df_ct_up= pd.concat([df_ct_up_1,df_ct_up_2],axis=1).drop('gene',axis=1)
	df_ct_down = pd.concat([df_ct_down_1,df_ct_down_2],axis=1).drop('gene',axis=1)
	#

	
	#
	outpath = 'C:\\Users\\celeb\\Dropbox\\Kunt\\clusters\\FINAL\\'
	writer = pd.ExcelWriter(outpath + str(file))
	#

	#
	df_con.to_excel(writer, 
			sheet_name='Conserved', index=False)

	df_ct_con.to_excel(writer, 
			sheet_name='Conserved cell type', index=False)
	#

	df_up.to_excel(writer, sheet_name='MS up', index=False)
	df_ct_up.to_excel(writer, sheet_name='MS up cell type', index=False)

	df_down.to_excel(writer, sheet_name='MS down', index=False)
	df_ct_down.to_excel(writer, sheet_name='MS down cell type', index=False)

	writer.save()

