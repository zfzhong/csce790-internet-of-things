%%% This scriptis used to read the binary file produced by the DCA1000
%%% and MmwaveStudio with pre-pended by various parameters of transmissions
%%% Commandto run in MatlabGUI - readDCA1000('<ADC capturebin file>')

function [profile_id start_freq idle_time adc_start_time ramp_end_time ...
    freq_slope tx_start_time adc_samples sample_rate rf_gain_target ...
    enable_Tx0 enable_Tx1 enable_Tx2 num_chirp_frames num_chirp_loops ...
    frame_periodicty trigger_delay trigger_mode retVal] = readDCA1000Params(fileName, Nchirps, Nframes, K, n_tx)


% global variables
% change based on sensor config 
% numberof ADC bitsper sample
numADCBits = 16; 
% do not change. number of lanes is always 4 even if only 1 lane is used. unusedlanes
numLanes = 4;
% set to 1 if real only data, 0 if complex data are populated with 0 %% readfile and convert to signed number
isReal = 0;  

Nsamples = numLanes*2*Nchirps*Nframes*K*n_tx;

% read.binfile
fid = fopen(fileName, 'r');
% DCA1000 should read in two's complement data
adcData = fread(fid, 'int16');

% Make sure this IS a ADC file with parameters
% find the magic number: magicParam = 12233;
if (adcData(1) ~= 12233)
    disp('Error: this is an ADC data file without pre-pended parameters');
    profile_id = 0;
    start_freq = 0;
    idle_time = 0;
    adc_start_time = 0;
    ramp_end_time = 0;
    freq_slope = 0;
    tx_start_time = 0;
    adc_samples = 0;
    sample_rate = 0;
    rf_gain_target = 0;
    enable_Tx0 = 0;
    enable_Tx1 = 0;
    enable_Tx2 = 0;
    num_chirp_frames = 0;
    num_chirp_loops = 0;
    frame_periodicty = 0;
    trigger_delay = 0;
    trigger_mode = 0;
    retVal = zeros(4, Nchirps*Nframes*K);
    return;
end

% The file has the correct format with pre-pended parameters
% Extract the parameters

% start from second index, first one was the magic number
adcIdx = 2;
% hardware profile related
profile_id = adcData(adcIdx); adcIdx = adcIdx + 1;
start_freq = adcData(adcIdx); adcIdx = adcIdx + 1; 
idle_time = adcData(adcIdx); adcIdx = adcIdx + 1; 
adc_start_time = adcData(adcIdx); adcIdx = adcIdx + 1; 
ramp_end_time = adcData(adcIdx); adcIdx = adcIdx + 1;
% freq_slope is saved as MHz/ms, we need to convert as MHz/us
freq_slope = adcData(adcIdx)/1000; adcIdx = adcIdx + 1; 
tx_start_time = adcData(adcIdx); adcIdx = adcIdx + 1; 
adc_samples = adcData(adcIdx); adcIdx = adcIdx + 1; 
sample_rate = adcData(adcIdx); adcIdx = adcIdx + 1; 
rf_gain_target = adcData(adcIdx); adcIdx = adcIdx + 1;

% chirp config related
enable_Tx0 = adcData(adcIdx); adcIdx = adcIdx + 1; 
enable_Tx1 = adcData(adcIdx); adcIdx = adcIdx + 1;
enable_Tx2 = adcData(adcIdx); adcIdx = adcIdx + 1;

% frame config related
num_chirp_frames = adcData(adcIdx); adcIdx = adcIdx + 1; 
num_chirp_loops = adcData(adcIdx); adcIdx = adcIdx + 1; 
frame_periodicty = adcData(adcIdx); adcIdx = adcIdx + 1;
trigger_delay = adcData(adcIdx); adcIdx = adcIdx + 1; 
trigger_mode = adcData(adcIdx); adcIdx = adcIdx + 1;
    
% Get rest of I/Q data 
adcData = adcData(adcIdx:end);

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
