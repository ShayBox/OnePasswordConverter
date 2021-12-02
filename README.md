# 1PasswordConverter
Convert .1pux to .csv

1Password uses this new export format `.1pux`, I assume stands for `1 Password User eXport`.  
As of right now, 1Password doesn't support importing their new export format...  
This process is lossy, it only converts `Title/Name`, `URL`, `Username`, and `Password`.  
This program only extracts this data because 1Password also doesn't support importing anything but those columns,  
So if you have other data such as TOTP, files, documents, etc, you will need to manually recreate it.  
Expansion on this program to export other data for other password managers is welcomed.  

### Installation
- Install `Poetry` (via pip or package manager)
- Build the package: `poetry build`
- Install the package: `pip install dist/*.tar.gz`
- Run the package: `convert`

### Development
- Install `Poetry` (via pip or package manager)
- Install dependencies: `poetry install`
- Run the package in venv: `poetry run convert`