#!/usr/bin/env python

from sdwanAPI import sdwanAPI
from pprint import pprint


def main():

    sdwan = sdwanAPI.sdwanAPI('admin', 'WWTwwt1!', '10.246.2.159', port='443')
    # get events
    query = {
        "query": {
            "condition": "AND",
            "rules": [
                {
                    "value": [
                        "6"
                    ],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "last_n_hours"
                }
            ]
        },
        "size": 10000
        }

    event_results = sdwan.get_events(query)
    if event_results.ok:
        pprint(event_results.json()['data'])
    else:
        print("failed")

if __name__ == "__main__":
    main()
