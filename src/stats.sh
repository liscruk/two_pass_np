#!/usr/bin/env bash


input=$(realpath $1)
output=$(realpath $2)

sed '1,4d' ${input} | sed '$ d' | sed -E 's/\s+/\t/g' > $output


