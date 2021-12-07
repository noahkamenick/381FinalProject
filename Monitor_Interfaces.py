from datetime import datetime
import json

# Genie import
from genie.conf import Genie

# import the genie libs
from genie.libs import ops  # noqa

# Parser import
from genie.libs.parser.iosxe.show_interface import ShowIpInterfaceBrief

# Import Genie Conf

from vpnCommand import vpn_command


class MonitorInterfaces:
    def setup(self, testbed):
        genie_testbed = Genie.init(testbed)
        self.device_list = []
        str = ""
        for device in genie_testbed.devices.values():
            try:
                device.connect()
            except Exception:
                print("Failed to establish connection to '{}'".format(device.name))
                str += "\nFailed to establish connection to " + device.name

            self.device_list.append(device)

        return str

    def learn_interface_ip(self):
        self.prev = {}
        self.summ = ""
        for dev in self.device_list:  # For each device in the device list (routers.yml)
            self.parser = ShowIpInterfaceBrief(dev)
            self.curr = self.parser.parse()  # Parse current, fetched addresses and interfaces

            try:
                with open(
                    "./prevCurr/previous_ip_{name}.json".format(name=dev.hostname)
                ) as f:  # Open previous json file
                    self.prev = json.load(f)  # Load into prev object

            except:
                print("No previous file found for {name} \nCreating new file...".format(name=dev.hostname))
                with open("./prevCurr/previous_ip_{name}.json".format(name=dev.hostname), "w+") as intoFile:
                    json.dump(self.curr, intoFile)

            self.summ += self.ipAddLogic(dev.hostname)

            with open("prevCurr/previous_ip_{name}.json".format(name=dev.hostname), "w+") as intoFile:
                json.dump(self.curr, intoFile)

        return self.summ

    def ipAddLogic(self, hostname):

        text = ""

        for curr_int, curr_value in self.curr["interface"].items():

            for prev_int, prev_value in self.prev["interface"].items():

                if not "unassigned" in prev_value["ip_address"]:

                    if curr_value["ip_address"] != prev_value["ip_address"] and curr_int == prev_int:

                        text += (
                            "\n\n"
                            + curr_int
                            + " IP changed on "
                            + hostname
                            + " at {tim}".format(tim=datetime.now())
                            + "\n --Previous IP: "
                            + prev_value["ip_address"]
                            + "\n --New IP: "
                            + curr_value["ip_address"]
                        )

                    if (
                        curr_value["ip_address"] != prev_value["ip_address"]
                        and curr_int == prev_int
                        and curr_int == "GigabitEthernet2"
                        and hostname == "R2"
                    ):

                        text += vpn_command(prev_value["ip_address"], curr_value["ip_address"])
                        print("done")

        return text


if __name__ == "__main__":
    # Test Functions
    mon = MonitorInterfaces()
    mon.setup("routers.yml")
    intfl = mon.learn_interface_ip()
    print(intfl)

# Just a change to run it through CI/CD linting/formatting sorta deal
