#### Simple two pass mapping

A simple two pass mapping pipeline.
The pipeline is currently not super deployable but the dependencies are managable.
If you have issues let me know.

Dependencies in no particular order that should be in $PATH:
Snakemake
minimap2
samtools
nanoQC - if you want QC
salmon
R and tidyverse
Python3 with pandas,numpy,argparse
gffread & gffcompare 
RSeQC - particullary the script read_distribution.py!

Pipeline DAG:

![text83](https://github.com/liscruk/two_pass_np/assets/48765886/76e76934-887c-453c-b7c0-dc9d90e8a0ae)


