%%
% Zifei (David) Zhong
% zhongz@email.sc.edu
% University of South Carolina
% March 7, 2023
%
% Example 2: Gnerate a mixed signal, and use FFT to disclose the
% frequencies of the mixed signal.
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

freqs = [1, 2, 3]; % three different frequencies

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
% Plot FFT of the mixed signal.
plot_fft(ms, sr);

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
        s = cosine_signal(freqs(i), sr, len);
        x = s(1, :);
        y = s(2, :);

        if length(m) == 0
            m = y;
        else
            m = m + y;
        end
    end
end

%%
% cosine_signal: Generate a cosinusoidal signal
%  * return: two arrays, one is the X ticks, and the other is the Y values.
%  * args:
%    - freq: frequency of the signal
%    - sr: sampling rate
%    - len: duration of the signal (in second)
%
function s = cosine_signal(freq, sr, len)
    T = 1 / sr;
    N = sr * len;

    t = (0:N - 1) * T;
    v = cos(2 * pi * freq * t);

    s = [t; v];
end
