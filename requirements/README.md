# Auto update requirements

This script automatically updates the packages listed in a requirements file to their latest versions. Update the requirements file only, not install the packages.

The import end with `NO-UPDATE` comment will be ignored during the update process.

# Quickstart
```
python update_requirements.py <path_to_requirements_file, default: requirements.txt>
```