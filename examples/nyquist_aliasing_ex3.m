%%
% Zifei (David) Zhong
% zhongz@email.sc.edu
% University of South Carolina
% March 8, 2023
%
% Example 3: Demonstrate the nyquite frequency and frequency aliasing in FFT.
%
% Given a cosinusoidal signal with frequency f Hz, the nyquist frequency is 
% 2*f Hz. The samping rate for FFT should be greater than twice the frequency
% of the signal in order to recover it. Frequency aliasing happens otherwise.
%

%%
% Close previous plots, clear variables, and clear command window;
close all; clear; clc;


%%
% Plot a 14-Hz signal at various samping rate. When the sampling rate is
% equal to or lower than 24 Hz, the plotted waves don't have the correct 
% frequency. Please refer to the Nyquist rate/frequency theory for details.
%
freq = 14; % 14 Hz

len = 3; % signal duration: 3 seconds
sample_rates = [6,8,10,12,14,16,18,20,22,24,26,28,30]; % various sampling rate

for i=1:length(sample_rates)
    sr = sample_rates(i);
    plot_cosine_samples(freq, len, sr);

    loc = freq_aliasing(freq, sr); % Calculate the frequency aliasing.
    fprintf("Freuency: %d, sampling rate: %d, aliasing location: %d\n", freq, sr, loc);
end

%%
% freq_aliasing: calculating the frequency aliasing location.
% * args:
%   - freq: frequency of the signal/wave
%   - sr: sampling rate
%
function f = freq_aliasing(freq, sr)
    nyquist_freq = sr /2;
    if nyquist_freq > freq
        f = freq;
    else
        r = mod(freq, nyquist_freq);
        q = (freq - r) / nyquist_freq;

        if r > 0
            q = q + 1;
        end

        if mod(q,2) == 0
            f = mod(q * nyquist_freq, freq);
        else
            f = nyquist_freq - mod(q*nyquist_freq, freq);
        end
    end
end

%%
% Plot wave and FFT based on the given frequency and sampling rate.
% * args:
%   - freq: frquency of the wave
%   - len: duration of the wave (in second)
%   - sr: sampling rate
%
function plot_cosine_samples(freq, len, sr)
    N = sr * len; % total number of samples

    T = 1/sr;
    t = (0:N-1) * T; % time ticks

    theta = pi/2; % Phase pi/2, purposely selected for demonstration purpose
    y = cos(2*pi*freq*t + theta);

    %%
    % Plot the wave.
    figure;
    plot(t, y);
    ylim([-1,1]);
    xlabel("Time (sec)");
    legend(sprintf("Frequency: %d, Sampling Rate: %d", freq, sr));
    set(gca, "FontSize", 15);
    hold on;

    %%
    % Plot the FFT.
    plot_fft(y, sr);
end