
close all;
clear all;
clc;

% Read the samples from the audio file
filename = '/Users/zfz/workspace/csce790-internet-of-things/projects/1/code/1_0_recordSound/audio-0426-00:0134.wav';
[inputSound, sampleRate] = audioread(filename);
sampleTimes = (1:length(inputSound))*(1/sampleRate);

% Play sound
% sound(inputSound, sampleRate);

% Plot the sound
figure;
plot(sampleTimes, inputSound);
ax = gca;
F_size = 20;
ax.FontSize = F_size;
xlabel('Time (sec)', 'FontSize', F_size);
ylabel('Amplitude', 'FontSize', F_size);

%Plot spectrogram
Window = 1000;
Overlap = 900;
NumFFT = 5000;
figure; spectrogram(inputSound, Window, Overlap, NumFFT, sampleRate, 'yaxis');
ax = gca;
F_size = 20;
ax.FontSize = F_size;
xlabel('Time (sec)', 'FontSize', F_size);
ylabel('Frequency (kHz)', 'FontSize', F_size);

figure; plot(abs(inputSound));
plot_fft(abs(inputSound), sampleRate);

fftCoeff = fftshift(fft((abs(inputSound))));
disp(length(fftCoeff));

fftCoeff = fftCoeff(end/2+1:end);
figure; plot(abs(fftCoeff));

%sdata = abs(fftshift(fft(abs(inputSound))));
%figure; plot(sdata);


% 
fftCoeff_low = fftCoeff(1:100);
xmarks = 0.1:0.1:10;
figure; plot(xmarks, abs(ifft(fftCoeff_low)));
xlabel("Time (s)");
ylabel("Magnitude");