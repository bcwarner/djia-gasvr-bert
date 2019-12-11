# Component companies, tickers, and other terms to look for.
# Separate each one into their respective dates.

# Query the NYT for each term and save each headline and the day it was written.

# Sleep 6 seconds per minute to avoid hitting per minute rate limit.
# 4,000 request maximum per day


import json
import http.client
import time
import datetime
import pickle

api_key = "fN0RirlNXK8JG12SPfaAYR4cjDVw1Ryt"
data_start = datetime.date(2018, 11, 9) # Officially starts at 2009-11-09
data_end = datetime.date(2019, 11, 8)
daily = datetime.timedelta(days = 1)
current = data_start
q_count = 0

# Probably just stick with tickers since they may be ambiguous.

terms = []

results = []

# Get tickers from file.

inp = input("Name of input file: ")
date_form = "%m/%d/%Y"
nyt_date_form = "%Y%m%d"

with open(inp, "r") as f:
	f.readline()
	for l in f:
		y = l.split(",")
		print(y)
		dat = {"t": y[1], "start": data_start if y[3] == "data_start" else datetime.datetime.strptime(y[3], date_form).date(), "end": data_end if y[2] == "data_end" else datetime.datetime.strptime(y[2], date_form).date()}
		terms.append(dat)

fn = input("Name of results file: ")
# Rate limit

try:
	while current <= data_end:
		# Perform search
		print("Grabbing terms for date: " + str(current))
		for t in terms:
			if t["start"] > current or t["end"] < current:
				continue

			while True:
				c = http.client.HTTPSConnection("api.nytimes.com")
				q_count += 1
				c.request("GET", "/svc/search/v2/articlesearch.json?q={0}&begin_date={1}&end_date={1}&api-key={2}".format(t["t"], datetime.datetime.strftime(current, nyt_date_form), api_key))
				r = c.getresponse()
				dat = json.loads(r.read())
				if "fault" not in dat:
					break
				else:
					print(dat)
					print("Sleeping 1 hour")
					sleep(60 * 60 * 6) # Six hours

			# Sleep 6 secs
			print("Grabbed {0} on {1}".format(t["t"], str(current)))
			for x in dat["response"]["docs"]:
				results.append([t["t"], str(current), x["abstract"], x["headline"]["main"], x["lead_paragraph"]])
			time.sleep(6)
		# Increment
		current += daily

except Exception as e:
	print("Died at " + str(current))
	print(e.args)

pickle.dump(results, open(fn, "wb"))
