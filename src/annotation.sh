#!/usr/bin/env bash

input=$(realpath $1)
output=$(realpath $2)

# Returns a tsv with ENST | ENSG | SYMBOL | FPKM | TPM
grep ENS* ${input}| cut -f14,16,18,20,22,24 > ${output}