import re

class ManualViewer:
    @staticmethod
    def manual_view(reg, key, key_path):
        while True:
            # print current path
            print(f"Current path: {key_path}")

            # print the subkeys
            print("Subkeys:")
            for key in key.subkeys():
                print(key.name())

            print("")

            # print values
            print("Values:")
            for value in key.values():
                try:
                    print(f"Value Name: {value.name()}\n"
                          f"Value: {re.sub(r'[^\x20-\x7E]+', '', value.value().decode("utf-8"))}")
                except:
                    print(end="")

            print("")

            # take navigation input
            while True:
                key_input = input("")
                if key_input == "back" or key_input == "0":
                    break
                try:
                    reg.open(f"{key_path}\\{key_input}")
                    break
                except:
                    print("Invalid input. Try again.\n")

            if key_input == "back":
                if key_path != "SAM":
                    while True:
                        if key_path[-1] == "\\":
                            key_path = key_path[:-1]
                            break
                        else:
                            key_path = key_path[:-1]
                key = reg.open(key_path)
            elif key_input == "0":
                break
            else:
                key_path += f"\\{key_input}"
                key = reg.open(key_path)
