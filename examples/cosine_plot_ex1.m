%%
% Zifei (David) Zhong
% zhongz@email.sc.edu
% University of South Carolina
% March 7, 2023
%
% Example 1: Plot a cosinusoidal signal/wave
% y = cos(2*pi*freq*t + theta);
%

%%
% Close previous plots, clear variables, and clear command window;
close all; clear; clc;

%%
% Setup basic parameters and plot the wave.
%
freq = 2; % 2 cycles per second
theta = pi / 4; % Starting phase: 45 degrees;
len = 3; % Plot the wave for 3 seconds;

plot_cosine_wave(freq, theta, len);

%%
% Plot waves with various frequencies and phases.
% 
freqs = [3, 4];
phases = [pi / 6, -pi / 2];

for i = 1:2
    for j = 1:2
        plot_cosine_wave(freqs(i), phases(j), len);
    end
end

%%
% cosine_plot: plot a sinusoidal signal/wave
%
% args:
% - freq: frequency of the signal (cycle/sec), i.e., 3;
% - theta: starting phase of the signal, in radians, i.e., pi/4;
% - length: the length of the signal to plot, in second, i.e., 5;
%
function plot_cosine_wave(freq, theta, len)
    %%
    % When plot a wave, we actually plot the dots at different discrete time ticks. 
    % These dots are essentially the samples for the wave. The more samples we have,
    % the better the curve approaches the real signal.
    %

    sr = 1000; % Sampling rate, Hz (# samples/sec)
    dt = 1 / sr; % Sampling period (time between two consecutive samples, in seconds)
    N = sr * len; % Total number of samples we collect

    t = (0:N - 1) * dt; % Time ticks, an array
    y = cos(2 * pi * freq * t + theta);

    figure;
    plot(t, y);
    xlabel('Time (sec)');
    title("Example 1: Cosinusoidal Signal");
    la = sprintf("Frequency: %s, Starting phase: %s", string(freq), string(theta));
    legend(la);
    hold on;
end
