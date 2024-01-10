% Zifei (David) Zhong, zhongz@email.sc.edu
% 
% separate the 'U S C' letters spoken in the audio file
% into three audio files.
%

close all;
clear all;
clc;


% Read the samples from the audio file
filename = './48k_audio.wav';
[inputSound, sampleRate] = audioread(filename);
disp(sampleRate);
disp(length(inputSound));

sampleTimes = (1:length(inputSound))*(1/sampleRate);


fftCoeff = fftshift(fft((abs(inputSound))));

fftCoeff = fftCoeff(end/2+1:end);

figure; plot((0.2:0.2:24000), abs(fftCoeff));
xlabel("Frequency");
ylabel("Magnitude");
title("FTT of sound");

figure; plot(inputSound);

% 5. Plot 
%figure; plot(abs(fftCoeff));

% lowpass filter
% figure this out?
figure; plot(lowpass(abs(inputSound), 20, sampleRate));
title("Low pass filter, threshold=20");

% bandpass filter
% figure this out?
figure; plot(bandpass(abs(inputSound), [0.2 100], sampleRate));

% 6. Keep signal with 1<= frequency <=100, and do inverse fft.
freq = find_frequency_threshold(abs(inputSound), length(inputSound)/sampleRate);
disp(freq);

fftCoeff_low = fftCoeff(1:freq);

figure; plot(abs(ifft(fftCoeff_low)));

% now let's split the file
data = abs(ifft(fftCoeff_low));
threshold = find_threshold(data);
disp(threshold);

nLeft = 1;
nRight = 1;
N = length(data);
counter = 1;
inChunk = false;

for i=1:N
    if (data(i) <= threshold)
        if (inChunk == true)
            nRight = i/N * length(inputSound);

            fname = 'split'+string(counter)+'.wav';
            audiowrite(fname, inputSound(nLeft:nRight), sampleRate);
            
            disp(counter);
            counter = counter + 1;

            inChunk = false;

            nLeft = 0;
            nRight = 0;
        end
    else
        if (inChunk == false)
            inChunk = true;
            nLeft = i/N * length(inputSound);
        end
    end
end

if (nLeft > 0 && nRight == 0)
    fname = 'split'+string(counter)+'.wav';
    audiowrite(fname, inputSound(nLeft:end), sampleRate);
end

plot_spectrogram('split1.wav');
plot_spectrogram('split2.wav');
plot_spectrogram('split3.wav');


function freq = find_frequency_threshold(data, n)
    fftCoeff = fftshift(fft(data));
    mag = (1/length(data))*abs(fftCoeff);
    
    s = 0;
    for i=1:length(mag)
        if (s+mag(i) > 0.00005*n)
            freq = i;
            return
        end
        s = s + mag(i);
    end

end

function plot_spectrogram(inputfile)
    [inputSound, sampleRate] = audioread(inputfile);
    %sampleTimes = (1:length(inputSound))*(1/sampleRate);
    Window = 1000;
    Overlap = 900;
    NumFFT = 5000;
    %obw(inputSound,48000);
    figure; thd(inputSound,48000);
    %s = spectrogram(inputSound, Window, Overlap, NumFFT, sampleRate);
    %disp(s);
    figure; spectrogram(inputSound, Window, Overlap, NumFFT, sampleRate, 'yaxis');
    ax = gca;
    F_size = 20;
    ax.FontSize = F_size;
    xlabel('Time (sec)', 'FontSize', F_size);
    ylabel('Frequency (kHz)', 'FontSize', F_size);
end

function threshold = find_threshold(data)
    res = [];
    N = length(data);
    x = data(1);

    for i=1:N
        if (i+1 < N)
            if (data(i) > data(i+1))
                x = data(i+1);
            end
            if (data(i) < data(i+1))
                res(end+1) = x;
            end
        end
    end

    res = sort(res);
    for i=1:length(res)
        nChunks = count_chunks(data(1:end*0.8), res(i));
        if (nChunks == 3)
            threshold = res(i);
            return
        end
    end
end


function nChunks = count_chunks(data, threshold)
    nChunks = 0;
    inChunk = false;
    N = length(data);
    for i=1:N
        if (data(i) > threshold)
            if (inChunk == false)
                inChunk = true;
                nChunks = nChunks + 1;
            end
        end
        if (data(i) <= threshold)
            if (inChunk == true)
                inChunk = false;
            end
        end        
    end
end

