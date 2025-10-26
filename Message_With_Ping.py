#!/bin/python3
import sys
import os
from scapy.all import IP, ICMP, send, sr1

MAX_ICMP_PAYLOAD_SIZE = 1472  # Max size to avoid fragmentation (IP header + ICMP header = 28 bytes)

def check_sudo():
    """Ensure the script is running as root (sudo)."""
    if os.geteuid() != 0:
        print("This script must be run with sudo!")
        sys.exit(1)

def send_ping_chunk(chunk, target):
    """Send a manually crafted ICMP packet with the given chunk and check for a response."""
    # Ensure we are sending IPv4 packets (not IPv6)
    packet = IP(dst=target)/ICMP(type=8)/chunk.encode()
    
    if len(chunk.encode()) <= MAX_ICMP_PAYLOAD_SIZE:
        reply = sr1(packet, timeout=2, verbose=False)

        if reply:
            print(f"Sent: {chunk}  Response received!")
        else:
            print(f"Sent: {chunk}  No response.")
    else:
        print(f"Message is too large to send in one packet. Consider breaking it up.")

def main():
    check_sudo()  # Ensure script is running with sudo

    if len(sys.argv) != 3:
        print("Usage: Message_With_Ping.py <text> <target>")
        sys.exit(1)

    text = sys.argv[1]
    target = sys.argv[2]


    send_ping_chunk(text, target)

if __name__ == "__main__":
    main()
