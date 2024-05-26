
##  Infra-Dread PIGPIO  v1.4                                                          

infra-dread is a Python script designed for Raspberry Pi to Brute force and send infrared (IR) codes using a connected IR transmitter. The script allows you to send specific IR codes in sequence, randomize the codes, or count up from a given starting code. It provides flexibility in customizing the header pulse, header space, one pulse, one space, zero pulse, zero space, pulse trail, and gap durations, enabling compatibility with a wide range of IR devices.

Hardware Setup:
        Connect an IR transmitter to the Raspberry Pi GPIO pin (specified in the transmit_pin variable) that supports hardware PWM.
        Make sure you have the necessary hardware and wiring connections to send IR signals successfully.

Install Dependencies:
        Before using the script, ensure that the required packages are installed on your Raspberry Pi.
        The script relies on the RPi.GPIO library, which should be pre-installed on most Raspberry Pi systems. If it's not already installed, you can install it using the following command:
```
sudo apt-get update
sudo apt-get install python3-rpi.gpio
sudo apt-get install pigpio
```
Run the Script:

 Save the script on your Raspberry Pi. (Only tested with a raspberry pi)
 Open a terminal and navigate to the directory containing the script.
 To view available options, run:


Command Line Arguments:
```
infra-dread  --help

  _____        __                  _____                     _
 |_   _|      / _|                |  __ \                   | |
   | |  _ __ | |_ _ __ __ _ ______| |  | |_ __ ___  __ _  __| |
   | | | '_ \|  _| '__/ _` |______| |  | | '__/ _ \/ _` |/ _` |
  _| |_| | | | | | | | (_| |      | |__| | | |  __/ (_| | (_| |
 |_____|_| |_|_| |_|  \__,_|      |_____/|_|  \___|\__,_|\__,_|


usage: infra-dread [-h] [--gpio GPIO] [--recv_gpio RECV_GPIO] [-l LENGTH] [-r] [-m CODE] [-p PREAMBLE] [-x REPEAT] [--header_pulse HEADER_PULSE] [--header_space HEADER_SPACE]
                   [--one_pulse ONE_PULSE] [--one_space ONE_SPACE] [--zero_pulse ZERO_PULSE] [--zero_space ZERO_SPACE] [--ptrail PTRAIL] [--gap GAP] [--frequency FREQUENCY] [--duty DUTY]
                   [-sl START_FROM] [-v {b,h}] [--receive] [--replay]

Send and receive IR codes.

optional arguments:
  -h, --help            show this help message and exit
  --gpio GPIO           GPIO pin number for sending IR (default: 18).
  --recv_gpio RECV_GPIO
                        GPIO pin number for receiving IR.
  -l LENGTH, --length LENGTH
                        Number of bits for the IR codes (default: 32).
  -r, --random          Enable random mode (default is counting-up).
  -m CODE, --code CODE  IR code to send in hex format (e.g., 0x02A1).
  -p PREAMBLE, --preamble PREAMBLE
                        Fixed preamble IR code to send in hex format (e.g., 0x7FFFF).
  -x REPEAT, --repeat REPEAT
                        Number of times to repeat sending the code (default: 1).
  --header_pulse HEADER_PULSE
                        Header pulse duration (microseconds, default: 4058).
  --header_space HEADER_SPACE
                        Header space duration (microseconds, default: 3964).
  --one_pulse ONE_PULSE
                        One pulse duration (microseconds, default: 514).
  --one_space ONE_SPACE
                        One space duration (microseconds, default: 1980).
  --zero_pulse ZERO_PULSE
                        Zero pulse duration (microseconds, default: 514).
  --zero_space ZERO_SPACE
                        Zero space duration (microseconds, default: 981).
  --ptrail PTRAIL       Pulse trail duration (microseconds, default: 514).
  --gap GAP             Gap duration (microseconds, default: 64729).
  --frequency FREQUENCY
                        Carrier frequency (Hz, default: 38000).
  --duty DUTY           Duty cycle for the PWM signal (default: 50.0).
  -sl START_FROM, --start_from START_FROM
                        Start counting up from the specified hex code.
  -v {b,h}, --view_mode {b,h}
                        View mode: binary ('b') or hexadecimal ('h').
  --receive             Enable receiving mode to capture IR signals.
  --replay              Enable replay mode to capture and resend an IR signal.
```


LIRC conf file to get info on remote to bruteforce
```
  bits           24
  flags SPACE_ENC|CONST_LENGTH
  eps            30
  aeps          100

  header       4058  3964
  one           514  1980
  zero          514   981
  ptrail        514
  gap          64729
```
So command will be
```
python3 infra-dread.py --header_pulse 4058 --header_space 3964 --one_pulse 514 --one_space 1980 --zero_pulse 514 --zero_space 981 --ptrail 514 --gap 64729 -l 24
```
or
```
python3 infra_dread.py --receive --gpio <recv_gpio>

Waiting to receive IR signal... Press Ctrl+C to stop.
Received 71 pulses so far
Received 71 pulses so far
^C
IR signal received:
[9065, -4585, 535, -605, 540, -625, 515, -606, 590, -579, 540, -545, 545, -625, 565, -575, 540, -605, 535, -1720, 540, -1721, 534, -1720, 540, -1720, 565, -575, 540, -1745, 515, -1720, 560, -1671, 539, -625, 565, -1696, 539, -600, 540, -605, 516, -625, 514, -630, 590, -575, 515, -601, 519, -1740, 541, -600, 539, -1720, 541, -1739, 515, -1720, 535, -1721, 514, -1770, 515, -1715, 540, -41420, 9040, -2325, 565]
Extracted Signal Parameters:
header_pulse: 9065 microseconds
header_space: 4585 microseconds
one_pulse: 565 microseconds
one_space: 575 microseconds
zero_pulse: 540 microseconds
zero_space: 605 microseconds
ptrail: 565 microseconds
gap: 2325 microseconds
bit_count: 34 microseconds
```
```
python3 infra-dread.py --header_pulse 9065 --header_space 4585 --one_pulse 565 --one_space 5575 --zero_pulse 540 --zero_space 605 --ptrail 565 --gap 2325 -l 32
```
Notes:
    The script is designed for Raspberry Pi with an IR transmitter connected to the specified GPIO pin 17 (change the transmit_pin variable if necessary).
    Ensure that the GPIO pin supports hardware PWM for accurate IR transmission.
    For successful IR transmission, configure the duration of the header pulse, header space, one pulse, one space, zero pulse, zero space, pulse trail, and gap according to the requirements of the target IR device. You can take a look at a lirc.conf remote file for all vaules for arguments like header gap pulse etc....
    Use the appropriate options to send specific IR codes, randomize codes, or count up from a given starting code.
    The script does not require any additional Python packages beyond the standard RPi.GPIO library.
    test mode is still under dev. Timings may be off adjust gap by takeing or adding 1000ms to it.

License:

This script is provided under the MIT License. Feel free to use, modify, and distribute it as per the terms of the MIT License.
Author:

The script is developed by Commander Crash of 29A Society

