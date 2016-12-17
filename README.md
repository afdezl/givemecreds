# givemecreds

**givemecreds** is a simple python script to retrieve and store AWS STS credentiale.

It is thought to be used where a logging account is configured or to provide STS credentials to other tools like *test-kitchen*.


The script is managed by a configuration file `sessionconfig.yml` that allows to set up multiple profiles to quickly assume different roles in one or multiple accounts.

**NOTE: It is recommended to make a copy of your `~/.aws/config` file before proceeding with this script.**


## Usage

```bash
./givemecreds.py <session>
```

Alternatively it can be sourced via an alias in your `.zshrc` or `.bashrc`:

```bash
alias givemecreds="/path/to/givemecreds.py"
```

The script also supports exporting the generated profile as the AWS_DEFAULT_PROFILE:

```bash
givemecreds <session> --export-profile
```

## Profiles Setup

```
sessions:
  <session>:                          
    account: 012345678910
    role: read-only
    source_profile: <source_profile>        
    target_profile: <target_profile>
  staging:
    account: 109876543210
    role: super-admin
    source_profile: <source_profile>
  development:
    account: 567891001234
    role: developer
    source_profile: <source_profile>
```

Where:

* `<session>` **[REQUIRED]** is simply the name of the session to be called via `$ givemecreds <session>`
* `account` **[REQUIRED]** is the account in which the STS session is assumed
* `role` **[REQUIRED]** is the role that is being targeted in the account
* `source_profile` **[REQUIRED]** is the profile configured in your `~/.aws/config` that has assume role capabilites in the destination account.
* `target` **[OPTIONAL]** is an empty profile within the `~/.aws/config` that contains the basic STS required keys and that will be populated by the script. This should be setup if the generated credentials are to be used with other tools.


`~/.aws/config`
```bash
[profile source_profile]
region = eu-west-1
mfa_serial = ...
output = json
```

Upon first setup, the target profile must be configured as follows in your `~/.aws/config`:


```bash
[profile <target_profile>]
aws_access_key_id =
aws_secret_access_key =
aws_session_token =
```
