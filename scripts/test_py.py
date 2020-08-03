from util_copy import *
import sys

file=2458851
uv = UVData()
uv.read('/lustre/aoc/projects/hera/pstar/autos/'+str(file)+'_autos_sum.uvh5')

auto_waterfall_lineplot (uv, file, 86,0.3*10e6, 0.3*10e7)