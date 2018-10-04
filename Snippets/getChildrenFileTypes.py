#! usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import os
import csv
 
# Function parses tab delimited file information
# fileName must be within the current working directory
def readFile(fileName, separator):
    # Using a 'with' statement is safer than
    # needing to remember to close the file afer reading
	with open(fileName) as file:
        # Delimiter is the character separating the values
		reader = csv.reader(file, delimiter=separator)
        # Generates a list of the stored information
		data = list(reader)
    # Returns the list of data gathered from the file
	return data

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

text_files = log_filetype_within('.', '.txt', 'text_files_within_test.txt')
