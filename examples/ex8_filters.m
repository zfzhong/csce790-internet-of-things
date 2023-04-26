%%
% Zifei (David) Zhong
% zhongz@email.sc.edu
% University of South Carolina
% April 26, 2023
%
% Example 8: Example to show how to apply filters to signals.
% 
% The filters won't remove the signals completely. Essentially, the 
% filtering process decreases the power of signals that are not needed.
% .
%

close all; clear; clc;

% Mix signals of three frequencies: 50, 150, 250
fs = 1e3;
t = 1/fs:1/fs:1;
x = [1 2 3] * sin(2*pi*[50 150 250]'.* t) + randn(size(t))/10;

% Plot the original signals
figure;
plot(t, x);
xlabel("Time (s)");
ylabel("Amplitute");

%% Apply highpass filter and compare
figure; hold on;
pspectrum(x, fs);

h1 = highpass(x, 100, fs);
pspectrum(h1, fs); 
title("Highpass Filter, threshold=100");


%% Apply lowpass filter and compare
figure; hold on;
pspectrum(x, fs);

l1 = lowpass(x, 200, fs);
pspectrum(l1, fs);
title("Lowpass Filter, threshold=200");


%% Apply bandpass filter and compare
figure; hold on;
pspectrum(x, fs);

l1 = bandpass(x, [100, 200], fs);
pspectrum(l1, fs);
title("Bandpass Filter, threshold=[100, 200]");
