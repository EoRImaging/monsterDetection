#!/bin/bash
#PBS -N test_py
#PBS -q hera
#PBS -l nodes=1:ppn=1
#PBS -l walltime=144:00:00
#PBS -l vmem=64g
#PBS -j oe
#PBS -o /lustre/aoc/projects/hera/amyers/out/test_py.out
#PBS -m be
#PBS -M pyxstar@uw.edu

# load python environment
source ~/.bashrc@
conda activate hera

# run python script
cd /lustre/aoc/projects/hera/amyers/gitrepos/monsterDetection/scripts/
python test_py.py
cd /lustre/aoc/projects/hera/amyers/
