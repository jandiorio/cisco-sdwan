#!/usr/bin/env python

from sdwanAPI import sdwanAPI
from pprint import pprint


def main():

    sdwan = sdwanAPI.sdwanAPI('admin', 'WWTwwt1!', '10.246.2.159', port='443')
    # get alarms
    body = {
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

    # {
    #     "query": {
    #         "condition": "AND",
    #         "rules": [
    #             {
    #                 "value": [
    #                     "3"
    #                 ],
    #                 "field": "entry_time",
    #                 "type": "date",
    #                 "operator": "last_n_hours"
    #             },
    #             {
    #                 "value": [
    #                     "Critical"
    #                 ],
    #                 "field": "severity",
    #                 "type": "string",
    #                 "operator": "in"
    #             }
    #         ]
    #     }
    # }
    alarm_results = sdwan.get_alarms(body)
    pprint(alarm_results.json()['data'])


if __name__ == "__main__":
    main()
