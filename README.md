# OnePasswordConverter
Convert [1pux] to [Bitwarden] CSV

1Password this new export format `1pux` which stands for `1Password Unencrypted Export` format, or `1Password User eXport`  
Currently 1Password and Bitwarden do not support importing this format  
This file is essentially a `zip` containing a few JSON files:
```
    <account UUID>.1pux
    │── export.attributes
    │── export.data
    └── files
        └── ...
```
You will need to extract this, you may need to change `.1pux` to `.zip`  
You can optionally add a `.json` to `export.data` since it is a json file  
Read more about the [1pux] format here

This program was created originally to transfer my vaults into a new account, however I have decided after a month not to use 1Password, you can [read more here](https://gist.github.com/ShayBox/177fee12bc424dfe79507cb4c827bc7d)  

This program exports to Bitwarden CSV, if there's anything missing feel free to create an issue or pull request

### Installation
- Install `Poetry` (via pip or package manager)
- Build the package: `poetry build`
- Install the package: `pip install dist/*.tar.gz`
- Run the package: `1passconv export.data`

### Development
- Install `Poetry` (via pip or package manager)
- Install dependencies: `poetry install`
- Run the package in venv: `poetry run convert`

[1pux]:https://support.1password.com/1pux-format
[Bitwarden]:https://bitwarden.com/help/article/condition-bitwarden-import