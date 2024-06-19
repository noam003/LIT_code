function randomChopWavFiles()
    % Create the output folder if it does not exist
    outputFolder = 'randchop';
    if ~exist(outputFolder, 'dir')
        mkdir(outputFolder);
    end

    % Get a list of all .wav files in the current folder
    files = dir('*.wav');

    % Loop through each file
    for i = 1:length(files)
        % Get the filename
        filename = files(i).name;
        % Read the audio file
        [audioData, sampleRate] = audioread(filename);
        numSamples = length(audioData);

        % Generate a random starting sample within the number of samples
        randomStartSample = randi([48000, 96000]);

        % Chop the audio from the random starting sample to the end
        choppedAudio = audioData(randomStartSample:end, :);

        % Create a new filename for the chopped audio
        [~, name, ext] = fileparts(filename);
        newFilename = fullfile(outputFolder, [name '_chopped' ext]);

        % Save the chopped audio to the new file
        audiowrite(newFilename, choppedAudio, sampleRate);

        % Display the filename and the random starting sample
        fprintf('File: %s, Random Start Sample: %d, Saved As: %s\n', filename, randomStartSample, newFilename);
    end
end
