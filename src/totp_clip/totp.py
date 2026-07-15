#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 ENEA
# SPDX-FileContributor: Alberto P
#
# SPDX-License-Identifier: MPL-2.0

import argparse
from pathlib import Path
import keyring
from tkinter import Tk
from tkinter.ttk import Label, Button
import yaml
import pyotp
import pyperclip

KEYRING_SERVICE_NAME = "totp-clip"


def retrieve_configuration(service_name, config_filename="totp.yml"):
    with open(Path.home() / config_filename) as config_file:
        services = yaml.safe_load(config_file)
    return services[service_name]


def generate_topt(remote_name):
    key = keyring.get_password(KEYRING_SERVICE_NAME, remote_name)
    if key is None:
        raise ValueError(
            f"no secret found in the keyring for {remote_name!r} "
            f"(service {KEYRING_SERVICE_NAME!r})"
        )
    totp = pyotp.TOTP(key)
    return totp.now()


def display_totp(mytotp, window_title, store_clipboard=True):
    window = Tk()
    window.title = window_title

    label = Label(text=mytotp, font=('TkDefaultFont', 24))
    label.pack()
    if store_clipboard:
        pyperclip.copy(mytotp)
        pyperclip.paste()

    window.after(2000,lambda:window.destroy())
    window.mainloop()


def main():
    parser = argparse.ArgumentParser(description='Generate TOTP from configuration')
    parser.add_argument('service_name')
    parser.add_argument('--config_filename', default="totp.yml")
    args = parser.parse_args()

    config = retrieve_configuration(args.service_name, args.config_filename)
    totp = generate_topt(config['remote_name'])
    display_totp(totp, config['window_title'], config['store_clipboard'])
