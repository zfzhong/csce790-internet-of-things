%%
% Zifei (David) Zhong
% zhongz@email.sc.edu
% University of South Carolina
% April 20, 2023
%
% Example 7: Example to how to extract the phase of signals.
% (this example is taken from a Matlab web page)
%
% Mix two signals (one with frequency 15 and phase -pi/4, the other with
% frequency 40 and phase pi/2) and plot the phases after FFT.
%

fs = 100;
t = 0:1/fs:1-1/fs;
x = cos(2*pi*15*t - pi/4) - sin(2*pi*40*t);

y = fft(x);
z = fftshift(y);

ly = length(y);
f = (-ly/2:ly/2-1)/ly*fs;

figure;
stem(f,abs(z))
xlabel 'Frequency (Hz)'
ylabel '|y|'
grid

tol = 1e-6;
z(abs(z) < tol) = 0;
theta = angle(z);

figure;
stem(f,theta/pi)
xlabel 'Frequency (Hz)'
ylabel 'Phase / \pi'
grid
