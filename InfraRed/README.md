
##  Infra-Dread   V0.2                                                          

infra-dread.py

infra-dread.py is a Python script designed for Raspberry Pi to Brute force and send infrared (IR) codes using a connected IR transmitter. The script allows you to send specific IR codes in sequence, randomize the codes, or count up from a given starting code. It provides flexibility in customizing the header pulse, header space, one pulse, one space, zero pulse, zero space, pulse trail, and gap durations, enabling compatibility with a wide range of IR devices.
How to Use:

    Hardware Setup:
        Connect an IR transmitter to the Raspberry Pi GPIO pin (specified in the transmit_pin variable) that supports hardware PWM.
        Make sure you have the necessary hardware and wiring connections to send IR signals successfully.

    Install Dependencies:
        Before using the script, ensure that the required packages are installed on your Raspberry Pi.
        The script relies on the RPi.GPIO library, which should be pre-installed on most Raspberry Pi systems. If it's not already installed, you can install it using the following command:

    bash

sudo apt-get update
sudo apt-get install python3-rpi.gpio

Run the Script:

    Save the script as infra-dread.py on your Raspberry Pi.
    Open a terminal and navigate to the directory containing the script.
    To view available options, run:

bash

python3 infra-dread.py -h

    Usage examples:

bash

    # Send a specific IR code
    python3 infra-dread.py -m 0x02A1

    # Send a specific IR code with a fixed preamble
    python3 infra-dread.py -p 0x7FFFF -m 0x02A1

    # Send a random IR code 10 times
    python3 infra-dread.py -r -x 10

    # Count up from a specific IR code
    python3 infra-dread.py -sl 0x1111

Command Line Arguments:

    -h, --help: Display help information and available arguments.
    -l, --length: Number of bits for the IR codes (default: 32).
    -r, --random: Enable random mode (default is counting-up).
    -m, --code: IR code to send in hex format (e.g., 0x02A1).
    -p, --preamble: Fixed preamble IR code to send in hex format (e.g., 0x7FFFF).
    -x, --repeat: Number of times to repeat sending the code (default: 1).
    --header_pulse: Header pulse duration in microseconds (default: 4058).
    --header_space: Header space duration in microseconds (default: 3964).
    --one_pulse: One pulse duration in microseconds (default: 514).
    --one_space: One space duration in microseconds (default: 1980).
    --zero_pulse: Zero pulse duration in microseconds (default: 514).
    --zero_space: Zero space duration in microseconds (default: 981).
    --ptrail: Pulse trail duration in microseconds (default: 514).
    --gap: Gap duration in microseconds (default: 64729).
    --frequency: Carrier frequency in Hz (default: 38000).
    --duty: Duty cycle for the PWM signal (default: 50.0).
    -sl, --start_from: Start counting up from the specified hex code.

Notes:

    The script is designed for Raspberry Pi with an IR transmitter connected to the specified GPIO pin pin 17 (change the transmit_pin variable if necessary).
    Ensure that the GPIO pin supports hardware PWM for accurate IR transmission.
    For successful IR transmission, configure the duration of the header pulse, header space, one pulse, one space, zero pulse, zero space, pulse trail, and gap according to the requirements of the target IR device. You can take a look at a lirc.conf for all vaules for arguments like header gap pulse etc....
    Use the appropriate options to send specific IR codes, randomize codes, or count up from a given starting code.
    The script does not require any additional Python packages beyond the standard RPi.GPIO library.

License:

This script is provided under the MIT License. Feel free to use, modify, and distribute it as per the terms of the MIT License.
Author:

The script is developed by Commander Crash of 29A Society

