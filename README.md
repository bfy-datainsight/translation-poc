# translation-poc
Poc for translations in thoughtspot (and generic manipulation of the .tml files)

# How to use
1. Ensure a local folder "content" is created  (this contains your input files, currently only worksheets are supported)
2. Add desired targets to the config.yml (src/configuration/config.yml). All fields (name, locale and uuid are required). UUID needs to be unique as this is what thoughtspot uses
3. Create a virtual environment and add dependences ("pip install -r requirements.txt" when in the root folder)
4. Run the main file.

# To do list
Pretty huge.
1. Support multiple config files
2. Support updating translation files (current set up is to overwrite one so you lose the existing translations when adding a new one)
3. Support encoding for special character (ö,ä,å, you get the idea).
4. Unit tests everywhere
5. Final type validations (not all type hints are accurate)
6. A whole lot more

# Formatting
If any changes are made, please use black formatter. https://github.com/psf/black