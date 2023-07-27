
import random
import time
import argparse
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
transmit_pin = 17
GPIO.setup(transmit_pin, GPIO.OUT)

def send_ir_code(code, code_length, header_pulse, header_space, one_pulse, one_space, zero_pulse, zero_space, ptrail, gap):
    print(f"Sending IR code: {code:X}")

    def send_pulse_pwm(duration_us):
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(duration_us / 1000000.0)
        pwm.ChangeDutyCycle(0)

    def send_space(duration_us):
        time.sleep(duration_us / 1000000.0)

    send_pulse_pwm(header_pulse)
    send_space(header_space)

    for i in range(code_length):
        bit = (code >> (code_length - 1 - i)) & 1
        if bit == 1:
            send_pulse_pwm(one_pulse)
            send_space(one_space)
        else:
            send_pulse_pwm(zero_pulse)
            send_space(zero_space)

    send_pulse_pwm(ptrail)
    time.sleep(gap / 1000000.0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send IR codes in sequence or random mode.")
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
    args = parser.parse_args()

    pwm_frequency = args.frequency  # Assign the frequency from the arguments
    duty_cycle = args.duty  # Assign the duty cycle from the arguments

    pwm = GPIO.PWM(transmit_pin, pwm_frequency)
    pwm.start(duty_cycle)

    def send_preamble_and_code(preamble_code, code, preamble_length, code_length, header_pulse, header_space, one_pulse, one_space, zero_pulse, zero_space, ptrail, gap):
        send_ir_code(preamble_code, preamble_length, header_pulse, header_space, one_pulse, one_space, zero_pulse, zero_space, ptrail, gap)
        send_ir_code(code, code_length, header_pulse, header_space, one_pulse, one_space, zero_pulse, zero_space, ptrail, gap)

    if args.preamble:
        preamble_code = int(args.preamble, 16)
        preamble_length = len(bin(preamble_code)) - 2

    if args.code:
        code = int(args.code, 16)
        code_length = len(bin(code)) - 2
        try:
            for _ in range(args.repeat):
                if args.preamble:
                    send_preamble_and_code(preamble_code, code, preamble_length, code_length,
                                           args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                           args.zero_pulse, args.zero_space, args.ptrail, args.gap)
                else:
                    send_ir_code(code, code_length, args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                 args.zero_pulse, args.zero_space, args.ptrail, args.gap)
        except KeyboardInterrupt:
            print("\nExiting the script.")

    elif args.random:
        num_codes = 100000000
        try:
            for _ in range(num_codes):
                random_code = random.getrandbits(args.length)
                for _ in range(args.repeat):
                    if args.preamble:
                        send_preamble_and_code(preamble_code, random_code, preamble_length, args.length,
                                               args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                               args.zero_pulse, args.zero_space, args.ptrail, args.gap)
                    else:
                        send_ir_code(random_code, args.length, args.header_pulse, args.header_space, args.one_pulse,
                                     args.one_space, args.zero_pulse, args.zero_space, args.ptrail, args.gap)
                    time.sleep(0.2)
        except KeyboardInterrupt:
            print("\nExiting the script.")

    else:
        num_codes = 10000000
        try:
            for i in range(1, num_codes + 1):
                for _ in range(args.repeat):
                    if args.preamble:
                        send_preamble_and_code(preamble_code, i, preamble_length, args.length,
                                               args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                               args.zero_pulse, args.zero_space, args.ptrail, args.gap)
                    else:
                        send_ir_code(i, args.length, args.header_pulse, args.header_space, args.one_pulse, args.one_space,
                                     args.zero_pulse, args.zero_space, args.ptrail, args.gap)
                    time.sleep(0.2)
        except KeyboardInterrupt:
            print("\nExiting the script.")

    pwm.stop()
    GPIO.cleanup()