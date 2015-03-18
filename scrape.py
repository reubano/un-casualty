# -*- coding: utf-8 -*-
# Script to query HDX for a list of datasets
# and return CSV table.

import sys
import csv
import yajl as json
import requests
import unicodecsv

from termcolor import colored as color

ENCODING = 'utf-8'

# Fetch arguments from command line.
if __name__ == '__main__':
	if len(sys.argv) <= 1:
		usage = '''
		Please provide a CSV path.

		python code/ebola-dataset-list.py {path/to/file.csv}

		e.g.

		python code/ebola-dataset-list.py data/data.csv
		'''
		print(usage)
		sys.exit(1)

	csv_path = sys.argv[1]

# Get list of datasets form HDX.
def getDatasetListforTag(tag=None, csv_path=None, verbose=False):

	if tag is None:
		print "Please provide tag."
		return

	if csv_path is None:
		print "I need a CSV path, e.g. data/data.csv"
		return

	print "----------------------------------"

	url = "https://data.hdx.rwlabs.org/api/action/tag_show?id=%s" % tag
	r = requests.get(url)
	json_data = r.json()

	if json_data['success'] is True:
		records = []
		m = color('SUCCESS', 'green', attrs=['bold'])
		n = color(len(json_data['result']['packages']), 'yellow', attrs=['dark'])
		print "%s : processing %s records." % (m, n)

		headers = [
			'title', 'name', 'owner_org', 'maintainer', 'maintainer_email',
			'revision_timestamp', 'id', 'num_resources', 'num_tags',
			'num_extras'
		]

		for dataset in json_data['result']['packages']:
			record = {k: v for k, v in dataset.iteritems() if k in set(headers)}
			record['num_extras'] = len(dataset['extras'])
			records.append(record)

		with open(csv_path, 'wb') as f:
			f.write(u'\ufeff'.encode(ENCODING))  # BOM for Windows
			w = unicodecsv.DictWriter(f, headers, encoding=ENCODING)

			# Write headers
			w.writer.writerow(headers)

			# Write records
			w.writerows(records)
	else:
		m = color("ERROR", "red", attrs=['bold'])
		print "%s : %s" % (m, json_data["error"]["message"])
		return


	print "----------------------------------"
	print "************* %s ***************" % (color("DONE", "blue", attrs=['blink','bold']))
	print "----------------------------------"


# Running the function.
getDatasetListforTag("ebola", csv_path, verbose = False)
