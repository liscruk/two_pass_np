#!/usr/bin/env bash

input=$(realpath $1)
output=$(realpath $2)

sed '1d' ${input} | sed 's/"//g' | sed 's/;//g' | sed 's/\s/\t/g' | sed '/exon/d' > ${output}
