from Registry import Registry
import re

class SAMParser:
    @staticmethod
    def SAM_parse(reg):
        def get_RID(user):
            # navigate to path of user and open the user key
            path = rf"SAM\Domains\Account\Users\Names\{user}"
            key = reg.open(path)
            RID = key.value("").value_type()  # obtain RID value
            return RID

        def get_name(RID):
            RID_hex = str(hex(RID)[2:]).upper()  # convert RID to hex
            RID_hex = RID_hex.zfill(8)  # pad RID
            path = rf"SAM\Domains\Account\Users\{RID_hex}"  # navigate to user key
            key = reg.open(path)  # open user key

            try:
                # obtain first name
                first_name = key.value("GivenName").value()  # get value for first name
                first_name = first_name.decode("utf-8")  # decode data to utf-8
                first_name = re.sub(r'[^\x20-\x7E]+', '', first_name)  # remove unreadable characters
            except Registry.RegistryValueNotFoundException:
                first_name = ""

            try:
                # obtain last name
                last_name = key.value("Surname").value()  # get value for last name
                last_name = last_name.decode("utf-8")  # decode data to utf-8
                last_name = re.sub(r'[^\x20-\x7E]+', '', last_name)  # remove unreadable characters
            except Registry.RegistryValueNotFoundException:
                last_name = ""

            if first_name == "" and last_name == "":
                return "N/A"
            else:
                return f"{first_name} {last_name}"

        def get_internet_username(RID):
            RID_hex = str(hex(RID)[2:]).upper()  # convert RID to hex
            RID_hex = RID_hex.zfill(8)  # pad RID
            path = rf"SAM\Domains\Account\Users\{RID_hex}"  # navigate to user key
            key = reg.open(path)  # open user key

            try:
                internet_username = key.value("InternetUserName").value().decode("utf-8")  # get name and decode it to utf-8
                internet_username = re.sub(r'[^\x20-\x7E]+', '', internet_username)  # remove unreadable characters
            except Registry.RegistryValueNotFoundException:
                internet_username = "N/A"

            return internet_username


        # initialize empty list to hold user data
        user_data = []

        # access a key
        key_path = r"SAM\Domains\Account\Users\Names"
        key = reg.open(key_path)

        # loop through each user and create a dictionary with their data
        for key in key.subkeys():
            RID = get_RID(key.name())
            user_dict = {"Username": key.name(),
                         "RID": RID,
                         "Name": get_name(RID),
                         "Internet Username": get_internet_username(RID)}
            user_data.append(user_dict)

        # output the data
        for users in user_data:
            print(f"Username: {users['Username']}\n"
                  f"RID: {users['RID']}\n"
                  f"Name: {users['Name']}\n"
                  f"Internet Username: {users['Internet Username']}\n")
            print("------------------------------\n")
