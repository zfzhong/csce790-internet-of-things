%%% This scriptis used to read the binary file producedby the DCA1000
%%% and MmwaveStudio
%%% Commandto run in MatlabGUI - readDCA1000('<ADC capturebin file>')

function [retVal] = readDCA1000(fileName, Nchirps, Nframes, K)

%% global variables
% change based on sensor config 
% numberof ADC bitsper sample
numADCBits = 16; 
% do not change. number of lanes is always 4 even if only 1 lane is used. unusedlanes
numLanes = 4;
% set to 1 if real only data, 0 if complex data are populated with 0 %% readfile and convert to signed number
isReal = 0;  

Nsamples = numLanes*2*Nchirps*Nframes*K;

% read.binfile
fid = fopen(fileName, 'r');
% DCA1000 should read in two's complement data
adcData = fread(fid, 'int16');

% Make sure this is NOT a ADC file with parameters
% find the magic number: magicParam = 12233;
if (adcData(1) == 12233)
    disp('Error: this is an ADC data file with pre-pended parameters');
    retVal = zeros(4, Nchirps*Nframes*K);
    return;
end

% Most likely the file is barebone ADC file then if you come here

if Nsamples > length(adcData)
    fprintf('%s do not have that many samples\n', fileName);
    retVal = zeros(4, Nchirps*Nframes*K);
    return;
end

% Only consider first N frames
adcData = adcData(1:Nsamples);

% if 12 or 14 bits ADC per sample compensate for sign extension
if numADCBits ~= 16
    l_max = 2^(numADCBits - 1) - 1;
    adcData(adcData > l_max) = adcData(adcData > l_max)- 2^numADCBits;
end

fclose(fid);

%% organize data by LVDS lane
% for real only data 
if isReal
    % reshape data based on one samples per LVDS lane
    adcData = reshape(adcData, numLanes, []);
%for complex data
else
    % reshape and combine real and imaginary parts of complex number
    adcData = reshape(adcData, numLanes*2, []);
    adcData= adcData([1, 2, 3, 4],:) + sqrt(-1)*adcData([5, 6, 7, 8],:);
end

%% return receiver data 
retVal = adcData;

end
