#!/usr/bin/env python

import requests
import json
import tabulate
import datetime
import click
import sys


class sdwanAPI:
    def __init__(
        self, username, password, vmanage, port="8443", version=19, verify=False
    ):
        self.username = username
        self.password = password
        self.vmanage = vmanage
        self.version = version
        self.base_url = f"https://{vmanage}:{port}"
        self.session = None
        self.verify = verify

        self.login()

    def login(self):
        """instance method to log in to the vManage node
        """

        endpoint = "/j_security_check"
        auth_url = f"{self.base_url}{endpoint}"

        credentials = {"j_username": self.username, "j_password": self.password}

        HEADERS = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-XSRF-TOKEN": "",
        }

        self.session = requests.session()

        response = self.session.post(
            auth_url, data=credentials, headers=HEADERS, verify=False
        )

        if response.status_code != 200 or "<html>" in response.text:
            print("login failed.")
            sys.exit()
        else:
            print(f"login succeeded.  JSESSIONID: {response.cookies['JSESSIONID']}")

        if self.version >= 19:
            token_endpoint = "/dataservice/client/token"
            token = self._request("get", token_endpoint).text
            self.session.headers["X-XSRF-TOKEN"] = token

    def _request(self, method, endpoint, data=None, params=None, print_rsp=True):
        """internal method used to make the Requests.request call to the target

        Arguments:
            method {str} -- [CRUD operation.  put, post, get, delete]
            endpoint {[str]} -- [REST endpoint portion of the URL (everything after the port)]

        Keyword Arguments:
            data {[obj]} -- [the payload data for calls requiring it] (default: {None})
            params {[type]} -- [description] (default: {None})
            print_rsp {bool} -- [description] (default: {True})

        Returns:
            [type] -- [description]
        """

        self.session.headers["Content-Type"] = "application/json"

        _url = f"{self.base_url}{endpoint}"
        result = self.session.request(
            method, _url, json=data, params=params, verify=self.verify
        )

        if print_rsp:
            print(f"API CALL STATUS CODE: {str(result.status_code)}")

        return result

    def build_table(self, header, data):
        row_data = []

        # row_data.append(header_keys)
        for d in data:
            row = []
            for key in header:
                row.append(d[key])
            row_data.append(row)

        print(tabulate.tabulate(row_data, headers=header, tablefmt="fancy_grid"))

        return row_data

    # @click.group()
    # def cli(self):
    #     pass

    # @click.command()
    def get_device_list(self):
        print("Retrieving device list.")
        endpoint = "/dataservice/device"
        results = self._request("get", endpoint, print_rsp=False)
        if results.ok:
            print("Successfully retrieved device list.")
            devices = results.json()["data"]
            return devices

        else:
            print(f"Failed to retrieve device list. {results.text}")
            results.raise_for_status()

    def get_device_status(self):
        pass

    def get_events(self, query=None):
        """ Retrieve Events

        Keyword Arguments:
            query {[dict]} -- [Viptela query dictionary.] (default: {None})

        Returns:
            [Response] -- [Response object from call.]
        """

        endpoint = f"/dataservice/event"
        results = self._request(method="post", endpoint=endpoint, data=query)

        if results.ok:
            print("Successfully retrieved events.")
            return results
        else:
            print("Failed to retrieve events.")
            return results

    def get_capacity(self):
        print("getting capacity")
        endpoint = "/dataservice/capacity"

        results = self._request("get", endpoint)

        if results.ok:
            capacity = results.json()["data"]
            return capacity

    def get_vsmart_certificate_list(self):

        print("getting vsmart certificate list")
        endpoint = "/dataservice/certificate/vsmart/list"
        results = self._request(endpoint)
        if results.ok:
            print(results.json()["data"])
            return results

    # cli.add_command(get_device_list)

    def create_user(self, user):
        """
        Crete a user
        if user exists already a 500 error is returned
        """

        endpoint = "/dataservice/admin/user"
        usernames = [u["userName"] for u in self.get_user().json()["data"]]

        if user["userName"] not in usernames:
            results = self._request(method="post", endpoint=endpoint, data=user)

        else:
            print("user already exists...exiting")
            sys.exit()

        if results.ok:
            print(f"Created User {user['userName']}")
            return results
        else:
            print(f"failed to create user.  {results.text}")

    def get_user(self, username=None, params=None):
        """ get a list of users"""

        endpoint = "/dataservice/admin/user"

        results = self._request(method="get", endpoint=endpoint, params=params)

        if results.ok:
            print("Retrieved users...")
            return results

    def delete_user(self, username):

        print(f"Deleting user {username}")

        endpoint = f"/dataservice/admin/user/{username}"
        results = self._request(method="delete", endpoint=endpoint)

        if results.ok:
            print(f"Successfully deleted {username}")
        else:
            print(f"Unable to delete username {username}:  {results.text}")

        return results

    def update_password(self, data):

        endpoint = f"/dataservice/admin/user/password/{data['userName']}"

        results = self._request(method="put", endpoint=endpoint, data=data)

        if results.ok:
            print(f"Successfully updated user {data['userName']}")
            return results
        else:
            print(f"Failed to update user {data['userName']}")
            return results

    def get_alarms(self, params):

        endpoint = f"/dataservice/alarms"

        results = self._request(method="post", endpoint=endpoint, data=params)

        if results.ok:
            print("Retrieved alarms.")
            return results
        else:
            print("Failed to get alarms.")
            return results.raise_for_status()

    def get_device_status(self):

        pass

    def get_device_sla(self, device_id):

        endpoint = f"/dataservice/device/app-route/statistics"
        params = {"deviceId": device_id}
        results = self._request(method="get", endpoint=endpoint, params=params)
        if results.ok:
            print(f"Successfully retrieved device SLA for {device_id}")
            return results.json()["data"]

    def get_template_list(self):
        """ get a list of templates"""

        endpoint = f"/dataservice/template/device"
        results = self._request(method="get", endpoint=endpoint)
        if results.ok:
            print("Successfully retrieved the templates list.")
            return results.json()["data"]
        else:
            print("Failed to retrieve templates list.")
            print(f"Status Code: {results.status_code}")
            print(f"Error:  {results.text}")

    def get_feature_templates(self):
        """ get all feature templates"""

        endpoint = f"/dataservice/template/feature"
        results = self._request(method="get", endpoint=endpoint)
        if results.ok:
            print("Successfully retrieved the feature templates list.")
            return results.json()["data"]
        else:
            print("Failed to retrieve templates list.")
            print(f"Status Code: {results.status_code}")
            print(f"Error:  {results.text}")


    def get_attached_devices(self, template_id):
        """ retrieve what devices are attached to a template"""
        endpoint = f"/dataservice/template/device/config/attached/{template_id}"
        results = self._request(method="get", endpoint=endpoint)
        if results.ok:
            return results.json()["data"]
        else:
            print("Failed to retrieve templates list.")
            print(f"Status Code: {results.status_code}")
            print(f"Error:  {results.text}")


if __name__ == "__main__":

    sdwan = sdwanAPI("admin", "WWTwwt1!", "10.246.2.159", port="443")
    # sdwan = sdwanAPI('devnetuser','Cisco123!','sandboxsdwan.cisco.com')
    # devices
    devices = sdwan.get_device_list()
    # devices = results.json()['data']
    header_keys = ["host-name", "deviceId", "system-ip", "version"]
    sdwan.build_table(header_keys, devices)

    # get certificate vsmart list
    # vsmart_certs = sdwan.get_vsmart_certificate_list()

    # features templates
    # endpoint = '/dataservice/template/feature'
    # results = sdwan._request(endpoint)
    # fts = results['data']
    # header_keys = ['templateName','templateDescription', 'templateType', 'createdBy', 'devicesAttached']
    # sdwan.print_table(header_keys,fts)
