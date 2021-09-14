#!/usr/bin/env python
import subprocess
import optparse
import re

def getArguements():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC Address")
    parser.add_option("-m", "--mac", dest="newMac", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.newMac:
        parser.error("[-] Please specify a new MAC, use --help for more info.")
    return options

def macChanger(interface, newMac):
    print("[+] Changing MAC address for: " + interface + ", to: " + newMac)
    # Secure
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newMac])
    subprocess.call(["ifconfig", interface, "up"])
    # Unsecure
    # subprocess.call("ifconfig " + interface + " down", shell=True)
    # subprocess.call("ifconfig " + interface + " hw ether " + newMac, shell=True)
    # subprocess.call("ifconfig " + interface + " up", shell=True)

def getCurrentMac(interface):
    ifconfigResult = subprocess.check_output(["ifconfig", interface])
    macAddressSearchResult = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfigResult)
    if macAddressSearchResult:
        return macAddressSearchResult.group(0)
    else:
        return "[-] Could not get MAC Address."

options = getArguements()

currentMac = getCurrentMac(options.interface)
print("Current MAC: " + currentMac)

if currentMac == "[-] Could not get MAC Address.":
    print("You have selected an interface that has no MAC Address.")
else:
    macChanger(options.interface, options.newMac)

currentMac = getCurrentMac(options.interface)
if currentMac == options.newMac:
    print("[+] MAC Address was successfully changed to " + currentMac)
else:
    print("[-] MAC Address did not change.")


