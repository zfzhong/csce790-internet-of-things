%% File to store global parameters to configure the devices, frames parameters, etc.

% Make the parameters global
global profile_id start_freq idle_time adc_start_time ramp_end_time ...
freq_slope tx_start_time adc_samples sample_rate rf_gain_target ...
    ...
    enable_Tx0 enable_Tx1 enable_Tx2 ...
    tx0_start_end_idx tx1_start_end_idx tx2_start_end_idx ...
    ...
    num_chirp_frames num_chirp_loops frame_periodicty ...
    trigger_delay trigger_mode ...
    IWR1443_COM_PORT

%% COM port for the IWR1443BOOST board
% Find out which COM port from Control panel
IWR1443_COM_PORT = 11;

%% Configure hardware profile

% The time per chirp is idle_time + ramp_end_time so in the example 160 us
% A valid ramp_end_time requires:
% ramp_end_time > adc_start_time + adc_sampling_time.
% Where adc_sampling_time is #adc_samples / sampling rate.

% Profile Config
% ar1.ProfileConfig takes the following parameters
% see document TODO to have an understanding of the FMCW parameters
% profile_id = 0;
profile_id = 0;
% start_freq = 77 GHz;
start_freq = 77;
% Idle time = 100 uS;
idle_time = 100;
% ADC start time = 6 us;
adc_start_time = 6;
% Ramp end time = 60 us;
ramp_end_time = 66;
% O/p Pwr backoff Tx0 = 0 dB;
% O/p Pwr backoff Tx1 = 0 dB;
% O/p Pwr backoff Tx2 = 0 dB;
% Phase shifter Tx0 = 0 deg;
% Phase shifter Tx1 = 0 deg;
% Phase shifter Tx2 = 0 deg;
% Frequency slope = 29.982 MHz/us;
% Not all values of frequency slopes are allowed
% freq_slope = 65.998;
% freq_slope = 50.018;
freq_slope = 29.982;
% Total useful transmission time = 60 us (per chirp)
% total_bandwidth = freq_slope * ramp_end_time;
% Calculated bandwidth from the above configuration: 1798.92 MHz
% Maximum supported bandwidth in TI IWR1443BOOST 3959.88 MHz
% Tx start time = 0 us;
tx_start_time = 0;
% ADC samples = 256;
adc_samples = 256;bn
% Sample rate = 10000 ksps;
sample_rate = 10000;
% Dig gain = 0 dB;
% Dig Ph shift = 0 deg;
% RF gain target = 30 dB;
rf_gain_target = 30;

%% Chirp config
% Chirp config parameters
% Each Tx will be enabled separately in time
enable_Tx0 = 1;
enable_Tx1 = 1;
enable_Tx2 = 1;

% Configure the order of the chirps
% ex: [1 0 0] [0 1 0] [0 0 1] => tx0 = 0 tx1 = 1 tx2 = 2
% set value to zero if tx is not being used
tx0_start_end_idx = 0;
tx1_start_end_idx = 1;
tx2_start_end_idx = 2;

%% Frame config
% Frame config parameters
% Number of chirp frames
num_chirp_frames = 250;
% Number of chirps inside one frame
% num_chirp_loops = 128;      % single Tx
% num_chirp_loops = 64;         % two Tx
num_chirp_loops = 32; % three Tx
% num_chirp_loops = 5;
% Frame periodicty in ms, i.e., next frame is sent after 40 ms from the
% start of last frame
frame_periodicty = 40;
% duty cycle ~ 50%
% How do we get duty cyle?
% Each chirp has tx_start_time = 0 us, idle time = 100 us,
% ADC start time = 6 us, useful transmission = 60 us;
% so total time per chirp ~ 166 us
% Total number of chirps in a frame is 128, i.e., total time for a frame ~
% 166*128 us = 21.25 ms
% duty cycle = 21.25/40 ~ 50%

% Trigger delay is us
trigger_delay = 0;
% software or hardware trigger? 1 - software, 2 - hardware
trigger_mode = 1;

% Total data file size in bytes
% Every ADC sample is 4 byte (16 bit complex).
% numRxAnt = 4;
% adc_samples * 4 * numRxAnt * num_chirp_loops * num_chirp_frames
