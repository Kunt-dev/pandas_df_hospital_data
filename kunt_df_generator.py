import pandas as pd 
import numpy as np
import os

def gene_celltype_df_builder(gene_list,df_braincell):
	"""This fuction is building a gene dictionary"""
	gene_dict = {}
	for gene in gene_list:
		cell_type_list =[]
		for i in list(range(len(df_braincell.columns))):
			if gene in df_braincell.iloc[:,i].unique():
				cell_type = df_braincell.columns[i]
				cell_type_list.append(cell_type)
				gene_dict[gene] = list(dict.fromkeys(cell_type_list))
			else: 
				cell_type_list.append('')
				gene_dict[gene] = list(dict.fromkeys(cell_type_list))		
	
	#middle step to make one column
	"""This fuction combines the values of a dictinary, if the values are 
	a list. So the list becomes one string"""
	for gene, cell_type in gene_dict.items():
		# For example 'CRYAB' is in the loop 
		gene_dict[gene]=', '.join(cell_type)

	"""Now building a dataframe to be able use it as excel"""	
	df = pd.DataFrame.from_dict(gene_dict,
		orient='index',
		columns=['Cell type'])

	#genes had to be repeated becuase the genes are indexed for the dataframe
	manupulate_dict={}
	for gene in gene_list:
		manupulate_dict[gene] = gene

	df_gene_manupulated = pd.DataFrame.from_dict(manupulate_dict,
		orient='index',
		columns=['Gene'])
	#This had to be made inorder to use the concat fuction with the same index

	df_all = pd.concat([df_gene_manupulated,df],axis=1)

	return df_all

def data_joiner(gene_list,df_cluster,df_cluster_spfc):
	"""This function joins the rows with the given columns above"""
	appended_data = []
	gene_not_cluster = []

	for gene in gene_list:
		if gene not in df_cluster['Gene'].unique():
			gene_not_cluster.append(gene)

	df_not_in_cluster = pd.DataFrame({'Gene':gene_not_cluster}, 
			columns=['Gene'], 
			index=list(range(len(gene_not_cluster))))

	for gene in gene_list: 
		df_kunt_gene = df_cluster_spfc[df_cluster_spfc['Gene'] == gene]
		appended_data.append(df_kunt_gene) 

	if appended_data != []: 
		joined_df = pd.concat(appended_data).drop_duplicates().append(df_not_in_cluster)
	else: 
		joined_df = pd.DataFrame()
	
	return joined_df

def df_generator_expended(gene_list, file_list):
	
	# Create an empthy dictionary 
	manupulate_dict={} 
	for gene in gene_list: # same structure with the other dataframe 
		manupulate_dict[gene] = [] #emppthy list to append the wanted cell tpyes

	for excel_file in file_list: #excell file list is stored in the same dir
		df_celltype_expended = pd.read_excel(excel_file)

		data = {'Cell Type': df_celltype_expended.iloc[1:,0],
					'Gene': df_celltype_expended.iloc[1:,1]}

		df = pd.DataFrame(data) #Create a new dataframe with the correct structure

		gene_list_expended = df['Gene'].unique() #make a list from the df

		gene_dict_expended={} #make dcitornary and split the cell types 
		for i in range(len(df['Gene'].unique())):
			gene_row_list = gene_list_expended[i].replace(",","").split()
			for gene in gene_row_list:
				gene_dict_expended[gene]=str(df.iloc[i,0])

		detected_genes_dict={} #some genes will be detected, now new dictionary
		for gene, cell_type in gene_dict_expended.items():
			if gene in gene_list:
				detected_genes_dict[gene]=cell_type

		for gene in gene_list:
			if gene in detected_genes_dict.keys():
				manupulate_dict[gene].append(detected_genes_dict[gene])

	# Now making the dictionary into df . combining the list back to one cell
	# in excel 
	for gene, cell_type_list in manupulate_dict.items():
		manupulate_dict[gene]= ', '.join(cell_type_list)

	# building the dataframe from the dictionary

	df = pd.DataFrame.from_dict(manupulate_dict,
		orient='index',
		columns=['Cell type expnaded'])

	#genes had to be repeated becuase the genes are indexed for the dataframe
	exp_dict_only_genes={}
	for gene in gene_list:
		exp_dict_only_genes[gene] = gene

	df_only_gene = pd.DataFrame.from_dict(exp_dict_only_genes,
		orient='index',
		columns=['gene'])
	#This had to be made inorder to use the concat fuction with the same index

	df_all = pd.concat([df_only_gene,df],axis=1)

	return df_all 




