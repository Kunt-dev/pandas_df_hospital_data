import pandas as pd 
import numpy as np 
import os 


from kunt_df_generator import gene_celltype_df_builder, data_joiner, df_generator_expended

# Define the names of the files.
# All the files needs to be defined here. 
excelsheet_cluster = 'Clusters.xls'
excelsheet_brain_celltpye = 'NEW_brain_immune_vascular_celltypes_def.xlsx'

df_cluster = pd.read_excel(excelsheet_cluster, 
				sheet_name='cluster_beskrivelse_ex')

df_braincell = pd.read_excel(excelsheet_brain_celltpye)

# The specific columns are to be analysed. 
df_cluster_spfc = df_cluster[['Gene','Gene.full', 'Gene.type', 
				'Biological.processes', 'Tissue.spicificity',
				'Cell.specificity.cellular.location']]

# Loop through all the MS group files 
filepath_group = 'C:\\Users\\celeb\\Dropbox\\Kunt\\clusters\\MS vs CTRL group'
file_list_group = os.listdir(filepath_group)
os.chdir(filepath_group)

for excel_file in file_list_group: 
	# Read the excel files into python pandas dataframe. (Changing the Data)
	df_conserved = pd.read_excel(excel_file, sheet_name='Conserved')
	df_ms_up = pd.read_excel(excel_file, sheet_name='MS up')
	df_ms_down = pd.read_excel(excel_file, sheet_name='MS down')

	# Store the specific genes in a list from the group excel file 
	# In this case: conserved, ms up and ms down # A fuction can be defined. 
	genes_conserved = df_conserved.iloc[2:,0].unique()
	genes_ms_up = df_ms_up['Gene'].unique()
	genes_ms_down = df_ms_down['Gene'].unique()

	# The specific genes from the group are to be read in cluster 
	# Than those specific rows in cluster are to be copied to a new excel file 

	# Groups
	join_conserved=data_joiner(gene_list=genes_conserved,
		df_cluster=df_cluster, df_cluster_spfc=df_cluster_spfc)
	join_ms_up=data_joiner(gene_list=genes_ms_up,
		df_cluster=df_cluster, df_cluster_spfc=df_cluster_spfc)
	join_ms_down=data_joiner(gene_list=genes_ms_down,
		df_cluster=df_cluster, df_cluster_spfc=df_cluster_spfc)

	# Cell type 
	df_celltype_conserved = gene_celltype_df_builder(gene_list=genes_conserved,
		df_braincell=df_braincell)
	print(df_celltype_conserved)
	df_celltype_ms_up= gene_celltype_df_builder(gene_list=genes_ms_up,
		df_braincell=df_braincell)
	df_celltype_ms_down= gene_celltype_df_builder(gene_list=genes_ms_down,
		df_braincell=df_braincell)
	print(df_celltype_conserved)

	# Cell type expended
	filepath = 'C:\\Users\\celeb\\Dropbox\\Kunt\\clusters\\cell types_expanded'
	file_list_celltype_expanded = os.listdir(filepath)
	os.chdir(filepath)

	df_expended_conserved = df_generator_expended(
		gene_list=genes_conserved,file_list=
		file_list_celltype_expanded)

	df_expended_ms_up = df_generator_expended(
		gene_list=genes_ms_up,file_list=
		file_list_celltype_expanded)

	df_expended_ms_down = df_generator_expended(
		gene_list=genes_ms_down,file_list=
		file_list_celltype_expanded)
	
	#To write all the file in 1 new excel 
	outpath='C:\\Users\\celeb\\Dropbox\\Kunt\\clusters\\kunt_final\\'
	writer = pd.ExcelWriter(outpath +'kunt_' + str(excel_file))

	join_conserved.to_excel(writer, 
		sheet_name='Conserved', 
		index=False)
	df_celltype_conserved .to_excel(writer, 
		sheet_name='Conserved cell type', 
		index=False)

	df_expended_conserved.to_excel(writer,
		sheet_name='Conserved expended cell type',
		index=False)

	join_ms_up.to_excel(writer, sheet_name='MS up', index=False)
	df_celltype_ms_up.to_excel(writer, sheet_name='MS up cell type', index=False)
	df_expended_ms_up.to_excel(writer, sheet_name='MS up expended cell type',
		index=False)

	join_ms_down.to_excel(writer, sheet_name='MS down', index=False)
	df_celltype_ms_down.to_excel(writer, sheet_name='MS down cell type', index=False)
	df_expended_ms_up.to_excel(writer, sheet_name='MS down expended cell type',
		index=False)
	writer.save()
	
	os.chdir(filepath_group)