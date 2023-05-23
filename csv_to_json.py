# from https://www.geeksforgeeks.org/convert-csv-to-json-using-python/

import csv
import json


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath):
	
	# create a dictionary
	data = {}
	
	# Open a csv reader called DictReader
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		
		# Convert each row into a dictionary
		# and add it to data
		for rows in csvReader:
			
			# Assuming a column named 'No' to
			# be the primary key
			key = rows['uid']

			# if (key in data):
			# 	continue
			# else:
			data[key] = rows
				# print(rows)

	data1 = json.dumps(data, indent=4)
	return data1
