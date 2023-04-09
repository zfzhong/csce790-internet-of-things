%%
% Zifei (David) Zhong
% zhongz@email.sc.edu
% University of South Carolina
% April 6, 2023
%
% Read data chirp by chirp from outpupt of 'DCA_trigger_capture_loopmax.m' to generate
% a 4D data matrix.
%
% This code is modified from 'post_process.m' originally written by Jackie Schellberg.
%


close all; clear; clc;

adc_file_name = 'adc_data_params0.bin';

% 32 chirps per frame in configuration for 3 transmitters.
config_chirps = 32;

% 250 total frames are configed to be transmitted, lasting about 10 sec.
config_frames = 250;

% 256 adc samples per chirp in configuration
config_samples = 256;

% 4 receivers of IWR1443
num_rx = 4;

% 3 transmitters of IWR1443
num_tx = 3;

% light speed in meters per second
light_speed = physconst('lightspeed');

% read the raw file from loadConfig attributes
[profile_id start_freq idle_time adc_start_time ramp_end_time ...
    freq_slope tx_start_time adc_samples sample_rate rf_gain_target ...
    enable_tx0 enable_tx1 enable_tx2 num_frames num_chirps ...
    frame_periodicty trigger_delay trigger_mode Rx_data]  = ...
        readDCA1000Params(adc_file_name, config_chirps, config_frames, config_samples, num_tx);


%% Parameters collection
% Collect the parameters using the first measurement, rest of the
% measurements parameters are the same

% sample rate: 10000 ksps
% sampling rate is in ksps --> convert to sps, i.e., multiply by 1e3
sampling_rate_sps = sample_rate*1e3;

% freqency slope: 29.982M Hz/us
% freq_slot is in MHz/us --> convert to Hz/s, i.e., multiply by 1e6*1e6
slope_hps = freq_slope*1e6*1e6;

% chirp duration, the whole time slot is about 166 us for each chirp. But the actual transmitting time
% is only 66 us.
%
% idle_time = 100 us
% ramp_end_time = 66 us
chirp_duration = (idle_time + ramp_end_time)*1e-6;

% Range bins
% range_axis = ((((0:adc_samples-1)/adc_samples)*sampling_rate_sps)/slope_hps)*light_speed/2;
%% Range focusing to z0
% ADC converter starts late (value > 0), so the distance that we estimate
% is larger distance
tI = 4.5225e-10; % Instrument delay for range calibration (corresponds to a 6.78cm range offset)

% The above is from the UT Dallas SAR implementation
range_axis = (((((0:adc_samples-1)/adc_samples)*sampling_rate_sps)/slope_hps) - tI)*light_speed/2;

f0 = start_freq + adc_start_time*slope_hps; % This is for ADC sampling offset
f = f0 + (0:adc_samples - 1)*slope_hps/sampling_rate_sps; % wideband frequency

% In FMCW, the bandwidth actually determines the frequency resolution, which determines
% the range resolution.
range_resolution = light_speed/(2*(f(end)-f(1)));
fprintf('Range resolution: %0.3f (m.)\n', range_resolution);

% adc_samples = 256
% Normalize for window, and for 2D FFT gain.
hann_win = hanning(adc_samples);
hw = hann_win.';

pruned_adc_samples1 = zeros(adc_samples, num_frames, num_rx, num_tx);
pruned_adc_samples2 = zeros(adc_samples, num_frames, num_rx, num_tx);

% Within each frame time, there are 32 chirps sent (given 3 transmitters);
%% Collect frame by frame, use median of the chirps inside one frame
for i = 1:num_frames
    % Resize Rx_data
    adc_dat1 = zeros(adc_samples, num_rx, num_tx, num_chirps);
    adc_dat2 = zeros(adc_samples, num_rx, num_tx, num_chirps);

    % loop through the 32 chirps within in a frame time
    for j = 1:num_chirps

        % loop through 4 receivers
        for r = 1:num_rx
            
%             % debug to make sure object comes at correct dist per chirp 
%             plot(range_axis, 20*log10(abs(fft(getChirp(Rx_data, ...
%                  num_frames, num_chirps, adc_samples, r, i, j)))))
            
            % loop through 3 transmitters
            for t = 1:num_tx
                % get chirp in interleaved Tx configs
                adc_dat1(:, r, t, j) = getChirp(Rx_data, ...
                    num_frames, num_chirps * num_tx, adc_samples, ...
                    r, i, (j-1) * num_tx + t);
                
                % Another set of data with hanning window smoothing
                adc_dat2(:, r, t, j) = hw.* adc_dat1(:, r, t, j);
            end
        end

    end

    % first make sure adc_dat and adc_dat1 has three dimensions
    if length(size(adc_dat1)) ~= 4 || length(size(adc_dat2)) ~= 4
        disp('Error: in adc_dat dimension');
        status = -1;
        return;
    end

    % Find median of chirps within each frames;
    % Question: The 32 chirps were sent within a 40ms time interval, how much
    % difference could it be between chirps?
    pruned_adc_samples1(:, i, :, :) = median(adc_dat1, 4);
    pruned_adc_samples2(:, i, :, :) = median(adc_dat2, 4);
end

% rawdata dimensions: num_samples * num_frames * num_rx * num_tx
rawdata = pruned_adc_samples1;

%% fft for middlemost frame
figure(30)
for i = 1:num_tx
    plot(range_axis, 20*log10(abs(fft(rawdata(:,floor(end/2), 3, i)))));
    hold on;
end
title('FFT of middlemost frame across all Tx Antennas')
xlabel('Distance (m.)')
ylabel('Magnitude')

%% test phase across TX samples
% the phase of each Tx channel should be offset according to the antenna
% spacing
figure(1);
frame_idx = 50;
rx_idx = 4;
plot(angle(rawdata(:,frame_idx, rx_idx, 1)));
hold on;
plot(angle(rawdata(:,frame_idx, rx_idx, 2)));
hold on;
plot(angle(rawdata(:,frame_idx, rx_idx, 3)));
hold on;
legend('Tx1', 'Tx2', 'Tx3')
ylabel('Phase')
title('Phase across single frame, all 3 Tx, single Rx')
% 
figure(2);
tx_idx = 1;
plot(angle(rawdata(:,frame_idx, rx_idx, tx_idx)));
hold on;
plot(angle(rawdata(:,frame_idx+5, rx_idx, tx_idx)));
hold on;
plot(angle(rawdata(:,frame_idx+10, rx_idx, tx_idx)));
hold on;
title('Phase across every 5 frames, 1 Tx and 1 Rx')
ylabel('Phase')

% figure(3);
% tx_idx = 2;
% plot(angle(rawdata(:,frame_idx, rx_idx, tx_idx)));
% hold on;
% plot(angle(rawdata(:,frame_idx+5, rx_idx, tx_idx)));
% hold on;
% plot(angle(rawdata(:,frame_idx+10, rx_idx, tx_idx)));
% hold on;
% 
% figure(4);
% tx_idx = 3;
% plot(angle(rawdata(:,frame_idx, rx_idx, tx_idx)));
% hold on;
% plot(angle(rawdata(:,frame_idx+5, rx_idx, tx_idx)));
% hold on;
% plot(angle(rawdata(:,frame_idx+10, rx_idx, tx_idx)));
% hold on;