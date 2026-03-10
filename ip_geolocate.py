import csv
import json
import time
import urllib.request

INPUT_FILE = "ips.csv"
OUTPUT_FILE = "ip_countries.csv"

FIELDS = [
    "query",                        # IP address
    "status", "message",            # success / error info
    "continent", "continentCode",   # e.g. North America, NA
    "country", "countryCode",       # e.g. United States, US
    "region", "regionName",         # e.g. CA, California
    "city", "district", "zip",      # e.g. Mountain View, 94043
    "lat", "lon",                   # coordinates
    "timezone", "offset",           # e.g. America/Los_Angeles, -25200
    "currency",                     # e.g. USD
    "isp", "org",                   # e.g. Google, Google LLC
    "as", "asname",                 # e.g. AS15169 Google Inc., GOOGLE
    "mobile", "proxy", "hosting",   # boolean flags
]

# Read IPs from first column of CSV
with open(INPUT_FILE, encoding="utf-8") as f:
    ips = [row[0].strip() for row in csv.reader(f) if row]

# Look up in batches of 100 (ip-api.com limit)
results = []
for i in range(0, len(ips), 100):
    batch = ips[i:i+100]
    payload = json.dumps([{"query": ip} for ip in batch]).encode()
    url = "http://ip-api.com/batch?fields=" + ",".join(FIELDS)
    req = urllib.request.Request(url, data=payload)
    with urllib.request.urlopen(req) as resp:
        results += json.loads(resp.read())
    print(f"Processed {min(i+100, len(ips))}/{len(ips)}")
    time.sleep(1.5)  # stay under 45 req/min free tier limit

# Write results
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(results)

print(f"Done! Results saved to {OUTPUT_FILE}")
