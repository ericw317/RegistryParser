from Registry import Registry

class SYSTEMParser:
    @staticmethod
    def SYSTEM_parse(reg):
        def get_computer_name():
            path = "ControlSet001\\Control\\ComputerName\\ComputerName"
            key = reg.open(path)
            return key.value("ComputerName").value()

        def get_timezone():
            path = "ControlSet001\\Control\\TimeZoneInformation"
            key = reg.open(path)
            return key.value("TimeZoneKeyName").value()

        def get_USB_history():
            path = "ControlSet001\\Enum\\USB"
            key = reg.open(path)
            print(f"{'USB Device History':>50}")
            print(f"{'Device Name':<60} {'Time Used'}")

            # loop through all USB devices
            for device in key.subkeys():
                try:  # Look at first subkey of each device to find device name and timestamp
                    name = device.subkeys()[0].value("DeviceDesc").value()
                    name = name[name.rfind(";") + 1:]
                    print(f"{name:<60} {device.subkeys()[0].timestamp()}")
                except Registry.RegistryValueNotFoundException:
                    continue

        # output the data
        print(f"Computer Name: {get_computer_name()}\n"
              f"Timezone: {get_timezone()}\n")
        get_USB_history()
