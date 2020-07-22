#useful functions

import os
from pyuvdata import UVData
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
import numpy.ma as ma


#plots all auto waterfall+line plots for the loaded file
def allauto_waterfall_lineplot (uv,colorbar_min, colorbar_max):
    
    for ant in uv.antenna_numbers:
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
        im = plt.imshow(np.abs(uv.get_data((ant,ant, uv.polarization_array[0]))),norm=colors.LogNorm(), 
                   vmin=colorbar_min, vmax=colorbar_max, aspect='auto')
        waterfall.set_title('Waterfall+Lineplot, Antenna '+str(ant))

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

        averaged_data= np.abs(np.average(uv.get_data((1,1, uv.polarization_array[0])),0))

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
        
        #plt.savefig('/lustre/aoc/projects/hera/amyers/gitrepos/monsterDetection/waterfalls/'+
        #            str(file)+'WF_LP_ant'+str(ant))
        plt.show()
        plt.close()
    return;

#plots a single waterfall+line plot for the given antenna and colorbar lims
def auto_waterfall_lineplot (uv,ant,colorbar_min, colorbar_max):
    
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
    im = plt.imshow(np.abs(uv.get_data((ant,ant, uv.polarization_array[0]))),norm=colors.LogNorm(), 
                vmin=colorbar_min, vmax=colorbar_max, aspect='auto')
    waterfall.set_title(str(file)+' Waterfall+Lineplot, Antenna '+str(ant))

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

    averaged_data= np.abs(np.average(uv.get_data((1,1, uv.polarization_array[0])),0))

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
        
    #plt.savefig('/lustre/aoc/projects/hera/amyers/gitrepos/monsterDetection/waterfalls/'+
    #                str(file)+'_WF_LP_ant'+str(ant))
    plt.show()
    plt.close()


#makes a lineplot every hour for the given antenna and loaded file
def every_hour_lineplot(uv,ant):

    freq = uv.freq_array[0]*1e-6
    times = np.unique(uv.time_array)

    fig = plt.figure(figsize=(20,20))

    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    #creating hour_array, which has times from time_array that are spaced ~ 1 hour apart 
    hour_arrange = np.arange(times[0],times[-1],(1/24))
    hour_array=[]
    for hour_value in hour_arrange:
        time = find_nearest(times,hour_value)
        hour_array.append(time)

    #setting up the structure of the subplots plots
    nhours = len(hour_array)
    cols = 3
    rows = nhours//cols +1
    i = 1

    #creating the plots
    for time in hour_array:

        plt.subplot(rows,cols,i)

        times_index = np.where(times == time)
        #np.where outputs a tuple. [0] pulls out a single number array, int makes it a number
        #which is not in an array
        times_index = int(times_index[0])

        dat = np.abs(uv.get_data((ant,ant,'xx'))[times_index])

        plt.plot(freq,dat)
        plt.title('Ant '+str(ant)+',  time = '+str(time))
        plt.yscale('log')
        plt.ylim((1e6,1e8))

        #add 1 to i
        i +=1

#mask the inputted array
def mask(uv,input_array):

    #this blocks out the entire ratio band.
    radio = np.array(np.arange(300,501,1))
    hand_picked = np.array([128,
                    640,
                    739,740,741,742,743,744,745,746,
                    810,811,844,845,
                    1117,1152,1166,1173,1174,1175,1176,1177,1178,1179,1180,1181,1182,
                        1183,1184,1185,1186,1187,1188,1189,1190,1191,1192,1193,1194,
                        1195,1196,1197,1198,1199,
                    1218,1219,1220,1231,1232,
                    1444,1445,1493,1494,
                    1510])
    idx=np.concatenate((radio,hand_picked))


    #creates masking array
    spike_mask = np.zeros_like(input_array)

    #tells the array which values to set to 1 (which values to mask out)
    spike_mask[:,idx]= 1

    #makes masked array without undesired values
    masked_data = ma.masked_array(input_array, spike_mask)
    return masked_data;

#plots a waterfall+line plot for the specified ant. uses the same mask as above.
def masked_auto_waterfall_lineplot (uv,ant,colorbar_min, colorbar_max):
    
    #creating the mask
    
    data_array = np.abs(uv.get_data((1, 1, uv.polarization_array[0])))
    
    #this blocks out the entire ratio band.
    radio = np.array(np.arange(300,501,1))
    hand_picked = np.array([128,
                640,
                739,740,741,742,743,744,745,746,
                810,811,844,845,
                1117,1152,1166,1173,1174,1175,1176,1177,1178,1179,1180,1181,1182,
                    1183,1184,1185,1186,1187,1188,1189,1190,1191,1192,1193,1194,
                    1195,1196,1197,1198,1199,
                1218,1219,1220,1231,1232,
                1444,1445,1493,1494,
                1510])
    idx=np.concatenate((radio,hand_picked))


    #creates masking array
    spike_mask = np.zeros_like(data_array)

    #tells the array which values to set to 1 (which values to mask out)
    spike_mask[:,idx]= 1

    #makes masked array without undesired values
    masked_data = ma.masked_array(data_array, spike_mask)
    
    
    
    
    #plotting the graphs
    
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
    im = plt.imshow(masked_data,norm=colors.LogNorm(), 
                vmin=colorbar_min, vmax=colorbar_max, aspect='auto')
    waterfall.set_title(str(file)+' Masked Waterfall+Lineplot, Antenna '+str(ant))

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

    #gets power averaged over time 
    masked_mean_data= ma.mean(masked_data,0)

    #used when i was trying to identify frequencies
    #creates 1d array of frequency indeces
    #freq_index= np.arange(0,uv.Nfreqs,1)
   # plt.plot(freq_index,powers_avg)
   # line.set_yscale('log')
    
    plt.plot(freq,masked_mean_data)
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
        
    #plt.savefig('/lustre/aoc/projects/hera/amyers/gitrepos/monsterDetection/waterfalls/'+
    #                str(file)+'_masked_WF_LP_ant'+str(ant))
    plt.show()
    plt.close()


#returns the array for the expected bandpass
def expected_bandpass(uv):
    good_curves = [uv.get_data((0,0, uv.polarization_array[0])),
                   uv.get_data((1,1, uv.polarization_array[0])),
                   uv.get_data((13,13, uv.polarization_array[0])),
                   uv.get_data((14,14, uv.polarization_array[0])),
                   uv.get_data((23,23, uv.polarization_array[0])),
                   uv.get_data((25,25, uv.polarization_array[0])),
                   uv.get_data((39,39, uv.polarization_array[0])),
                  ]
    good_curves = np.asarray(good_curves)
    print(good_curves.shape)
    average_curve= np.abs(np.average(good_curves,0))
    print(average_curve.shape)
    average_curve = mask(average_curve)
    return average_curve;

#plots a waterfall for a single auto
def singleauto_waterfall (uv, ant, colorbar_min, colorbar_max):
    
    fig = plt.figure(figsize=(15,12))
    
    

    #create time axis
    jd_ax=plt.gca()

    #there are a lot of redundancies in time_array, so to make sure that we have a list
    #of unique times to work with, we start off by making a new array... not doing this will
    #make things get messy. gave me a blank plot at first with a bunch of lines on the side
    #before i did this.
    times= np.unique(uv.time_array)

    #create the plot. uv.get_data will get data from specified antennas
    #colors.LogNorm() puts colors on log scale
    im = plt.imshow(np.abs(uv.get_data((ant,ant, uv.polarization_array[0]))),norm=colors.LogNorm(), 
           vmin=colorbar_min, vmax=colorbar_max, aspect='auto')
    plt.title('Auto_'+str(ant)+' Waterfall Plot')
    plt.xlabel('Frequency (MHz)')
    
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

    #pad moves colorbar farther from plot
    cbar = plt.colorbar(im, pad= 0.2)
    cbar.set_label('Power')


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
    
    plt.show()
    plt.close()
    return;

#plots a waterfall for every antenna in the file
def allauto_waterfall (uv,colorbar_min, colorbar_max):
    
    for ant in uv.antenna_numbers:
    
        fig = plt.figure(figsize=(15,12))
    
    

        #create time axis
        jd_ax=plt.gca()

        #there are a lot of redundancies in time_array, so to make sure that we have a list
        #of unique times to work with, we start off by making a new array... not doing this will
        #make things get messy. gave me a blank plot at first with a bunch of lines on the side
        #before i did this.
        times= np.unique(uv.time_array)

        #create the plot. uv.get_data will get data from specified antennas
        #colors.LogNorm() puts colors on log scale
        im = plt.imshow(np.abs(uv.get_data((ant,ant, uv.polarization_array[0]))),norm=colors.LogNorm(), 
           vmin=colorbar_min, vmax=colorbar_max, aspect='auto')
        plt.title('Auto_'+str(ant)+' Waterfall Plot')
        plt.xlabel('Frequency (MHz)')
        
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

        #pad moves colorbar farther from plot
        cbar = plt.colorbar(im, pad= 0.2)
        cbar.set_label('Power')


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
        
        plt.savefig('/lustre/aoc/projects/hera/amyers/gitrepos/monsterDetection/waterfalls/'+str(file)+
                    '_WF_ant'+str(ant))
        plt.show()
        plt.close()
    return;

