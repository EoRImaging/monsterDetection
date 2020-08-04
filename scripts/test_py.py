import os
from pyuvdata import UVData
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
import numpy.ma as ma
import sys

file=2458851
uv = UVData()
uv.read('/lustre/aoc/projects/hera/pstar/autos/'+str(file)+'_autos_sum.uvh5')


freq = uv.freq_array[0]*1e-6
fig = plt.figure(figsize=(20,20))

#can use gridspec instead of saying add_subplot(1,2,1) etc
gs = gridspec.GridSpec(2, 1, height_ratios=[2,1]) 

#creates waterfall subplot
waterfall= plt.subplot(gs[0])
    
#create time axis
jd_ax=plt.gca()

#there are a lot of redundancies in time_array, so to make sure that we have a list
#of unique times to work with, we start off by making a new array... not doing this will
#make things get messy. gave me a blank plot at first with a bunch of lines on the side
#before i did this.
times= np.unique(uv.time_array)

#create the plot. uv.get_data will get data from specified antennas
#colors.LogNorm() puts colors on log scale
im = plt.imshow(np.abs(uv.get_data((86,86, uv.polarization_array[0]))),norm=colors.LogNorm(), 
            vmin=0.3*10e6, vmax=0.3*10e7, aspect='auto')
waterfall.set_title(str(file_number)+' Waterfall+Lineplot, Antenna '+str(86))

# get an array of frequencies in MHz
freqs = uv.freq_array[0, :] / 1000000
xticks = np.arange(0, len(freqs), 120)
plt.xticks(xticks, labels =np.around(freqs[xticks],2))

jd_ax.set_ylabel('JD Time (days)')

#makes equally spaced ticks in increments of 100. since we are assuming time is pretty
#continuous, this will cover all times pretty well if we go from 0 to the length 
jd_yticks = np.arange(0,len(times),100)
#set_yticks takes a List of y-axis tick locations. its purpose is to set tick locations
jd_ax.set_yticks(jd_yticks)
#this function actually determines what the tickmarks will say.
jd_ax.set_yticklabels(np.around(times[jd_yticks],2))


#create second axis
lst_ax = jd_ax.twinx()
lst_ax.set_ylabel('LST Time (hour of the day)')

#lst_array is in radians, and we want it in *hours*.. rad*180/pi = degrees
#one hour= 15 degrees
lst_hours = (uv.lst_array*(180/np.pi))/(15)

#creates array of unique lsts
lsts= lst_hours.reshape(uv.Ntimes,uv.Nbls)
lsts = lsts[:,0]

#set the ticks of the lst axis to match the lst_array in hours
lst_yticks = np.arange(0,len(lsts),100)
lst_ax.set_yticks(lst_yticks)
lst_ax.set_yticklabels(np.around(lsts[lst_yticks],2))

#gives the lst_axis information about the jd_axis. stuff like the y-dimension of the data. 
#gets the axes to line up properly. will make it so that the tick-marks lining up, and the 
#zeroth entry of times[jd_yticks] lining up with the zeroth entry of lsts[lst_yticks]
lst_ax.set_ylim(jd_ax.get_ylim())

#makes it so that the second axis does not alter the structure of the figure
jd_ax.autoscale(False)
lst_ax.autoscale(False)

#creates line subplot and positions it according to gs[1]
line= plt.subplot(gs[1])

#drawing faint grey lines at boundaries
if boundaries == True:
    channel_boundaries = [192,384,576,768,960,1152,1344]

    freq_boundaries = []
    for channel in channel_boundaries:
        freq_boundary = freq[channel]
        freq_boundaries.append(freq_boundary)
        
        
    plt.axvline(freq_boundaries[0],0,1, color = '0.8')
    plt.axvline(freq_boundaries[1],0,1, color = '0.8')
    plt.axvline(freq_boundaries[2],0,1, color = '0.8')
    plt.axvline(freq_boundaries[3],0,1, color = '0.8')
    plt.axvline(freq_boundaries[4],0,1, color = '0.8')
    plt.axvline(freq_boundaries[5],0,1, color = '0.8')
    plt.axvline(freq_boundaries[6],0,1, color = '0.8')

averaged_data= np.abs(np.average(uv.get_data((ant,ant, uv.polarization_array[0])),0))

plt.plot(freq,averaged_data)
line.set_yscale('log')
line.set_xlabel('Frequency (MHz)')
line.set_ylabel('Power')
#sets the range of the graph to be the same range as waterfall plot
line.set_xlim(freq[0],freq[-1])


#makes waterfall x ticks invisible
plt.setp(waterfall.get_xticklabels(), visible=False)

#brings plots together
plt.subplots_adjust(hspace=.0)


#pad moves colorbar farther from plot
cbar = plt.colorbar(im, pad= 0.15, orientation = 'horizontal')
cbar.set_label('Power -->')

save=True

if save== False:
    print('Fig not saved to file')
elif save == True:
    plt.savefig('/lustre/aoc/projects/hera/amyers/out/'+
                    str(file_number)+'_WF_LP_ant'+str(ant))
    print('Fig saved to file')
plt.show()
plt.close()
