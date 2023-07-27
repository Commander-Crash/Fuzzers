
##  Infra-Dread                                                             

                                                              

The IR script is a Python script designed to send IR codes using a Raspberry Pi and its GPIO pins. It allows you to send individual IR codes or a sequence of random IR codes. The script uses Raspberry Pi 4 GPIO library, RPi.GPIO, to control the GPIO pins for generating the IR signals.
GPIO 17 is set for transmitter can be changed in script.
How to Use the IR Script:

    Connect IR Transmitter:
    Before using the script, you need to connect an IR transmitter to one of the GPIO pins of the Raspberry Pi. 
    The script assumes that you have connected the IR transmitter to GPIO pin 17, but you can modify the transmit_pin variable in the script to match your wiring configuration.

    Command Line Arguments:
    The script can be run from the command line with various arguments to control its behavior. Here are the available arguments:
        -l, --length: The number of bits for the IR codes. Default is 32.
        -r, --random: Enable random mode (default is counting-up).
        -m, --code: Send a specific IR code in hex format (e.g., 0x02A1).
        -x, --repeat: Number of times to repeat sending the code. Default is 1.
        --header_pulse, --header_space, --one_pulse, --one_space, --zero_pulse, --zero_space, --ptrail, --gap: Customize the duration of various IR signal components (in microseconds).
        --frequency: Carrier frequency for the IR signals (in Hz). Default is 38000 Hz.
        --duty: Duty cycle for the PWM signal (default: 50.0).

    Sending Fixed IR Code:
    To send a specific IR code, use the -m or --code argument followed by the desired hex code. For example:
    python Infra-Dread.py -m 0x7E000000

Sending Random IR Codes:
To send random IR codes, use the -r or --random argument. By default, it will send 100 million random codes. You can modify the number of random codes sent with the -x or --repeat argument. For example:
    python Infra-Dread.py -r -x 10

Customize IR Signal Parameters:
You can customize the duration of various components of the IR signal using the --header_pulse, --header_space, --one_pulse, --one_space, --zero_pulse, --zero_space, --ptrail, and --gap arguments. 
Look at a LIRC conf file to get the info for remote needed. For example:
    python Infra-Dread.py --header_pulse 4500 --header_space 4500 --one_pulse 600 --one_space 1600 --zero_pulse 600 --zero_space 500 --ptrail 600 --gap 40000

Pre-data Code:
If your IR protocol requires a pre-data code, you can include it using the -p argument followed by the desired hex code. For example:
    python Infra-Dread.py -p 0xA25D -m 0x7E000000

For Black and decker fan brute force:
    python Infra-Dread.py --header_pulse 1271 --header_space 402 --one_pulse 1272 --one_space 429 --zero_pulse 413 --zero_space 1260 --ptrail 1245 --gap 429--header_pulse 1271 --header_space 402 --one_pulse 1272 --one_space 429 --zero_pulse 413 --zero_space 1260 --ptrail 1245 --gap 429 --frequency 38000 -r -l 16

