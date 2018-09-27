import re
import os
# .       - Any Character Except New Line
# \d      - Digit (0-9)
# \D      - Not a Digit (0-9)
# \w      - Word Character (a-z, A-Z, 0-9, _)
# \W      - Not a Word Character
# \s      - Whitespace (space, tab, newline)
# \S      - Not Whitespace (space, tab, newline)

# \b      - Word Boundary
# \B      - Not a Word Boundary
# ^       - Beginning of a String
# $       - End of a String

# []      - Matches Characters in brackets
# [^ ]    - Matches Characters NOT in brackets
# |       - Either Or
# ( )     - Group

# Quantifiers:
# *       - 0 or More
# +       - 1 or More
# ?       - 0 or One
# {3}     - Exact Number
# {3,4}   - Range of Numbers (Minimum, Maximum)


# #### Sample Regexs ####

# [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+
part1_regex = re.compile(r"""(                    
    (\w*\d_)       # Lab Number
    (\s)?               # Space
    (\d*)               # Number of Samples
    (\s)                # Space
    (\d*)             # Sampling Freq
    (hz)
    (\.[a-zA-Z]{2,4})   # Suffix
                        )""", re.VERBOSE)

part2_regex = re.compile(r"""(                    
    (\w{3}\d{1}_)       # Lab Number
    (FFT\s|p2_)           # Part number or test
    (raw\sdata|resample)?
    (\s)?
    (\d*)               # Number of Samples
    (_)?           # Space
    (\d*|\w{2,4})             # Sampling Freq
    (hz)?
    (\.[a-zA-Z]{2,4})   # Suffix
                        )""", re.VERBOSE)
string1 = 'lab3_ 2048 500hz.txt lab3_FFT raw data 512_1000.txt lab3_FFT resample 2048_250.txt lab3_p2_50fftr.txt lab3_p2_500FFT.txt lab3_p2_500hz.txt'
str_1_matches = part1_regex.findall(string1)
for match in str_1_matches:
    if match[-4] == ' ':
        n_samples = str_1_matches[0][-5]
        s_freq = str_1_matches[0][-3]
        graph_title = '200 Hz Signal with {} samples drawn at {} Hz.'.format(n_samples, s_freq)
        # print(graph_title)
        return graph_title

str_2_matches = part2_regex.findall(string1)
for match in str_2_matches:
    if match[3].startswith('r'):
        d_source = match[3].title()
        n_samples = match[-5]
        s_freq = match[-3]
        graph_title = '200 Hz Signal LabView FFT {} Data with {} samples drawn at {} Hz.'.format(d_source, n_samples, s_freq)
        # print(graph_title)
        return graph_title
    else:
        s_freq = match[-5]
        if match[-3].lower() == 'fftr':
            graph_title = 'Aluminum Bar Vibration Labview Raw Data FFT with {} Hz. Sampling Frequency'.format(s_freq)
            # print(graph_title)
            return graph_title
        elif match[-3].lower() == 'fft':
            graph_title = 'Aluminum Bar Vibration Labview Resampled FFT with {} Hz. Sampling Frequency'.format(s_freq)
            return graph_title
            # print(graph_title)
        else:
            graph_title = 'Aluminum Bar Vibration Accelerometer Data with {} Hz. Sampling Frequency'.format(s_freq)
            return graph_title
            # print(graph_title)


def log_filetype_within(directory, extension, filename):
    # Creates a log file containing all of the files of a given type
    # within the folder tree.

    results = []

    # results = str()

    # os.walk moves through the whole folder tree and looks at each
    # item within. Returns these three arguments.
    for dirpath, dirnames, files in os.walk(directory):
        # Files is an iterable containing a list of the directories
        # inside of the current 'step' folder.
        for name in files:
            # Modifiers allow us to control for case formatting
            # and find the correct extension.
            if name.lower().endswith(extension):
                # The item name ends with the required extension, so 
                # add the results to the existing list

                results.append(os.path.join(dirpath, name))

                # results += '{}\n'.format(os.path.join(dirpath, name))

    # Open the log filename and write the results instead of printing

    # with open(filename, 'w+') as logfile:
    #     logfile.write(results)
    for result in results:
        print(result)
    return(results)

# text_files = log_filetype_within('.', '.txt', 'text_files_within_test.txt')