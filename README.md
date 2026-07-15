<!--
SPDX-FileCopyrightText: 2025 ENEA
SPDX-FileContributor: Alberto P

SPDX-License-Identifier: MPL-2.0
-->

# TOTP-CLIP

Generate TOTP authentication code for 2FA from a configuration stored in a YAML file with secrets in the system keyring and copy it to the clipboard.

## Configuration (YAML)
Defaults to `~/totp.yml`.
``` yaml
service_name:
  remote_name: identifier used to look up the secret in the keyring
  window_title: title of the window showing the OTP
  store_clipboard: Boolean option to either store the OTP in the clipboard
```

## Secret storage (keyring)
Secrets are stored in the OS-native keyring (e.g. Secret Service on Linux, Keychain on macOS, Credential Locker on Windows) via the [keyring](https://github.com/jaraco/keyring) library, under the service name `totp-clip`.

The `keyring` command line tool is used to store secrets, install it with:
``` shell
pipx install keyring
```

Store the secret key provided during the setup of the two-factor authentication with:
``` shell
keyring set totp-clip remote_name
```
where `remote_name` matches the corresponding entry in the YAML configuration.

## Installation

``` shell
pipx install totp-clip
```

## Usage

``` shell
totp-clip service_name
```

A shortcut may be manually created to launch the command mentioned.
