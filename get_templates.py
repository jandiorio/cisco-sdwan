#!/usr/bin/env python

import json
from sdwanAPI import sdwanAPI
from pprint import pprint


def main():

    sdwan = sdwanAPI.sdwanAPI('admin', 'WWTwwt1!', '10.246.2.159', port='443')
    # get events

    templates = sdwan.get_template_list()
    feature_templates = sdwan.get_feature_templates()

    with open("output/all_templates.json", "w") as file:
        file.write(json.dumps(templates))

    with open("output/feature_templates.json", "w") as file:
        file.write(json.dumps(feature_templates))
>
    devices_attached = sdwan.get_attached_devices("4708dc57-3753-401e-9a59-b21a52cf588f")
    print(devices_attached)


if __name__ == "__main__":
    main()
