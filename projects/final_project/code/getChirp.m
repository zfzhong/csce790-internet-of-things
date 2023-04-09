%%% This scriptis used to get specific chirp data from any frame and from
%%% any chirp within that frame

% Input: 
% Big 2D matrix of data (output of readDCA1000())
% N = number of valid frame
% C = number of chirps per frame
% K = number of adc samples per chirp
% m = rx antenna to get data for
% n = frame number to get data for
% c = chirp number within that frame to get data for

function [chirpData] = getChirp(Rx_data, N, C, K, m, n, c)

% General expression to get chirp data from any Rx antenna and from any
% frames
% Assume we have N frames, C chirps per frames, K samples per chirp
% Get ADC samples from Mth antenna (M = 1, 2, 3, 4), from nth frame, from
% cth chirp
% Rx_data = Rx_data(m, (n - 1) * C * K + (c - 1) * K + 1 : ...
%     (n - 1) * C * K + (c - 1) * K + K);

if (size(Rx_data, 1) < m)
    disp('Invalid antenna number');
    chirpData = zeros(1, K);
    return;
end

if (n > N)
    disp('Invalid frame number');
    chirpData = zeros(1, K);
    return;
end

if (c > C)
	disp('Invalid chirp number');
	chirpData = zeros(1, K);
    return;
end

if ((size(Rx_data, 2) < (n - 1) * C * K + (c - 1) * K + K))
    disp('Insufficient input data, rerun readDCA1000() or recollect data');
    disp('Usage: getChirp(Rx_data, N, C, K, m, n, c)');
    chirpData = zeros(1, K);
    return;
end

chirpData = Rx_data(m, (n - 1) * C * K + (c - 1) * K + 1 : ...
    (n - 1) * C * K + (c - 1) * K + K);

end
