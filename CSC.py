#!/bin/python3

import pexpect
import os
import struct, fcntl, termios, signal, sys
import keyboard
import argparse


argunments = argparse.ArgumentParser()
argunments.add_argument("-c","--command", required=False, type=str)
a = argunments.parse_args()


child = pexpect.spawn("ssh -X -i \"/root/Desktop/RDP/lucky.pem\" root@ec2-3-134-79-227.us-east-2.compute.amazonaws.com",timeout=99999999)


def sigwinch_passthrough (sig, data):
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ , s))
    global child
    child.setwinsize(a[0],a[1])

signal.signal(signal.SIGWINCH, sigwinch_passthrough)

def ssh_connect():    

        child.expect("root")
        child.sendline("docker container start -i 693ee88c7b30")
        child.expect("#")
        child.interact()
        child.wait()
        if child.close():
                ssh_connect()

while True:
        ssh_connect()
