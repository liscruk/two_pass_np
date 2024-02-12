#!/usr/bin/env python3

import sys
import re
import os.path
from collections import defaultdict
from functools import reduce
import argparse
import pandas as pd
import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Process data output of rna seq') 
parser.add_argument('file', type=argparse.FileType('r'), nargs='+')
parser.add_argument('-t','--type',type=str,help ="Argument for what we are using [tpm] / [counts]")


args = parser.parse_args()

if args.type == 'tpm':

	fileNames = []
	files = []

	# Process all tpm files 
	for f in args.file:
		file = f.name
		basename = os.path.basename(file).split('.')[0]
		fileNames.append(basename)

		samp = pd.read_csv(f,sep="\t",index_col=0)
		samp = samp[["Gene Name","TPM"]]

		samp = samp.groupby(samp.index).agg({'Gene Name': 'first',"TPM":sum})

		samp = samp.filter(regex='ENSG.+',axis = 0)
		
		files.append(samp)

	out = reduce(lambda x,y: pd.merge(x,y,how="outer",left_index=True,right_index=True),files)

	gene_names = out.iloc[1:,0]
	
	out = out.filter(regex='TPM')
	out.columns = fileNames
	out = out.merge(gene_names,left_index=True,right_index=True)

	cols = out.columns.tolist()
	cols = cols[-1:] + cols[:-1]
	out = out[cols]
	out.rename(columns={"Gene Name_x":'Gene_Names'},inplace=True)
	out.to_csv(sys.stdout,sep="\t")
else:
	pass

if args.type == 'counts':

	fileNames = []
	files = []

	# Process all count files 
	for f in args.file:
		file = f.name
		basename = os.path.basename(file).split('.')[0]
		fileNames.append(basename)
		samp = pd.read_csv(f,header = None,sep="\t",skiprows=2,index_col=0)
		samp = samp[[6]]
		samp = samp.filter(regex='ENSG.+',axis = 0)
		files.append(samp)

	out = reduce(lambda x,y: pd.merge(x,y,left_index=True,right_index=True),files)
	out.columns = fileNames
	out.to_csv(sys.stdout,sep="\t",index_label='Gene ID')
else:
	pass

### This will only aggregate known transcripts
if args.type == 'transcripts':

	fileNames = []
	files = []
	defaultCols = ["Transcript","GeneID","Symbol","Coverage","FPKM","TPM"]
	
	for f in args.file:
		file = f.name
		basename = os.path.basename(file).split(".")[0]
		cols = [str(basename)+"-"+x for x in defaultCols]		
		fileNames.append(cols)
		samp = pd.read_csv(f,header=None,sep="\t")
		samp.columns = cols
		samp = samp.set_index(cols[0])

		files.append(samp)


	out = reduce(lambda x,y: pd.merge(x,y,how="outer",left_index=True,right_index=True),files)

	geneTable = out.filter(regex="Symbol")
	geneList = geneTable.bfill(axis=1).ffill(axis=1).iloc[:,0]

	idTable = out.filter(regex="GeneID")
	idList = idTable.bfill(axis=1).ffill(axis=1).iloc[:,0]

	out.iloc[:,0] = idList
	out.iloc[:,1] = geneList
		
	out = out.rename(columns={out.columns[0]: 'ID'})	
	out = out.rename(columns={out.columns[1]: 'GeneSymbol'})

	out.drop(list(out.filter(regex = '-GeneID')), axis = 1, inplace = True)
	out.drop(list(out.filter(regex = '-Symbol')), axis = 1, inplace = True)

	out = out.replace(np.nan,0)
	out.to_csv(sys.stdout,sep="\t",index_label='TranscriptID')
else:
	pass

if args.type == 'stats':

	fileNames = []
	files = []

	# Process all count files 
	for f in args.file:
		file = f.name
		basename = os.path.basename(file).split('.')[0] 
		fileNames.append(basename)

		samp = pd.read_csv(f,header = 0,sep="\t",index_col = 0)

		samp.drop(list(samp.filter(regex = 'Unnamed')), axis = 1, inplace = True)

		cols = samp.columns

		cols = [basename+"-"+x for x in cols]

		samp.columns = cols
		files.append(samp)

	out = reduce(lambda x,y: pd.merge(x,y,left_index=True,right_index=True),files)
	out.to_csv(sys.stdout,sep="\t",index_label='Metric')
else:
	pass

if args.type == 'salmon':

	colHeads = []
	files = []

	# Process all tpm files 
	for f in args.file:
		file = str(f.name)
		file = file.split("/")[-2]
		samp = pd.read_csv(f,sep="\t",index_col=0,header=0)

		cols = samp.columns.tolist()

		cols = [str(file)+"-"+x for x in cols]		

		colHeads.append(cols)
		samp.columns = cols

		files.append(samp)


	colHeads = [x for y in colHeads for x in y]
	
	out = reduce(lambda x,y: pd.merge(x,y,how="outer",left_index=True,right_index=True),files)
	out.columns = colHeads


	out.to_csv(sys.stdout,sep="\t")
else:
	pass
