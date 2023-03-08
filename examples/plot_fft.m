%%
% Zifei (David) Zhong
% zhongz@email.sc.edu
% University of South Carolina
% March 7, 2023
%
% This code is revised from another 'plot_fft.m' by Sanjib Sur.
%

%%
% plot_fft: plot frequency vs. magnitude for given signal samples.
% 
% * args:
%   - data: an array of samples
%   - sr: sampling rate
%
function plot_fft(data, sr)
    N = length(data); % total number of samples

    %%
    % FFT will generate an frequency array, where the 1st half are positive 
    % frequencies, and the 2nd half are negative frequencies. We have to use 
    % fftshit() to move the second half to the left of the array (aka, center
    % the zero-frequency).
    %
    freqs = fft(data);
    coeffs = fftshift(freqs); % Center the zero-freqency
    mag = abs(coeffs) * (1 / N); % abs() gives the norm of a complex number

    %%
    % df: frequency spacing, or the minimum frequency that can be characterize;
    % df = 1/T, T = N/sr, where T is the signal's duration (length) in seconds.
    %
    df = sr / N;

    %%
    % Prepare the frequency ticks to display on the x-axis.
    %
    f = (0:N - 1) * df; % f: 0 ~ (sr-df)
    f(f >= sr / 2) = f(f >= sr / 2) - sr; % f: -sr/2 ~ sr/2
    freq_ticks = fftshift(f); % Frequencies on the x-axis

    %%
    % Plot frequency vs. magnitude
    %
    figure;
    plot(freq_ticks, mag);
    ylim([0,1]);
    xlabel('Frequency (Hz)');
    ylabel('Magnitude');
    legend(sprintf("Sampling Rate: %d", sr));
    set(gca, 'FontSize', 15);
end
