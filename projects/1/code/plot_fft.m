%function [mag, freqList] = plot_fft(data, sampleRate)
function plot_fft(data, sampleRate)
    fftCoeff = fftshift(fft(data));
    mag = (1/length(data))*abs(fftCoeff);
    N = length(data);
    %freqList = (-N/2:N/2-1)*(sampleRate/N)
    
    % calculate frequency spacing
    df = sampleRate / N;
    % calculate unshifted frequency vector
    f = (0:(N-1))*df;
    % move all frequencies that are greater than fs/2 to the negative side of the axis
    f(f >= sampleRate/2) = f(f >= sampleRate/2) - sampleRate;
    % freq are aligned with one another; if you want frequencies in strictly
    % increasing order, fftshift() them
    freqList = fftshift(f);
    
    figure;
    %plot(freqList, 20*log(mag));
    plot(freqList, mag);
    xlabel('Frequency (Hz)');
    ylabel('Magnitude');
    set(gca, 'FontSize', 15);
    
%     fftLen = size(mag)
%     freqLen = size(freqList)
%     [freqList(1) freqList(end)]
end