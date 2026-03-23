<!--
SPDX-FileCopyrightText: Copyright © 2025 ENEA
SPDX-FileContributor: Alberto P

SPDX-License-Identifier: MPL-2.0
-->

# TOTP GUI

Create TOTP authentication code for 2FA and copy it to the clipboard.

## Configuration

### .netrc

Add the following authentication information in the `.netrc` in the root of the home directory, according the the information provided during the setup of the two-factor authentication.

``` Bash
machine website.tld
	login username.or.email
	password authentication.key.2fa
```

Please assure that only the local user may read this file.

### topt.yml

``` yaml
service_name:
  remote_name: website.tld              # shall match machine entry in netrc
  window_title: Title of GUI window
  store_clipboard: true                 # whether to store OTP in the clipboard
```
