% MATLAB data capture from DCA1000EVM board in a continuous loop
% 
% Author: Sanjib Sur
% Institute: University of South Carolina
% 
% Date: 03/12/2020
%
% A demo script to collect and process data from DCA1000EVM
% mmWave studio is connected to the board, and we connect and send our
% command from MATLAB to mmWave studio
% mmWave studio use LUA shell to receive and transmit command from and to
% MATLAB

% We send commands to the LUA shell using the following general commands
% General command
% Lua_String = 'WriteToLog("Running script from MATLAB\n", "green")'; 
% ErrStatus = RtttNetClientAPI.RtttNetClient.SendCommand(Lua_String); 

% % Send a LUA file
% bitopfile = 'C:\\ti\\mmwave_studio_01_00_00_00\\mmWaveStudio\\Scripts\\bitoperations.lua';
% Lua_String = sprintf('dofile("%s")', bitopfile);
% ErrStatus = RtttNetClientAPI.RtttNetClient.SendCommand(Lua_String);


close all;
clear all;
clc;


%% Launch mmWave studio from here

% save the current folder
% curr_folder = pwd;
% Go to the folder where mmWaveStudio is present
curr_folder = cd('C:\ti\mmwave_studio_01_00_00_00\mmWaveStudio\RunTime\');
% Launch mmWaveStudio
system('mmWaveStudio.exe &');
% pause till the application is initiliazed
pause(12);
% return to the working folder
cd(curr_folder);


%% Get the global paths and variables
globalpath;

% Check if the globalpaths exist
if (~exist(file_path, 'dir') | ~exist(fw_path, 'dir') | ...
        ~exist(data_path, 'dir'))
    disp('Error in mmWave studio installation is found! Please check.');
    return;
end

if ~exist(adc_data_params_path_folder, 'dir')
    fprintf('Error in data folder %s\n', adc_data_params_path_folder);
    return;
end

if ~exist(RSTD_DLL_Path, 'file')
    fprintf('%s not found\n', RSTD_DLL_Path);
    return;
end

if ~exist(BSS_FW, 'file') | ~exist(MSS_FW, 'file')
    fprintf('Firmware files\n %s\n or %s\n not found\n', BSS_FW, MSS_FW);
    return;
end


%% Get the global parameters for device configuration, frame configuration, etc.
loadConfig;


% Sanity check on the parameters
% We need to make sure the ramp time, chirp time, etc. are valid
total_chirp_duration = idle_time + ramp_end_time;

% chirp sampling validation
% A valid ramp_end_time requires:
% ramp_end_time > adc_start_time + adc_sampling_time. 
% Where adc_sampling_time is #adc_samples / sampling rate.
% sample_rate is in ksps, adc_sampling_time is also coverted to us
adc_sampling_time = (adc_samples/(sample_rate*1e3))*1e6;
if (ramp_end_time < adc_start_time + adc_sampling_time)
    disp('Error in chirp timing parameters: Not sufficient ramp_end_time');
    return;
end

% We need to make sure the Duty cycle is not more than 75% for any
% configuration
if (((tx_start_time + idle_time + adc_start_time + ramp_end_time)*num_chirp_loops)/1000) > 0.75*frame_periodicty
    disp('Duty cycle is more than 75%, please adjust the frame parameters');
    return;
end

% Total data collection duration per trigger
total_data_duration_per_trigger = frame_periodicty*num_chirp_frames;
fprintf('Total data collection duration per trigger: %.2f ms\n', ...
    total_data_duration_per_trigger);

% Do sanity check for frequency sweeping, so that it does not go beyond the
% allowed bandwidth in IWR1443


%% Ping LUA shell to make sure it can accept MATLAB commands
ErrStatus = pingLUA();
% try pinging at most 10 times unless successful
ping_count = 10;
while (ErrStatus ~= 30000)
	ping_count = ping_count - 1;
    if ping_count == 0
        break;
    end
    
    % ping again
    ErrStatus = pingLUA();
end

% something has gone very wrong!
if ping_count == 0
    % kill the running mmWaveStudio application
    % cleanup
    system('taskkill /IM mmWaveStudio.exe');
    return;
end

% make sure the user has reset and connect to the board
% input('Did you reset the board and connected to it via mmWave studio? (y/n)'); 


%% Reset and connect the board
ErrStatus = resetnconnectBoard();
if (ErrStatus ~= 30000)
    return;
end


%% BSS and MSS firmware download
ErrStatus = loadBSSMSS();
if (ErrStatus ~= 30000)
    return;
end


%% Configure device: channel, clock, etc.
ErrStatus = deviceConfig(enable_Tx0, enable_Tx1, enable_Tx2);
if (ErrStatus ~= 30000)
    return;
end


%% Configure hardware profile
ErrStatus = profileConfig(profile_id, start_freq, idle_time, ...
    adc_start_time, ramp_end_time, freq_slope, tx_start_time, adc_samples, ...
    sample_rate, rf_gain_target);
if (ErrStatus ~= 30000)
    return;
end


%% Chirp config
ErrStatus = chirpConfig(enable_Tx0, enable_Tx1, enable_Tx2, ...
    tx0_start_end_idx, tx1_start_end_idx, tx2_start_end_idx);
if (ErrStatus ~= 30000)
    return;
end


%% Frame config
% May miss the last frame, so collect one extra frame
ErrStatus = frameConfig(num_chirp_frames + 1, num_chirp_loops, ...
    frame_periodicty, trigger_delay, trigger_mode, ...
    tx0_start_end_idx, tx1_start_end_idx, tx2_start_end_idx);
if (ErrStatus ~= 30000)
    return;
end


%% Configure DCA1000EVM board
ErrStatus = DCA1000Config();
if (ErrStatus ~= 30000)
    return;
end


%% Collect via a while loop

max_loop = 1000;

for loop_idx = 1:max_loop

%     fprintf('Loop idx: %d\n', loop_idx);
    
%% Capture frames
% captureFrames takes waiting time (in seconds) as input
% total_data_duration_per_trigger is in ms
ErrStatus = captureFrames(total_data_duration_per_trigger/1000);
if (ErrStatus ~= 30000)
    return;
end


%% Merge Raw data files
% in case the size of collected data is more than 1 GB, there will be
% multiple Raw data files, adc_data_Raw_0.bin, adc_data_Raw_1.bin, etc.
% so we need to merge them into a single file adc_data.bin

% New file where ADC samples with pre-pended parameters will be stored
new_file_name = sprintf('adc_data_params%d.bin', loop_idx-1);


%% Update ADC file to pre-pend all parameters at the beginning
adc_data_params_path = sprintf('%s\\%s', adc_data_params_path_folder, new_file_name);
ErrStatus = updateADCFile(adc_data_path, adc_data_params_path);
if (ErrStatus ~= 0)
    disp('Error in saving adc_data with parameters');
    return;
end

reply = input('Continue?', 's');

% Exit data capture loop if the input begins with an 'N'.
if size(reply) > 0
    if strcmpi(reply(1), 'n') | strcmpi(reply(1), 'N')
    break;
    end
end

end


%% kill the running mmWaveStudio application
system('taskkill /IM mmWaveStudio.exe');
