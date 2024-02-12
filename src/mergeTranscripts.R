#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

library(tidyverse)

files = list.files(pattern="*.transcripts.tsv")
samples = lapply(files,basename)
data = lapply(files,read.table,)
data = reduce(data,full_join,"V1")

data = cbind(data[,1],data[,seq(6,ncol(data),by = 5)])
files = gsub('.transcripts.tsv','-TPM',files,perl=TRUE)
files = append(c("TranscriptID"),files)
colnames(data) = files
data[is.na(data)] = 0
data = aggregate(data[,-1], list(data[,'TranscriptID']), FUN = sum)

cat(format_delim(data,delim = "\t"))
