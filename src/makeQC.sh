#!/usr/bin/env bash

FASTQ="$1"
TRIM="${FASTQ%.fq.gz}.trim.fq"

nanoQC "$FASTQ" -o "${FASTQ%.fq.gz}.QC"
gunzip -c "$FASTQ" | NanoFilt -q 10 -l 500 --headcrop 120 --tailcrop 120 > ${FASTQ%.fq.gz}.trim.fq
nanoQC "$TRIM" -o "${TRIM%.fq}.QC"
gzip -f "$TRIM"