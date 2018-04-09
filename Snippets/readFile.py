# -*- coding: utf-8 -*-
# The built-in comma-separated-value library is useful
# for parsing data files.
import csv
 
# Function parses tab delimited file information
# fileName must be within the current working directory
def readFile(fileName):
    # Using a 'with' statement is safer than
    # needing to remember to close the file afer reading
	with open(fileName) as file:
        # Delimiter is the character separating the values
		reader = csv.reader(file, delimiter="\t")
        # Generates a list of the stored information
		data = list(reader)
    # Returns the list of data gathered from the file
	return data