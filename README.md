<!--
SPDX-FileCopyrightText: Copyright © 2025 ENEA
SPDX-FileContributor: Alberto P

SPDX-License-Identifier: MPL-2.0
-->

# TOTP-CLIP

Generate TOTP authentication code for 2FA from a configuration stored in a YAML file with secrets in netrc format and copy it to the clipboard.

## Configuration (YAML)
Defaults to `~/totp.yml`.
``` yaml
service_name:
  remote_name: machine item in netrc
  window_title: title of the window showing the OTP
  store_clipboard: Boolean option to either store the OTP in the clipboard
```

## Secret storage (netrc).
Defaults to `~/.netrc`.
``` shell
machine remote_name in corresponding YAML
	login username as show by the TOTP provider
	password secret key provided during the setup of the two-factor authentication
```

Please assure that only the local user may read this file.
