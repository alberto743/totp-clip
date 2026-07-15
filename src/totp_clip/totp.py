#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 ENEA
# SPDX-FileContributor: Alberto P
#
# SPDX-License-Identifier: MPL-2.0

import argparse
import getpass
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


def load_services(config_filename="totp.yml"):
    config_path = Path.home() / config_filename
    if not config_path.exists():
        return {}
    with open(config_path) as config_file:
        return yaml.safe_load(config_file) or {}


def save_services(services, config_filename="totp.yml"):
    config_path = Path.home() / config_filename
    with open(config_path, "w") as config_file:
        yaml.safe_dump(services, config_file, sort_keys=False)


def prompt(question, default=None):
    suffix = f" [{default}]" if default is not None else ""
    answer = input(f"{question}{suffix}: ").strip()
    return answer or default


def prompt_bool(question, default=True):
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{question} {suffix}: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def setup_service(service_name, config_filename="totp.yml"):
    services = load_services(config_filename)

    if service_name in services and not prompt_bool(
        f"{service_name!r} already exists, overwrite?", default=False
    ):
        print("Aborted.")
        return

    remote_name = prompt("Remote name (keyring identifier)", default=service_name)
    window_title = prompt("Window title", default=service_name)
    store_clipboard = prompt_bool("Store OTP in clipboard?", default=True)
    secret = getpass.getpass("TOTP secret key: ")

    try:
        pyotp.TOTP(secret).now()
    except Exception as error:
        raise ValueError(f"invalid TOTP secret key: {error}") from error

    keyring.set_password(KEYRING_SERVICE_NAME, remote_name, secret)

    services[service_name] = {
        "remote_name": remote_name,
        "window_title": window_title,
        "store_clipboard": store_clipboard,
    }
    save_services(services, config_filename)

    print(f"{service_name!r} configured in {Path.home() / config_filename}")


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


def setup():
    parser = argparse.ArgumentParser(description='Setup a new TOTP account entry')
    parser.add_argument('service_name')
    parser.add_argument('--config_filename', default="totp.yml")
    args = parser.parse_args()

    setup_service(args.service_name, args.config_filename)
