from Registry import Registry
from SAM_parser import SAMParser
from manual_view import ManualViewer
from SYSTEM_parser import SYSTEMParser
import sys

# ask user for registry hive type
registry_type = input("Which type of registry hive are you reading?\n"
                      "1) SAM\n"
                      "2) SYSTEM\n"
                      "0) Exit\n")

# input validation
while not registry_type.isnumeric() or int(registry_type) < 0 or int(registry_type) > 2:
    registry_type = input("Input must be a number between 0-2.\n")

if int(registry_type) == 0:
    sys.exit(0)
else:
    key_path = ""

# open the registry hive
while True:
    try:
        reg = Registry.Registry(input("Enter the path to the registry file: "))
        break
    except FileNotFoundError:
        print("Error opening file. Try again: ")

# access key
key = reg.open(key_path)

# ask user to input operation type
operation = input("Would you like to manually view this hive or automatically parse the data?\n"
                  "1) Look through manually\n"
                  "2) Automatically parse data\n"
                  "0) Exit\n")

# input validation
while not operation.isnumeric() or int(operation) < 0 or int(operation) > 2:
    operation = input("Input must be a number between 0-2: ")

if int(operation) == 1:
    ManualViewer.manual_view(reg, key, key_path)
elif int(operation) == 2:
    if int(registry_type) == 1:
        SAMParser.SAM_parse(reg)
    elif int(registry_type) == 2:
        SYSTEMParser.SYSTEM_parse(reg)
