#!/usr/bin/env bash

for i in $(ls *counts*);do echo $i; cut -f1,7 $i | sed '1,2d' | sed s/\\.[0-9]// > ${i%.counts.tsv}.counts.processed.tsv;done