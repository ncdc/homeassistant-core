import logging

import requests

# From https://github.com/jakecrowley/AylaLocalAPI/tree/mqtt


class Device:
    def __init__(self, access_token, name, dsn, lan_ip, key, lan_enabled) -> None:
        self.name = name
        self.dsn = dsn
        self.lan_ip = lan_ip
        self.key = key
        self.lan_enabled = lan_enabled
        self.properties = getProperties(access_token, dsn)

        if lan_enabled:
            self.Lanip = getLanip(access_token, key)


def login(
    email,
    password,
    app_id="schneider-5w-id",
    app_secret="schneider-4p5If6sO_QS9F0mQLJmOoCxswng",
):
    url = "https://user-field.aylanetworks.com/users/sign_in.json"
    data = {
        "user": {
            "email": email,
            "application": {"app_id": app_id, "app_secret": app_secret},
            "password": password,
        }
    }
    response = requests.request("POST", url, json=data)
    respjson = response.json()

    if response.status_code != 200:
        logging.error("Login failed with error: {}".format(respjson["error"]))
        exit(1)

    return response.json()["access_token"]


def getDevices(access_token):
    url = "https://ads-field.aylanetworks.com/apiv1/devices.json"
    headers = {"authorization": f"auth_token {access_token}"}
    response = requests.request("GET", url, headers=headers)
    respjson = response.json()

    if response.status_code != 200:
        logging.error("Failed to get devices with error: {}".format(respjson["error"]))
        exit(1)

    devices = []
    for device in respjson:
        d = device["device"]
        devices.append(
            Device(
                access_token,
                d["product_name"],
                d["dsn"],
                d["lan_ip"],
                d["key"],
                d["lan_enabled"],
            )
        )

    return devices


def getLanip(access_token, device_id):
    url = f"https://ads-field.aylanetworks.com/apiv1/devices/{device_id}/lan.json"
    headers = {"authorization": f"auth_token {access_token}"}
    response = requests.request("GET", url, headers=headers)
    respjson = response.json()

    if response.status_code != 200:
        logging.error(
            "Failed to get lanip for device {} with error: {}".format(
                device_id, respjson["error"]
            )
        )
        exit(1)

    return respjson


def getProperties(access_token, device_serial_number):
    url = f"https://ads-field.aylanetworks.com/apiv1/dsns/{device_serial_number}/properties.json"
    headers = {"authorization": f"auth_token {access_token}"}
    response = requests.request("GET", url, headers=headers)
    respjson = response.json()

    if response.status_code != 200:
        logging.error(
            "Failed to get properties for device {} with error: {}".format(
                device_serial_number, respjson["error"]
            )
        )
        exit(1)

    return respjson
