#monster traps for UW HERA
#these have not been fully tested yet
#note, i think that periodic spikes and spikes at high frequency look like the same monster.

#files to import
from util import *
from sklearn.linear_model import LinearRegression
import scipy.signal
import scipy.stats



#Adele's function for catching xeng monster
#runs through antennas in a data file and tells whether there is an xengine failure for that ant.
#evens are zero when xengine fails, so this checks to see if evens are zero within the boundaries of an xeng.

def xeng_trap (uvsum, uvdiff):

    #frequency channels. these are the channels at the borders of each xengine.
    boundaries = [0,192,384,576,768,960,1152,1344]

    #prints whether each antenna has an xengine failure
    for ant in uv.antenna_numbers:
        tearMonster=False
        datasum = (uvsum.get_data(ant,ant,'xx'))
        datadiff = (uvdiff.get_data(ant,ant,'xx'))
        evens = np.abs((data2sum+data2diff)/2)

        for boundary in boundaries:
            
            #the maximum even value within a given xengine
            max= np.max(evens[:,boundary:boundary+192])

            if max == 0:
                tearMonster = True

        print(str(ant)+ ' = '+str(tearMonster))


#Adele's function for catching "antennas with no node mapping" monster
#couldnt find an antenna to test this on, but i think it would work
#makes an array of the numerical difference between each point
#the max numerical difference for the *expected bandpass* was 42659668.85714285, so i will say that if 
#the diff between any two consecutive points is >100000000 (1e8) (gives room for very large RFI) then we 
#have a node mapping failure (diff "cutoff" can be adjusted)

#prints whether each ant in uv has a node mapping problem
def nodemap_trap (uv):

    for ant in uv.antenna_numbers:

        nodefail = False

        #only doing 'xx' polarization for now, but this can be altered.
        data = np.abs(uv.get_data(ant, ant, 'xx')[0])

        diff_array = []

        #current index of average_power array
        power_index = 0

        #builds diff_array
        for power in data:
            #makes sure that diff is not calculated for last value in average_power.
            if power_index != len(data)-1:
                diff = data[power_index+1]-power
                diff_array.append(diff)

            power_index +=1

        if np.max(diff_array) > 1e8:
            nodefail=True

        print(str(ant)+ ' = '+str(nodefail))

    
#Adele's function for catching nosky and high frequency ripple
#when an antenna does not see the sky (or when it has a high frequency ripple monster) it does not see the rfi band. 
#so we can calculate diffs for each point, and 
#if there are no diffs larger than 1e6, then the antenna does not see the rfi band.

#prints a list of antennas with nosky monster and a list of antennas with ripple monster
def nosky_ripple_trap(uv):

    nosky=[]
    ripple=[]

    for ant in uv.antenna_numbers:

        
        data = np.abs(uv.get_data(ant, ant, 'xx')[0])

        average_data = np.average(data)
        median_data = np.median(data)

        #average data will filter out antennas with no data at all
        #median_data will catch the antennas with mostly no data, but with a few spikes.
        if average_data != 0 and median_data !=0:

            diff_array = []

            #current index of average_power array
            power_index = 0

            #builds diff_array
            for power in data:
                #makes sure that diff is not calculated for last value in average_power.
                if power_index != len(data)-1:
                    diff = data[power_index+1]-power
                    diff_array.append(diff)

                power_index +=1

            #creates an array of the spikes in the fm radio band
            fm_diff_array= diff_array[300:501]
            spikes=[]
            for diff in fm_diff_array:
                if diff > 1e6:
                    spikes.append(diff)
                    
        

            #if there are no spikes in the fm radio band, antenna does not see the sky
            #this could either be caused by the "nosky" monster or the high frequency ripple monster
            #The fm band produces around 20 spikes here, so if there are <5, the ant does not see the fm band
            if len(spikes) < 5:
                
                peaks=scipy.signal.find_peaks(data,prominence =1e6)

                peak_channels = peaks[0]
                
                #high frequency ripple has many detectable peaks at this prominence level because of its 
                #oscillating nature
                #but nosky does not have many becasue it is just flat. the only prominant peaks come
                #from the hera clock and maybe from the periodic spikes.
                if len(peak_channels) > 10:
                    ripple.append(ant)
                    
                    
                else:
                    nosky.append(ant)
                    
    print('High Frequency Ripple Antennas: ')
    print(ripple)
    print('')
    print('No Sky Antennas: ')
    print(nosky)
            

#Adele's function for catching zero flatline spike monster
#zero flatline with spikes
#this monster also does not see the sky, but has a median 0 value and an average nonzero value.

def zero_flatline_spike (uv):

    for ant in uv.antenna_numbers:

        #we already know that antenna 2 is messed up
        if ant!=2:

            flatline_spike=False

            data = np.abs(uv.get_data(ant, ant, 'xx')[0])

            average_data = np.average(data[300:501])
            median_data = np.median(data)

            #this monster has average data!=0 and median_data=0
            #but we have to filter for more than that because there are a lot of other 
            #monsters that just so happen to also have average!=0 median=0
            #so we have to also check for spikes (which this monster does not have)
            if average_data != 0 and median_data ==0:

                diff_array = []

                #current index of average_power array
                power_index = 0

                #builds diff_array
                for power in data:
                    #makes sure that diff is not calculated for last value in average_power.
                    if power_index != len(data)-1:
                        diff = data[power_index+1]-power
                        diff_array.append(diff)

                    power_index +=1

                fm_diff_array= diff_array[300:501]

                spikes=[]
                for diff in fm_diff_array:
                    if diff > 1e6:
                        spikes.append(diff)


                if len(spikes)==0:
                    monster_data.append(data)
                    flatline_spike=True

                    #if antenna has the monster, print that it has the monster.
                    print('Ant  '+str(ant)+', flatline_spike  '+str(flatline_spike))


#Adele's function for catching intermod and comb (separately identified.)
#if we eventually want to do statistics, we can make a "total_intermod_spikes" array, a total_comb_spikes array
#and a total_early_spikes array that records the number of spikes of each type for each antenna, and you can
#do statistics on all the monster free antennas.

#catches intermod and flat/comb
def intermod_comb_trap(uv):
    
    for ant in uv.antenna_numbers:
        
        intermod_monster= False
        comb_monster=False
    
        data = np.abs(uv.get_data(ant,ant,'xx'))[0]

        freq=uv.freq_array[0]*1e-6


        #in testing, prominence can be toggled with to adjust the sensitivity of the peak detection.
        peaks=scipy.signal.find_peaks(data,prominence =1e6)

        #this is an array of channels where peaks were detected
        peak_channels = peaks[0]
        
        
        #counts the number of spikes in frequency channels before 300
        early_spikes = []
        for channel in peak_channels:
            if channel < 300:
                early_spikes.append(channel)

        
        #counts the number of spikes in frequency channels between 1000 and 1300
        comb_spikes = []
        for channel in peak_channels:
            if channel > 1000 and channel <1300:
                comb_spikes.append(channel)

        #counts the number of spikes in frequency channels where intermod is seen
        intermod_spikes=[]
        for channel in peak_channels:
            if (channel < 1000 and channel >700) or channel >1300:
                intermod_spikes.append(channel)
                
                
    
        #this catches intermod
        #in testing, these conditionals can be toggled with.
        if len(intermod_spikes)>15 and len(comb_spikes)<15 and len(early_spikes)<10:
            intermod_monster=True
        
        #this catches comb
        #in testing, these conditions can be toggled with
        if len(comb_spikes)>15 and len(early_spikes)>10 and len(early_spikes)>10:
            comb_monster=True
        
        if intermod_monster:
            print('Ant  '+str(ant)+' intermod: '+str(intermod_monster))
        if comb_monster:
            print('Ant  '+str(ant)+' comb: '+str(comb_monster))


#Adele's function for catching blob monster
#one should note that I have it set to pick up on correlation blobs that are very visible, but 
#there are also correlation blobs that are too "thin" to see, and you could detect those by
#decreasing the lower bound on the prominence.
#also sometimes catches spike monsters like comb

def blob_trap(uv):
    blob_ants=[]

    for ant in uv.antenna_numbers:

        data = np.abs(uv.get_data(ant,ant,'xx'))[0]

        freq=uv.freq_array[0]*1e-6


        #this is the prominence range of the correlation blob ripples
        peaks=scipy.signal.find_peaks(data,prominence =(1.9e5,1e8))

        peak_channels = peaks[0]



        #will not include fm radio band
        filtered_peak_channels=[]
        for channel in peak_channels:
            if (channel>300 and channel<500)==False:
                filtered_peak_channels.append(channel)


        #the number of channels between peaks
        diff_values=np.diff(filtered_peak_channels)


        #array that will document consecutive diffs of three.
        consecutive_three_count=[]
        #will count how many blobs we have documented
        blob_count=0
        #keeps track of index
        index=0
        #determines if there is a blobMonster
        for diff in diff_values:
            if blob_count==0:
                #if the current diff and the diff in front of it are both 3
                #including 2 and 4 becuase sometimes the diff is ~slightly~ off of 3 for a number or two
                if diff==3 and (index+1)<len(diff_values)and (diff_values[index+1]==3 or diff_values[index+1]==2 or diff_values[index+1]==4):


                    consecutive_three_count.append(diff)
                    #if there are six 3 diffs in a row, and we have not already had a blob
                    if len(consecutive_three_count)==4:
                        blob_ants.append(ant)
                        #make sure antenna is not double counted
                        blob_count+=1

            index+=1


    print('Antennas with blob monster:'+str(blob_ants))


#Adele's function for catching low power and high power
#should do this test if there isnt another monster detected in the antenna.

def high_low_power (uv):
    low_power=[]
    high_power=[]

    #filters out peaks, takes the average of the flat-ish part of the bandpass, compares that number to a 
    #value which determines if it is low or high power (or neither)
    for ant in uv.antenna_numbers:


        data = np.abs(uv.get_data(ant,ant,'xx'))[0]



        #these peaks are very large and should not be included in the average.
        peaks=scipy.signal.find_peaks(data,prominence =1)

        peak_channels = peaks[0]

        filtered_data=[]
        index=0
        for dat in data:
            if np.any(peak_channels == index) ==False and (index>200 and index<1400):
                filtered_data.append(dat)
            index+=1

        average_data=np.average(filtered_data)

        #this value can be toggled with.. to decide what is the best cutoff for low power.
        if average_data < 1.8e6:
            low_power.append(ant)

        #this cutoff is not researched well and should be looked into.
        if average_data >1.8e7:
            high_power.append(ant)




    print('Low Power:'+str(low_power))
    print('High Power:'+str(high_power))


#Adele's function for catching periodic spikes
#I know that this definitely works for the periodic spikes found on nosky monsters.

def periodic_spike_trap(uv):

    periodic_spike_ants=[]
    for ant in uv.antenna_numbers:



        data = np.abs(uv.get_data(ant,ant,'xx')[0])

        #filtering out the fm radio band because we don't want its nasty peaks messing with this
        filtered_data=[]
        index=0
        for dat in data:
            if (index>300 and index<500)==False:
                filtered_data.append(dat)

        peaks=scipy.signal.find_peaks(filtered_data,prominence =1.6e4)



        peak_channels = peaks[0]

        #the next peak in "peak_channels" is not necessarily part of the periodic peak series.
        #so we need to calculate the difference between this peak and several of the following peaks
        #and the difference that shows up the most in diff_array is probably the peak difference for 
        #our periodic peaks.
        #makes a list of diffs. channel difference between the peak and the peaks around it.
        index=0
        diff_array=[]
        for channel in peak_channels:
            #make sure we are not running off the end of the list
            if index+1<= len(peak_channels)-1:
                diff1= peak_channels[index+1]-channel
                diff_array.append(diff1)
            if index+2<= len(peak_channels)-1:
                diff2= peak_channels[index+2]-channel
                diff_array.append(diff2)
            if index+3<= len(peak_channels)-1:
                diff3= peak_channels[index+3]-channel
                diff_array.append(diff3)
            if index+4<= len(peak_channels)-1:
                diff4= peak_channels[index+4]-channel
                diff_array.append(diff4)

            index+=1

        #find the mode of diff_array to find the most commonly occuring diff, which will be the period 
        #of the periodic peaks
        diff_mode= scipy.stats.mode(diff_array)

        #the mode as an int, instead of computer output.
        mode_int=int(diff_mode[0])

        periodic_spike_count=[]
        for diff in diff_array:
            if diff== mode_int or diff== mode_int-1 or diff==mode_int +1:
                periodic_spike_count.append(diff)

        
        #interestingly enough, there are no visible periodic spikes when periodic_spike_count is large.. greater than 
        #around 100 or so
        #could be becasue it is picking up on a lot of small periodic spikes?
        if len(periodic_spike_count)<50:
            periodic_spike_ants.append(ant)

    print(periodic_spike_ants)


#Adele's function for catching spikes on whole bandpass
#note: needs to be more fully tested.

def whole_bandpass_spike_trap(uv):
    
    whole_bandpass_spikes=[]
    for ant in uv.antenna_numbers:

        data = np.abs(uv.get_data(ant,ant,'xx'))[0]

        peaks=scipy.signal.find_peaks(data,prominence =1e6)

        peak_channels = peaks[0]

        #this can be adjusted based on what works. i found that 100 worked.
        if len(peak_channels)>100:
            whole_bandpass_spikes.append(ant)

    print('Whole Bandpass Spikes:'+str(whole_bandpass_spikes))