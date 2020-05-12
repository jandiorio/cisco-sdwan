#!/usr/bin/env python

import json
from sdwanAPI import sdwanAPI
from pprint import pprint


def main():

    sdwan = sdwanAPI.sdwanAPI('admin', 'WWTwwt1!', '10.246.2.159', port='443')
    # sdwan = sdwanAPI('devnetuser','Cisco123!','sandboxsdwan.cisco.com')

    # devices
    devices = sdwan.get_device_list()
    vedges = [device['deviceId'] for device in devices if device['device-type'] == 'vedge']

    for vedge in vedges:
        sla_data = sdwan.get_device_sla(vedge)
        pprint(sla_data)


if __name__ == "__main__":
    main()
