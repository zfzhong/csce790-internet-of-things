%%
% Zifei (David) Zhong
% zhongz@email.sc.edu
% University of South Carolina
% April 20, 2023
%
% Example 6: Example to show how to use 'range-fft' to detect the
% distances of obstacles. 
% 
% The input signal is an IF signal from a IWR1443BOOST FMCW radar. The samples
% were collected when a human is sitting about 2 meters away in front of the 
% radar, in a rectangular room. The range-fft plot shows that the peak at
% a distance about 2 meters (on the x-axis).
%
% Rada parameters:
% 1. start frequency 77G Hz;
% 2. samples per chirp: adc_samples = 256;
% 3. sampling rate: sampling_rate_sps = 1e7 samples per second (10000 samples per ms);
% 4. FMCW slope: slope_hps = 29.982*1e6*1e6 Hz per second (29.982 MHz per us);

close all; clear; clc;


light_speed = physconst('lightspeed');
adc_samples = 256;
sampling_rate_sps = 1e7;
slope_hps = 29.982*1e6*1e6;

% Mapping: frequency -> range
range_axis = ((((0:adc_samples-1)/adc_samples)*sampling_rate_sps)/slope_hps)*light_speed/2;

% Load all samples form a file
samples = load_signal_from_file('chirp_sample.bin', 512);

% Plot range-fft
plot(range_axis, abs(fft(samples)));

%%
% Function that loads a sequence of samples from a file. Each sample is
% stored in the file as two double numbers (both real and imaginary).
% * args:
% - filename: the data file
% - size: twice the number of samples from the data file 
% 
function f = load_signal_from_file(fileanme, size)
    fid = fopen('chirp_samples.bin', 'r');
    rawdata = fread(fid, 512, 'double');
    fclose(fid);

    mid = size/2;
    d1 = rawdata(1:mid);
    d2 = rawdata(mid+1:size);

    f = d1 + j*d2;
end


