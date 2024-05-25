#!/usr/bin/env python3

# By Commander Crash of 29A Society
# Infra Dread v1.0

import random
import time
import argparse
import pigpio  # Import pigpio library

RED = "\033[91m"  # Red color
GREEN = "\033[92m"  # Green color
YELLOW = "\033[93m"  # Yellow color
WHITE = "\033[0m"  # White color (reset)

# Message of the Day (motd) in red
motd = f"""{RED}
  _____        __                  _____                     _ 
 |_   _|      / _|                |  __ \                   | |
   | |  _ __ | |_ _ __ __ _ ______| |  | |_ __ ___  __ _  __| |
   | | | '_ \|  _| '__/ _` |______| |  | | '__/ _ \/ _` |/ _` |
  _| |_| | | | | | | | (_| |      | |__| | | |  __/ (_| | (_| |
 |_____|_| |_|_| |_|  \__,_|      |_____/|_|  \___|\__,_|\__,_|
                                                               

{WHITE}"""
print(motd)

pi = pigpio.pi()  # Initialize pigpio

def send_ir_code(code, code_length, header_pulse, header_space, one_pulse, one_space, zero_pulse, zero_space, ptrail, gap, view_mode, pwm):
    if view_mode == 'b':
        print(f"{GREEN}Sending IR code (binary): {bin(code)}{WHITE}")
    elif view_mode == 'h':
        print(f"{GREEN}Sending IR code {YELLOW}(hex): 0x{code:0{code_length//4}X}{WHITE}")

    def send_pulse_pwm(duration_us, pwm):
        pi.hardware_PWM(pwm, args.frequency, 500000)  # Set duty cycle to 50%
        time.sleep(duration_us / 1000000.0)
        pi.hardware_PWM(pwm, args.frequency, 0)

    def send_space(duration_us):
        time.sleep(duration_us / 1000000.0)

    send_pulse_pwm(header_pulse, pwm)
    send_space(header_space)

    for i in range(code_length):
        bit = (code >> (code_length - 1 - i)) & 1
        if bit == 1:
            send_pulse_pwm(one_pulse, pwm)
            send_space(one_space)
        else:
            send_pulse_pwm(zero_pulse, pwm)
            send_space(zero_space)

    send_pulse_pwm(ptrail, pwm)
    time.sleep(gap / 1000000.0)

def count_up_from_hex(starting_code, preamble_code, preamble_length, header_pulse, header_space, one_pulse, one_space, zero_pulse, zero_space, ptrail, gap, view_mode, pwm):
    code = int(starting_code, 16)
    code_length = len(bin(code)) - 2
    tried_codes = set()
    total_possible_codes = 2 ** code_length

    try:
        while len(tried_codes) < total_possible_codes:
            if code not in tried_codes:
                send_preamble_and_code(preamble_code, code, preamble_length, code_length,
                                       header_pulse, header_space, one_pulse, one_space,
                                       zero_pulse, zero_space, ptrail, gap, view_mode, pwm)
                time.sleep(0.2)
                tried_codes.add(code)

            code += 1
            if code >= total_possible_codes:
                code = 0
    except KeyboardInterrupt:
        print("\nExiting the script.")

def send_preamble_and_code(preamble_code, code, preamble_length, code_length, header_pulse, header_space, one_pulse, one_space, zero_pulse, zero_space, ptrail, gap, view_mode, pwm):
    if preamble_code is not None:
        send_ir_code(preamble_code, preamble_length, header_pulse, header_space, one_pulse, one_space, zero_pulse, zero_space, ptrail, gap, view_mode, pwm)
    send_ir_code(code, code_length, header_pulse, header_space, one_pulse, one_space, zero_pulse, zero_space, ptrail, gap, view_mode, pwm)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send IR codes in sequence, random, or count-up mode.")
    parser.add_argument("--gpio", type=int, default=18, help="GPIO pin number (default: 18).")
    parser.add_argument("-l", "--length", type=int, default=32, help="Number of bits for the IR codes (default: 32).")
    parser.add_argument("-r", "--random", action="store_true", help="Enable random mode (default is counting-up).")
    parser.add_argument("-m", "--code", type=str, help="IR code to send in hex format (e.g., 0x02A1).")
    parser.add_argument("-p", "--preamble", type=str, help="Fixed preamble IR code to send in hex format (e.g., 0x7FFFF).")
    parser.add_argument("-x", "--repeat", type=int, default=1, help="Number of times to repeat sending the code (default: 1).")
    parser.add_argument("--header_pulse", type=int, default=4058, help="Header pulse duration (microseconds, default: 4058).")
    parser.add_argument("--header_space", type=int, default=3964, help="Header space duration (microseconds, default: 3964).")
    parser.add_argument("--one_pulse", type=int, default=514, help="One pulse duration (microseconds, default: 514).")
    parser.add_argument("--one_space", type=int, default=1980, help="One space duration (microseconds, default: 1980).")
    parser.add_argument("--zero_pulse", type=int, default=514, help="Zero pulse duration (microseconds, default: 514).")
    parser.add_argument("--zero_space", type=int, default=981, help="Zero space duration (microseconds, default: 981).")
    parser.add_argument("--ptrail", type=int, default=514, help="Pulse trail duration (microseconds, default: 514).")
    parser.add_argument("--gap", type=int, default=64729, help="Gap duration (microseconds, default: 64729).")
    parser.add_argument("--frequency", type=int, default=38000, help="Carrier frequency (Hz, default: 38000).")
    parser.add_argument("--duty", type=float, default=50.0, help="Duty cycle for the PWM signal (default: 50.0).")
    parser.add_argument("-sl", "--start_from", type=str, help="Start counting up from the specified hex code.")
    parser.add_argument("-v", "--view", type=str, choices=['b', 'h'], default='h', help="Output view mode: 'b' for binary, 'h' for hex (default: 'h').")
    args = parser.parse_args()

    transmit_pin = args.gpio

    pi.set_mode(transmit_pin, pigpio.OUTPUT)

    pwm_frequency = args.frequency  # Assign the frequency from the arguments
    duty_cycle = args.duty  # Assign the duty cycle from the arguments

    pi.hardware_PWM(transmit_pin, pwm_frequency, int(duty_cycle * 10000))  # Set initial duty cycle

    repetition_counter = 0

    if args.start_from:
        if args.random or args.length > 32 or args.code:
            print("Error: -sl cannot be used in combination with -r, -l > 32, or -m.")
        else:
            if args.preamble:
                preamble_code = int(args.preamble, 16)
                preamble_length = len(bin(preamble_code)) - 2
                count_up_from_hex(args.start_from, preamble_code, preamble_length,
                                  args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                  args.zero_pulse, args.zero_space, args.ptrail, args.gap, args.view, transmit_pin)
            else:
                print("Notice: -sl is specified without -p. The preamble will be ignored.")
                count_up_from_hex(args.start_from, None, None,
                                  args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                  args.zero_pulse, args.zero_space, args.ptrail, args.gap, args.view, transmit_pin)
    else:
        if args.code:
            code = int(args.code, 16)
            code_length = len(bin(code)) - 2
            try:
                while repetition_counter < args.repeat or args.repeat == 0:  # Repeat until the specified count is reached or args.repeat is 0
                    if args.preamble:
                        send_preamble_and_code(int(args.preamble, 16), code, len(bin(args.length)) - 2, args.length,
                                               args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                               args.zero_pulse, args.zero_space, args.ptrail, args.gap, args.view, transmit_pin)
                    else:
                        send_ir_code(code, code_length, args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                     args.zero_pulse, args.zero_space, args.ptrail, args.gap, args.view, transmit_pin)
                    time.sleep(0.2)
                    repetition_counter += 1  # Increment the repetition counter for finite repetitions
            except KeyboardInterrupt:
                print("\nExiting the script.")
        elif args.random:
            num_codes = 2 ** args.length
            tried_codes = set()
            total_possible_codes = 2 ** args.length
            try:
                while repetition_counter < args.repeat or args.repeat == 0:  # Repeat until the specified count is reached or args.repeat is 0
                    while len(tried_codes) < total_possible_codes:
                        code = random.randint(0, total_possible_codes - 1)
                        if code not in tried_codes:
                            for _ in range(args.repeat):
                                if args.preamble:
                                    send_preamble_and_code(int(args.preamble, 16), code, len(bin(args.length)) - 2, args.length,
                                                           args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                                           args.zero_pulse, args.zero_space, args.ptrail, args.gap, args.view, transmit_pin)
                                else:
                                    send_ir_code(code, args.length, args.header_pulse, args.header_space, args.one_pulse,
                                                 args.one_space, args.zero_pulse, args.zero_space, args.ptrail, args.gap, args.view, transmit_pin)
                                time.sleep(0.2)
                                repetition_counter += 1  # Increment the repetition counter for finite repetitions
                            tried_codes.add(code)
            except KeyboardInterrupt:
                print("\nExiting the script.")
        else:
            try:
                while repetition_counter < args.repeat or args.repeat == 0:  # Repeat until the specified count is reached or args.repeat is 0
                    for i in range(1, 2**args.length + 1):
                        for _ in range(args.repeat):
                            if args.preamble:
                                send_preamble_and_code(int(args.preamble, 16), i, len(bin(args.length)) - 2, args.length,
                                                       args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                                       args.zero_pulse, args.zero_space, args.ptrail, args.gap, args.view, transmit_pin)
                            else:
                                send_ir_code(i, args.length, args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                             args.zero_pulse, args.zero_space, args.ptrail, args.gap, args.view, transmit_pin)
                            time.sleep(0.2)
                            repetition_counter += 1  # Increment the repetition counter for finite repetitions
            except KeyboardInterrupt:
                print("\nExiting the script.")

    pi.set_mode(transmit_pin, pigpio.INPUT)  # Set GPIO pin back to INPUT
    pi.stop()  # Stop pigpio
