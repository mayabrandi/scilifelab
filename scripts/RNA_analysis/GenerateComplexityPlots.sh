#! /bin/bash -l
#SBATCH -A a2012043 
#SBATCH -p core
#SBATCH -t 01:00:00
#SBATCH -J complexity
#SBATCH -e complexity.err
#SBATCH -o complexity.out

#by Pelin Akan pelin.akan@scilifelab.se
#Arguments GenerateComplexityPlots.sh

#Outputs a scatter plot of complexity curves of all samples in the project
#Requires ccurveplots.R 

space=" "
for files in `ls tophat_out_*/*.ccurve.txt | sort`; do filelist+=($files$space); done;

asize=${#filelist[@]}

Rscript /bubo/home/h24/mayabr/opt/scilifelab/scripts/RNA_analysis/ccurveplots.R ${filelist[@]} 
 







