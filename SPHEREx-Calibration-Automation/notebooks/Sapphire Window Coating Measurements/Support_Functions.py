import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.fft as spfft

def plot_file_time_series(filename, scale=1.0):
    '''
    Plot time series from an input file
    '''
    
    fig, ax = plt.subplots()
    
    df = pd.read_csv(filename)
    
    ax.plot(df['Detector Voltage']*scale)
    
    
    
    
def plot_time_hist(t, working_samps, plot_title='Sample', fig_title=None):
    '''
    Plot time series and histogram of input samples 
    '''
    
    fig, plts = plt.subplots(1,2, figsize=(15,5))

    if fig_title is not None:
        fig.suptitle(fig_title)
    
    sample_mean = round(working_samps.mean(), 2)
    sample_std = round(working_samps.std(), 2)
    
    plts[0].plot(t, 1e3*working_samps)
    plts[0].set_title('{} Time Series'.format(plot_title))
    plts[0].set_xlabel('Time (s.)')
    plts[0].set_ylabel('Detector Voltage (mV.)')

    plts[1].hist(1e3*working_samps, bins=10)
    plts[1].set_title(r'{} Histogram: $\mu = {}$ $\sigma = {}$'.format(plot_title, sample_mean, sample_std))
    plts[1].set_xlabel('Detector Voltage (mV.)')
    plts[1].set_ylabel('Occurences')
    
    
    
def fft(samples, fs, N=None, ax=None, plot=True):
    '''
    Plot and return fft of input samples
    '''
    
    
    if N == None:
        N = len(samples)
    
    samps_fft = (1/N)*spfft.fft(samples, n=N)
    freqs = spfft.fftshift(spfft.fftfreq(N, d=1/fs)) #shift for zero frequency in center
    samps_fft = spfft.fftshift(samps_fft)
    samps_fft_mag = np.absolute(samps_fft)
       
    ##Apply fft magnitude scaling##
    #samps_fft_mag *= (2/N)
    #samps_fft_mag[np.where(freqs == 0)] /= 2
    
    fft_dict = {'fft': samps_fft, 'fft_mags': samps_fft_mag,
                'freqs': freqs}
    
    if ax is None and plot:
        fft_fig, ax = plt.subplots(figsize=(10,5))
    
    if plot:
        ax.plot(fft_dict['freqs'], fft_dict['fft_mags'])
        ax.set_title('Sample FFT')
        ax.set_xlabel('Frequency (Hz.)')
        ax.set_ylabel('|X(f)|')

    return fft_dict



def fft_rms_power_calc(fft_mags, fft_freqs, int_t=None):
    '''
    Return rms power in a two-sided magnitude spectrum after moving average filtering
    '''
    if int_t is not None:
        #Frequency response of moving average filter applied from integration
        Hma = np.abs(np.sinc(fft_freqs*int_t))
        #Apply filtering in fourier space
        fft_mags = np.multiply(Hma, fft_mags)
    
    return np.sqrt(np.sum(fft_mags**2)) 




def multiple_ts_fft(TopDf, waves, int_t=1000, fft_plot=False):
    '''
    Plot multiple time series, histogram and fft magnitude spectrums contained within a single dataframe
    '''
    for w in waves:
        df = TopDf[TopDf['Type'].isin([w])]
        voltages = df['Voltage'].values
        times = df['Time'].values
        zeros_ind = np.where(times==0)
        zeros = times[zeros_ind]
        zeros_ind = np.append(zeros_ind, -1)
        
        voltages = [voltages[zeros_ind[i]:zeros_ind[i+1]] for i in range(len(zeros_ind) - 1)]
        times = [times[zeros_ind[i]:zeros_ind[i+1]] for i in range(len(zeros_ind) - 1)]
        
        i0 = 0
        for vs in voltages:
            vs = np.array(vs)
            plot_time_hist(times[i0], vs, fig_title=w)
            df_fs = 1/(times[i0][1] - times[i0][0])
            df_fft = fft(vs, df_fs, plot=fft_plot)
            
            if(type(int_t) == int):

                sig_voltage = voltages.mean()
                print(sig_voltage)
             
            elif type(int_t) == np.ndarray:

                sig_voltages = np.zeros(len(int_t))
                sig_voltages_fft = np.zeros(len(int_t))
                i1 = 0
                for t in int_t:
                    sig_voltages[i1] = vs[:int(t*df_fs)].mean()
                    i1 += 1

                fig, ax = plt.subplots()
                ax.plot(int_t, sig_voltages)

            i0 += 1

            
            
def create_df(metadata, metadata_mask):
    '''
    Create new measurement dataframe from input metadata and metadata mask
    '''
    MaskedMetaData = metadata[metadata_mask]
    
    #Get lock-in sensitivities for all measurements
    sens = np.array([m['lock-in']['sensitivity'] for m in MaskedMetaData])

    #get voltages for all measurements
    voltages = [pd.read_csv(m['file-name'])['Detector Voltage'].values 
                                      for m in MaskedMetaData]

    #apply lock-in gain scale factor to each voltage time stream
    voltages = [np.multiply(voltages[i], sens[i]/10) for i in range(len(sens))]
        
    #Create list of wavelengths
    i = np.arange(0, len(voltages))
    waves = [[] for i_ in i]
    for i_ in i:
        if np.char.find(MaskedMetaData[i_]['type'], 'noise') != -1:
            waves[i_] = ('noise ' * len(voltages[i_])).split(' ')[:-1]
        else:
            waves[i_] = MaskedMetaData[i_]['monochromator']['wavelength'] \
                          *np.ones(len(voltages[i_]))
    

    fs = np.array([m['sample-frequency'] for m in MaskedMetaData])
    times = [np.arange(0, len(voltages[ind])*(1/(fs[ind])), 
                                   (1/(fs[ind]))) for ind in range(len(fs)) ]
        
    #Flatten extracted data so that a dataframe can be created
    waves = np.array([w for wave_list in waves for w in wave_list])
    times = np.array([t for time_list in times for t in time_list])
    voltages = np.array([v for voltage_list in voltages for v in voltage_list])
        

    #Final dictionary for all signal measurements w/o attenuation#################################
    Df = pd.DataFrame({'Type': waves, 'Time': times, 'Voltage': voltages})
    ##############################################################################################

    return Df