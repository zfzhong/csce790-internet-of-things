%%
% Zifei (David) Zhong
% zhongz@email.sc.edu
% University of South Carolina
% April 4, 2023
%
% Example 25: FFT with hanning window. When the frequencies of the input
% signals are not multiples of the frequency resolution, the FFT will
% result spreading of power across the spectrum. Applying hanning window
% is an effective remedy. Please compare the two generated figures.
%

%%
% Close previous plots, clear variables, and clear command window;
close all; clear; clc;

%%
% Create the target signal as a combination of 3 cosinusoidal waves.
%
len = 2; % Signal's duration: 2 seconds
sr = 100; % Sampling rate
N = sr * len; % Total number of samples;

freqs = [2.3, 4.7]; % two frequencies that are not multiple of 1/2.

time_ticks = (0:N - 1) * (1 / sr);
freq_ticks = (0:N - 1) * (sr / N);
ms = mix_signals(freqs, sr, len); % generate the mixed signal


%%
% Plot the mixed signal
%
figure;
plot(time_ticks, ms);
xlabel("Time (sec)");
set(gca, "FontSize", 15);
hold on;

%%
% Plot FFT of the mixed signal without applying hanning window.
plot_fft(ms, sr);
hold on;

%%
% Plot FFT of the mixed signal with hanning window applied.
hann_win = hanning(N);
ms = hann_win.* ms;
plot_fft(ms, sr);
title('With Hanning window');

%%
% mix_signals: Generate a signal that is a mix of multiple cosinusoidal waves.
% * args:
%   - freq: frequency of the signal
%   - sr: sampling rate
%   - len: duration of the signal (in second)
%
function m = mix_signals(freqs, sr, len)
    m = [];

    for i = 1:length(freqs)
        y = cosine_signal(freqs(i), sr, len);
        
        if isempty(m)
            m = y;
        else
            m = m + y;
        end
    end
end

%%
% cosine_signal: Generate a cosinusoidal signal
%  * return: the Y values at time ticks.
%  * args:
%    - freq: frequency of the signal
%    - sr: sampling rate
%    - len: duration of the signal (in second)
%
function s = cosine_signal(freq, sr, len)
    T = 1 / sr;
    N = sr * len;

    t = (0:N - 1) * T;
    s = cos(2 * pi * freq * t);
end

function out = hanning(N)

out = sin(pi*[1:N]/N);

end