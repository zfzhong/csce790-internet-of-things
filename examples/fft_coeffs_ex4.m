%%
% Zifei (David) Zhong
% zhongz@email.sc.edu
% University of South Carolina
% March 8, 2023
%
% Example 4: Gnerate a mixed signal, and use FFT to disclose the
% fourier coefficients.
%

%%
% Close previous plots, clear variables, and clear command window;
close all; clear; clc;

%%
% initializations
% ===================================
len = 10; % duration of the signal (sec)
N = 2 ^ 10; % total number of discrete samples

f = 0.2; % frequency
fa = 2 * pi * f;

t = linspace(0, len, N + 1); % time ticks

%%
% Create the mixed signal and perform FFT.
% ===================================
y = 5 ... % frequency 0
- 2 * cos(fa * t) ... % frequency 0.2
    + 3 * cos(5 * fa * t) ... % frequency 1.0
    + 8 * sin(20 * fa * t); % frequency 4.0

fhat = y;
fhat(1) = (y(1) + y(N + 1)) / 2;
fhat(N + 1) = [];
coeffs = fft(fhat, N);

%%
% Use the first half of the DFTs to extract coefficients.
% ===================================
C = coeffs(1:N / 2);
A = 2 * real(C) / N;
A(1) = A(1) / 2;
B = -2 * imag(C) / N;

for i = 1:length(A)
    if A(i) ^ 2 > 0.001
        fprintf("A(%d) = %f\n", i, A(i));
    end

    if B(i) ^ 2 > 0.001
        fprintf("B(%d) = %f\n", i, B(i));
    end
end
