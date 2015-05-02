#!/usr/bin/env python3

from pprint import pprint
import arrow
import sys
import json

def main(argv):
  timezone = "CET"
  members = json.load(sys.stdin)
  members.sort(key = lambda member: member['joined'])

  count = 0
  last_bucket = None
  buckets = {}

  for member in members:
    joined = arrow.get(member['joined']/1000).to(timezone)
    bucket = joined.replace(hour=0, minute=0, second=0)

    if last_bucket and last_bucket != bucket:
      buckets[last_bucket.timestamp] = count

    count += 1
    last_bucket = bucket

  print(json.dumps(buckets, indent=2))


if __name__ == "__main__":
  main(sys.argv[1:])