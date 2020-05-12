#!/usr/bin/env python

import json
from sdwanAPI import sdwanAPI
from pprint import pprint


def main():

    sdwan = sdwanAPI.sdwanAPI('admin', 'WWTwwt1!', '10.246.2.159', port='443')
    # sdwan = sdwanAPI('devnetuser','Cisco123!','sandboxsdwan.cisco.com')

    # devices
    users = sdwan.get_user()
    print(users)
    pprint(users.json()['data'])

    # Create Users
    with open("vars/users.json", "r") as file:
        stream = file.read()
        users = json.loads(stream)
        # print(users)
        for user in users["users"]:
            # print(user)
            sdwan.create_user(user)

    # Delete User
    result = sdwan.delete_user("jandiorio2")
    print(result, result.text)

    # Update User
    user_data = {"userName": "jandiorio", "password": "Cisco123!"}
    results = sdwan.update_password(data=user_data)
    print(results, results.status_code, results.text)


if __name__ == "__main__":
    main()
