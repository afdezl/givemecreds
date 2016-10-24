# givemecreds

**givemecreds** is a simple python script to get temporary sts credentials added into an aws config file.

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


### Config structure

```yaml
sessions:
  production_read:                          #<session>
    account: 012345678910
    role: read-only
    source_profile: <source_profile>        # Profile with assume role access into the account
    target_profile: <target_profile>        # Destination profile in aws config file
  staging:
    account: 109876543210
    role: super-admin
    source_profile: <source_profile>
  development:
    account: 567891001234
    role: developer
    source_profile: <source_profile>
```

The structure of the aws crendentials and config files result in:

`~/.aws/config`
```bash
[source_profile]
region = eu-west-1
mfa_serial = ...
output = json
```

`~/.aws/config`
```bash
[profile target_profile]
aws_access_key_id = ...
aws_secret_access_key = ...
aws_session_token = ...
```
